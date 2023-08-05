'''
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
'''
import os
import logging

from PySide import QtGui

from requests.exceptions import HTTPError
from mapclient.exceptions import ClientRuntimeError

from mapclient.settings.info import DEFAULT_WORKFLOW_PROJECT_FILENAME, \
    DEFAULT_WORKFLOW_ANNOTATION_FILENAME

from mapclient.widgets.utils import set_wait_cursor
from mapclient.widgets.utils import handle_runtime_error

from mapclient.widgets.ui_workflowwidget import Ui_WorkflowWidget
from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclient.widgets.workflowgraphicsscene import WorkflowGraphicsScene
from mapclient.core.workflow import WorkflowError
from mapclient.tools.pmr.pmrtool import PMRTool
from mapclient.tools.pmr.pmrsearchdialog import PMRSearchDialog
from mapclient.tools.pmr.pmrhgcommitdialog import PMRHgCommitDialog
import shutil
from mapclient.widgets.importworkflowdialog import ImportWorkflowDialog

logger = logging.getLogger(__name__)


class WorkflowWidget(QtGui.QWidget):
    '''
    classdocs
    '''
    def __init__(self, mainWindow):
        '''
        Constructor
        '''
        QtGui.QWidget.__init__(self, parent=mainWindow)
        self._mainWindow = mainWindow
        self._ui = Ui_WorkflowWidget()
        self._ui.setupUi(self)

        self._undoStack = QtGui.QUndoStack(self)
        self._undoStack.indexChanged.connect(self.undoStackIndexChanged)

        self._workflowManager = self._mainWindow.model().workflowManager()
        self._graphicsScene = WorkflowGraphicsScene(self)
        self._ui.graphicsView.setScene(self._graphicsScene)

        self._ui.graphicsView.setUndoStack(self._undoStack)
        self._graphicsScene.setUndoStack(self._undoStack)

        self._graphicsScene.setWorkflowScene(self._workflowManager.scene())
        self._graphicsScene.selectionChanged.connect(self._ui.graphicsView.selectionChanged)

        self._ui.executeButton.clicked.connect(self.executeWorkflow)
        self.action_Close = None  # Keep a handle to this for modifying the Ui.
        self._action_annotation = self._mainWindow.findChild(QtGui.QAction, "actionAnnotation")
        self._createMenuItems()

        self.updateStepTree()

        self._updateUi()

    def _updateUi(self):
        if hasattr(self, '_mainWindow'):
            try:
                wfm = self._mainWindow.model().workflowManager()
                self._mainWindow.setWindowTitle(wfm.title())
            except RuntimeError:
                return

            widget_visible = self.isVisible()

            workflow_open = wfm.isWorkflowOpen()
            self.action_Close.setEnabled(workflow_open and widget_visible)
            self.setEnabled(workflow_open and widget_visible)
            self.action_Save.setEnabled(wfm.isModified() and widget_visible)
            self._action_annotation.setEnabled(workflow_open and widget_visible)
            self.action_Import.setEnabled(widget_visible)
            self.action_New.setEnabled(widget_visible)
            self.action_NewPMR.setEnabled(widget_visible)
            self.action_Open.setEnabled(widget_visible)
            self.action_Execute.setEnabled(workflow_open and widget_visible)

    def updateStepTree(self):
        self._ui.stepTree.clear()
        for step in WorkflowStepMountPoint.getPlugins(''):
            self._ui.stepTree.addStep(step)

    def undoStackIndexChanged(self, index):
        self._mainWindow.model().workflowManager().undoStackIndexChanged(index)
        self._updateUi()

    def undoRedoStack(self):
        return self._undoStack

    def showEvent(self, *args, **kwargs):
        self._updateUi()
        return QtGui.QWidget.showEvent(self, *args, **kwargs)

    def hideEvent(self, *args, **kwargs):
        self._updateUi()
        return QtGui.QWidget.hideEvent(self, *args, **kwargs)

    def executeNext(self):
        self._mainWindow.execute()

    def executeWorkflow(self):
        wfm = self._mainWindow.model().workflowManager()
        errors = []

        if wfm.isModified():
            errors.append('The workflow has not been saved.')

        if not wfm.scene().canExecute():
            errors.append('Not all steps in the workflow have been '
                'successfully configured.')

        if not errors:
            self._mainWindow.execute()  # .model().workflowManager().execute()
        else:
            errors_str = '\n'.join(
                ['  %d. %s' % (i + 1, e) for i, e in enumerate(errors)])
            error_msg = ('The workflow could not be executed for the '
                'following reason%s:\n\n%s' % (
                    len(errors) > 1 and 's' or '', errors_str,
            ))
            QtGui.QMessageBox.critical(self, 'Workflow Execution', error_msg,
                QtGui.QMessageBox.Ok)

    def identifierOccursCount(self, identifier):
        return self._mainWindow.model().workflowManager().identifierOccursCount(identifier)

    def setCurrentWidget(self, widget):
        self._mainWindow.setCurrentWidget(widget)

    def setWidgetUndoRedoStack(self, stack):
        self._mainWindow.setCurrentUndoRedoStack(stack)

    def new(self, pmr=False):
        workflowDir = self._getWorkflowDir()
        if workflowDir:
            self._createNewWorkflow(workflowDir, pmr)

    def _getWorkflowDir(self):
        m = self._mainWindow.model().workflowManager()
        workflowDir = QtGui.QFileDialog.getExistingDirectory(self._mainWindow, caption='Select Workflow Directory', directory=m.previousLocation())
        if not workflowDir:
            # user abort
            return ''

        class ProblemClass(object):
            _mk_workflow_dir = False
            _rm_tree_success = True
            def rmTreeUnsuccessful(self, one, two, three):
                self._rm_tree_success = False

        if m.exists(workflowDir):
            # Check to make sure user wishes to overwrite existing workflow.
            ret = QtGui.QMessageBox.warning(self,
                'Replace Existing Workflow',
                'A Workflow already exists at this location.  '
                    'Do you want to replace this Workflow?',
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            # (QtGui.QMessageBox.Warning, '')
            if ret == QtGui.QMessageBox.No:
                # user abort
                return ''
            else:
                # Delete contents of directory
                shutil.rmtree(workflowDir, onerror=ProblemClass.rmTreeUnsuccessful)
                ProblemClass._mk_workflow_dir = True

        # got dir, continue
        if ProblemClass._rm_tree_success:
            if ProblemClass._mk_workflow_dir:
                os.mkdir(workflowDir)
            return workflowDir
        else:
            QtGui.QMessageBox.warning(self,
                'Replace Existing Workflow',
                'Could not remove existing workflow,'
                'New workflow not created.',
                QtGui.QMessageBox.Ok)

        return ''

    @handle_runtime_error
    @set_wait_cursor
    def _createNewWorkflow(self, workflowDir, pmr):
        m = self._mainWindow.model().workflowManager()
        m.new(workflowDir)
        m.setPreviousLocation(workflowDir)

        if pmr:
            pmr_tool = PMRTool()
            if pmr_tool.hasAccess():
                dir_name = os.path.basename(workflowDir)
                try:
                    repourl = pmr_tool.addWorkspace('Workflow: ' + dir_name, None)
                    pmr_tool.linkWorkspaceDirToUrl(workflowDir, repourl)
                except HTTPError as e:
                    logger.exception('Error creating new')
                    self.close()
                    raise ClientRuntimeError(
                        'Error Creating New', e.message)
            else:
                raise ClientRuntimeError('Error Creating New', "Client doesn't have access to PMR")

        self._undoStack.clear()
        self._ui.graphicsView.setLocation(workflowDir)
        self._graphicsScene.updateModel()
        self._updateUi()

    def newpmr(self):
        self.new(pmr=True)

    def load(self):
        m = self._mainWindow.model().workflowManager()
        # Warning: when switching between PySide and PyQt4 the keyword argument for the directory to initialise the dialog to is different.
        # In PySide the keyword argument is 'dir'
        # In PyQt4 the keyword argument is 'directory'
        workflowDir = QtGui.QFileDialog.getExistingDirectory(
            self._mainWindow,
            caption='Open Workflow',
            dir=m.previousLocation(),
            options=(
                QtGui.QFileDialog.ShowDirsOnly |
                QtGui.QFileDialog.DontResolveSymlinks |
                QtGui.QFileDialog.ReadOnly
            )
        )
        if len(workflowDir) > 0:
            try:
                m.load(workflowDir)
                m.setPreviousLocation(workflowDir)
                self._ui.graphicsView.setLocation(workflowDir)
                self._graphicsScene.updateModel()
                self._updateUi()
            except (ValueError, WorkflowError) as e:
                self.close()
                QtGui.QMessageBox.critical(self, 'Error Caught',
                    'Invalid Workflow.  ' + str(e))

    def importFromPMR(self):
        m = self._mainWindow.model().workflowManager()
        dlg = ImportWorkflowDialog(m.previousLocation(), self._mainWindow)
        if dlg.exec_():
            destination_dir = dlg.destinationDir()
            workspace_url = dlg.workspaceUrl()
            if os.path.exists(destination_dir) and workspace_url:
                try:
                    self._importFromPMR(workspace_url, destination_dir)
                except (ValueError, WorkflowError) as e:
                    QtGui.QMessageBox.critical(self, 'Error Caught', 'Invalid Workflow.  ' + str(e))
            else:
                QtGui.QMessageBox.critical(self, 'Error Caught', 'Invalid Import Settings.  Either the workspace url (%s) was not set' \
                                           'or the destination directory (%s) does not exist. ' % (workspace_url, destination_dir))

    @handle_runtime_error
    @set_wait_cursor
    def _importFromPMR(self, workspace_url, workflowDir):
        pmr_tool = PMRTool()

        pmr_tool.cloneWorkspace(
            remote_workspace_url=workspace_url,
            local_workspace_dir=workflowDir,
        )

        logger.info('Analyze first before attempting load ...')
        try:
            m = self._mainWindow.model().workflowManager()
            m.load(workflowDir)
            m.setPreviousLocation(workflowDir)
            self._graphicsScene.updateModel()
            self._updateUi()
        except:
            self.close()
            raise

    def close(self):
        self._mainWindow.confirmClose()
        m = self._mainWindow.model().workflowManager()
        self._undoStack.clear()
        self._graphicsScene.clear()
        m.close()
        self._updateUi()

    def save(self):
        m = self._mainWindow.model().workflowManager()
        if not os.path.exists(m.location()):
            workflow_dir = self._getWorkflowDir()
            if workflow_dir:
                m.setPreviousLocation(workflow_dir)
                m.setLocation(workflow_dir)
        if m.location():
            m.save()
            if self.commitChanges(m.location()):
                self._setIndexerFile(m.location())
            else:
                pass  # undo changes

        self._updateUi()

    def commitChanges(self, workflowDir):
        pmr_tool = PMRTool()
        if not pmr_tool.hasDVCS(workflowDir):
            # nothing to commit.
            return True

        dlg = PMRHgCommitDialog(self)
        dlg.setModal(True)
        if dlg.exec_() == QtGui.QDialog.Rejected:
            return False

        action = dlg.action()
        if action == QtGui.QDialogButtonBox.Ok:
            return True
        elif action == QtGui.QDialogButtonBox.Save:
            return self._commitChanges(workflowDir, dlg.comment(), commit_local=True)

        return self._commitChanges(workflowDir, dlg.comment())

    @handle_runtime_error
    @set_wait_cursor
    def _commitChanges(self, workflowDir, comment, commit_local=False):
        committed_changes = False
        pmr_tool = PMRTool()
        try:
            pmr_tool.commitFiles(workflowDir, comment,
                [workflowDir + '/%s' % (DEFAULT_WORKFLOW_PROJECT_FILENAME),
                 workflowDir + '/%s' % (DEFAULT_WORKFLOW_ANNOTATION_FILENAME)])  # XXX make/use file tracker
            if not commit_local:
                pmr_tool.pushToRemote(workflowDir)
            committed_changes = True
        except ClientRuntimeError:
            # handler will deal with this.
            raise
        except Exception:
            logger.exception('Error')
            raise ClientRuntimeError(
                'Error Saving', 'The commit to PMR did not succeed')

        return committed_changes

    @handle_runtime_error
    @set_wait_cursor
    def _setIndexerFile(self, workflow_dir):
        pmr_tool = PMRTool()

        if not pmr_tool.hasDVCS(workflow_dir):
            return
        try:
            pmr_tool.addFileToIndexer(workflow_dir, DEFAULT_WORKFLOW_ANNOTATION_FILENAME)
#             pmr_tool.commitFiles(local_workspace_dir, message, files)
        except ClientRuntimeError:
            # handler will deal with this.
            raise

    def _setActionProperties(self, action, name, slot, shortcut='', statustip=''):
        action.setObjectName(name)
        action.triggered.connect(slot)
        if len(shortcut) > 0:
            action.setShortcut(QtGui.QKeySequence(shortcut))
        action.setStatusTip(statustip)

    def _createMenuItems(self):
        menu_File = self._mainWindow.menubar.findChild(QtGui.QMenu, 'menu_File')
        menu_Project = self._mainWindow.menubar.findChild(QtGui.QMenu, 'menu_Project')

        lastFileMenuAction = menu_File.actions()[-1]
        menu_New = QtGui.QMenu('&New', menu_File)
#        menu_Open = QtGui.QMenu('&Open', menu_File)

        self.action_NewPMR = QtGui.QAction('PMR Workflow', menu_New)
        self._setActionProperties(self.action_NewPMR, 'action_NewPMR', self.newpmr, 'Ctrl+N', 'Create a new PMR based Workflow')
        self.action_New = QtGui.QAction('Workflow', menu_New)
        self._setActionProperties(self.action_New, 'action_New', self.new, 'Ctrl+Shift+N', 'Create a new Workflow')
        self.action_Open = QtGui.QAction('&Open', menu_File)
        self._setActionProperties(self.action_Open, 'action_Open', self.load, 'Ctrl+O', 'Open an existing Workflow')
        self.action_Import = QtGui.QAction('I&mport', menu_File)
        self._setActionProperties(self.action_Import, 'action_Import', self.importFromPMR, 'Ctrl+M', 'Import existing Workflow from PMR')
        self.action_Close = QtGui.QAction('&Close', menu_File)
        self._setActionProperties(self.action_Close, 'action_Close', self.close, 'Ctrl+W', 'Close open Workflow')
        self.action_Save = QtGui.QAction('&Save', menu_File)
        self._setActionProperties(self.action_Save, 'action_Save', self.save, 'Ctrl+S', 'Save Workflow')
        self.action_Execute = QtGui.QAction('E&xecute', menu_Project)
        self._setActionProperties(self.action_Execute, 'action_Execute', self.executeWorkflow, 'Ctrl+X', 'Execute Workflow')

        menu_New.insertAction(QtGui.QAction(self), self.action_NewPMR)
        menu_New.insertAction(QtGui.QAction(self), self.action_New)
        menu_File.insertMenu(lastFileMenuAction, menu_New)
        menu_File.insertAction(lastFileMenuAction, self.action_Open)
        menu_File.insertSeparator(lastFileMenuAction)
        menu_File.insertAction(lastFileMenuAction, self.action_Import)
        menu_File.insertSeparator(lastFileMenuAction)
        menu_File.insertAction(lastFileMenuAction, self.action_Close)
        menu_File.insertSeparator(lastFileMenuAction)
        menu_File.insertAction(lastFileMenuAction, self.action_Save)
        menu_File.insertSeparator(lastFileMenuAction)
        menu_Project.addAction(self.action_Execute)


