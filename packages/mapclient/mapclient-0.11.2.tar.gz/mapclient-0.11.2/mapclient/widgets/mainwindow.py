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

from PySide import QtGui

from mapclient.widgets.ui_mainwindow import Ui_MainWindow
# from mapclient.mountpoints.stackedwidget import StackedWidgetMountPoint
from mapclient.widgets.workflowwidget import WorkflowWidget
from mapclient.settings.info import DEFAULT_WORKFLOW_ANNOTATION_FILENAME

class MainWindow(QtGui.QMainWindow):
    '''
    This is the main window for the MAP Client.
    '''

    def __init__(self, model):
        '''
        Constructor
        '''
        QtGui.QMainWindow.__init__(self)

        self._model = model

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._setupMenus()
        self.setMenuBar(self.menubar)
        self._makeConnections()

        self._createUndoAction(self.menu_Edit)
        self._createRedoAction(self.menu_Edit)

        self._model.readSettings()
        self.resize(self._model.size())
        self.move(self._model.pos())

        self._model.pluginManager().load()

        self._workflowWidget = WorkflowWidget(self)
        self._ui.stackedWidget.addWidget(self._workflowWidget)
        self.setCurrentUndoRedoStack(self._workflowWidget.undoRedoStack())

        self._pluginManagerDlg = None

    def _setupMenus(self):
        '''
        Because of OS X we have to setup the menubar with no parent so we do
        it manually here instead of through designer.
        '''
        self.menubar = QtGui.QMenuBar()
        self.menubar.setObjectName("menubar")
        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Edit = QtGui.QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")
        self.menu_Project = QtGui.QMenu(self.menubar)
        self.menu_Project.setObjectName("menu_Project")
        self.menu_Tools = QtGui.QMenu(self.menubar)
        self.menu_Tools.setObjectName("menu_Tools")
        self.action_About = QtGui.QAction(self)
        self.action_About.setObjectName("action_About")
        self.action_Quit = QtGui.QAction(self)
        self.action_Quit.setObjectName("action_Quit")
        self.actionPluginManager = QtGui.QAction(self)
        self.actionPluginManager.setObjectName("actionPluginManager")
        self.actionPMR = QtGui.QAction(self)
        self.actionPMR.setObjectName("actionPMR")
        self.actionAnnotation = QtGui.QAction(self)
        self.actionAnnotation.setObjectName("actionAnnotation")
        self.actionPluginWizard = QtGui.QAction(self)
        self.actionPluginWizard.setObjectName("actionPluginWizard")
        self.menu_Help.addAction(self.action_About)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_Tools.addAction(self.actionPluginManager)
        self.menu_Tools.addAction(self.actionPluginWizard)
        self.menu_Tools.addAction(self.actionPMR)
        self.menu_Tools.addAction(self.actionAnnotation)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_Project.menuAction())
        self.menubar.addAction(self.menu_Tools.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self._retranslateUi()

    def _retranslateUi(self):
        self.menu_Help.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Edit.setTitle(QtGui.QApplication.translate("MainWindow", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Project.setTitle(QtGui.QApplication.translate("MainWindow", "&Project", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Tools.setTitle(QtGui.QApplication.translate("MainWindow", "&Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setStatusTip(QtGui.QApplication.translate("MainWindow", "Quit the application", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPluginManager.setText(QtGui.QApplication.translate("MainWindow", "Plugin &Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPMR.setText(QtGui.QApplication.translate("MainWindow", "&PMR", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAnnotation.setText(QtGui.QApplication.translate("MainWindow", "&Annotation", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPluginWizard.setText(QtGui.QApplication.translate("MainWindow", "Plugin Wi&zard", None, QtGui.QApplication.UnicodeUTF8))

    def _createUndoAction(self, parent):
        self.undoAction = QtGui.QAction('Undo', parent)
        self.undoAction.setShortcut(QtGui.QKeySequence('Ctrl+Z'))
        self.undoAction.triggered.connect(self._model.undoManager().undo)
        stack = self._model.undoManager().currentStack()
        if stack:
            self.undoAction.setEnabled(stack.canUndo())
        else:
            self.undoAction.setEnabled(False)

        parent.addAction(self.undoAction)

    def _createRedoAction(self, parent):
        self.redoAction = QtGui.QAction('Redo', parent)
        self.redoAction.setShortcut(QtGui.QKeySequence('Ctrl+Shift+Z'))
        self.redoAction.triggered.connect(self._model.undoManager().redo)
        stack = self._model.undoManager().currentStack()
        if stack:
            self.redoAction.setEnabled(stack.canRedo())
        else:
            self.redoAction.setEnabled(False)

        parent.addAction(self.redoAction)

    def model(self):
        return self._model

    def _makeConnections(self):
        self.action_Quit.triggered.connect(self.quitApplication)
        self.action_About.triggered.connect(self.about)
        self.actionPluginManager.triggered.connect(self.pluginManager)
        self.actionPluginWizard.triggered.connect(self.pluginWizard)
        self.actionPMR.triggered.connect(self.pmr)
        self.actionAnnotation.triggered.connect(self.annotationTool)

    def setCurrentUndoRedoStack(self, stack):
        current_stack = self._model.undoManager().currentStack()
        if current_stack:
            current_stack.canRedoChanged.disconnect(self._canRedoChanged)
            current_stack.canUndoChanged.disconnect(self._canUndoChanged)

        self._model.undoManager().setCurrentStack(stack)

        self.redoAction.setEnabled(stack.canRedo())
        self.undoAction.setEnabled(stack.canUndo())
        stack.canUndoChanged.connect(self._canUndoChanged)
        stack.canRedoChanged.connect(self._canRedoChanged)

    def _canRedoChanged(self, canRedo):
        self.redoAction.setEnabled(canRedo)

    def _canUndoChanged(self, canUndo):
        self.undoAction.setEnabled(canUndo)

    def execute(self):
        if self._ui.stackedWidget.currentWidget() != self._workflowWidget:
            self._ui.stackedWidget.setCurrentWidget(self._workflowWidget)
            self.setCurrentUndoRedoStack(self._workflowWidget.undoRedoStack())
        self.model().workflowManager().execute()

    def setCurrentWidget(self, widget):
        if self._ui.stackedWidget.indexOf(widget) <= 0:
            self._ui.stackedWidget.addWidget(widget)
        self._ui.stackedWidget.setCurrentWidget(widget)

    def closeEvent(self, event):
        self.quitApplication()

    def confirmClose(self):
        # Check to see if the Workflow is in a saved state.
        if self._model.workflowManager().isModified():
            ret = QtGui.QMessageBox.warning(self, 'Unsaved Changes', 'You have unsaved changes, would you like to save these changes now?',
                                      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if ret == QtGui.QMessageBox.Yes:
                self._model.workflowManager().save()

    def quitApplication(self):
        self.confirmClose()

        self._model.setSize(self.size())
        self._model.setPos(self.pos())
        self._model.writeSettings()
        QtGui.qApp.quit()

    def about(self):
        from mapclient.widgets.aboutdialog import AboutDialog
        dlg = AboutDialog(self)
        dlg.setModal(True)
        dlg.exec_()

    def pluginManager(self):
        from mapclient.tools.pluginmanagerdialog import PluginManagerDialog
        pm = self._model.pluginManager()
        dlg = PluginManagerDialog(self)
        self._pluginManagerDlg = dlg
        dlg.setDirectories(pm.directories())
        dlg.setLoadDefaultPlugins(pm.loadDefaultPlugins())
        dlg.reloadPlugins = self._pluginManagerReloadPlugins

        dlg.setModal(True)
        if dlg.exec_():
            directories_modified = pm.setDirectories(dlg.directories())
            defaults_modified = pm.setLoadDefaultPlugins(dlg.loadDefaultPlugins())
            if directories_modified or defaults_modified:
                pm.load()
                self._workflowWidget.updateStepTree()

        self._pluginManagerDlg = None

    def _pluginManagerReloadPlugins(self):
        '''
        Callback from the plugin manager to reload the current plugins.
        '''
        pm = self._model.pluginManager()
        pm.setDirectories(self._pluginManagerDlg.directories())
        pm.setLoadDefaultPlugins(self._pluginManagerDlg.loadDefaultPlugins())
        pm.load()
        self._workflowWidget.updateStepTree()

    def pluginWizard(self):
        from mapclient.tools.pluginwizard.wizarddialog import WizardDialog
        from mapclient.tools.pluginwizard.skeleton import Skeleton
        dlg = WizardDialog(self)

        dlg.setModal(True)
        if dlg.exec_() == dlg.Accepted:
            s = Skeleton(dlg.getOptions())
            try:
                s.write()
                QtGui.QMessageBox.information(self, 'Skeleton Step', 'The Skeleton step has successfully been written to disk.')
            except:
                QtGui.QMessageBox.critical(self, 'Error Writing Step', 'There was an error writing the step, perhaps the step already exists.')

    def pmr(self):
        from mapclient.tools.pmr.pmrsearchdialog import PMRSearchDialog
        dlg = PMRSearchDialog(self)
        dlg.setModal(True)
        dlg.exec_()

    def annotationTool(self):
        from mapclient.tools.annotation.annotationdialog import AnnotationDialog
        location = self._model.workflowManager().location()
        dlg = AnnotationDialog(location, DEFAULT_WORKFLOW_ANNOTATION_FILENAME, self)
        dlg.setModal(True)
        dlg.exec_()

