
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
from PySide.QtGui import QDialog, QFileDialog, QDialogButtonBox

from mapclientplugins.imagesourcestep.widgets.ui_configuredialog import Ui_ConfigureDialog
from mapclient.tools.pmr.pmrworkflowwidget import PMRWorkflowWidget
import os
from mapclient.tools.pmr.pmrtool import ontological_search_string, \
    plain_text_search_string

REQUIRED_STYLE_SHEET = 'border: 1px solid red; border-radius: 3px'
DEFAULT_STYLE_SHEET = 'border: 1px solid gray; border-radius: 3px'

class ConfigureDialogState(object):

    def __init__(self, identifier='', local_location='', pmr_location='', image_type=0, current_tab=0, previous_local_location=''):
        self._identifier = identifier
        self._local_location = local_location
        self._pmr_location = pmr_location
        self._image_type = image_type
        self._current_tab = current_tab
        self._previous_local_location = previous_local_location

    def location(self):
        return self._local_location

    def setLocation(self, location):
        self._local_location = location

    def pmrLocation(self):
        return self._pmr_location

    def identifier(self):
        return self._identifier

    def setIdentifier(self, identifier):
        self._identifier = identifier

    def imageType(self):
        return self._image_type

    def currentTab(self):
        return self._current_tab

    def previousLocalLocation(self):
        return self._previous_local_location

    def save(self, conf):
        conf.beginGroup('status')
        conf.setValue('identifier', self._identifier)
        conf.setValue('localLocation', self._local_location)
        conf.setValue('pmrLocation', self._pmr_location)
        conf.setValue('imageType', self._image_type)
        conf.setValue('currentTab', self._current_tab)
        conf.setValue('previousLocalLocation', self._previous_local_location)
        conf.endGroup()

    def load(self, conf):
        conf.beginGroup('status')
        self._identifier = conf.value('identifier', '')
        self._local_location = conf.value('localLocation', '')
        self._pmr_location = conf.value('pmrLocation', '')
        self._image_type = int(conf.value('imageType', 0))
        self._current_tab = int(conf.value('currentTab', 0))
        self._previous_local_location = conf.value('previousLocalLocation', '')
        conf.endGroup()


class ConfigureDialog(QDialog):
    '''
    Configure dialog to present the user with the options to configure this step.
    '''


    def __init__(self, state, parent=None):
        '''
        Constructor
        '''
        QDialog.__init__(self, parent)
        self._ui = Ui_ConfigureDialog()
        self._ui.setupUi(self)
        self._setupPMRTab()

        self.setState(state)

        self.validate()

        self._makeConnections()

    def _makeConnections(self):
        self._ui.identifierLineEdit.textChanged.connect(self.validate)
        self._ui.localLineEdit.textChanged.connect(self._localLocationEdited)
        self._ui.localButton.clicked.connect(self._localLocationClicked)
        self._pmr_widget._ui.lineEditWorkspace.textChanged.connect(self._workspaceChanged)
#         self._ui.pmrRegisterLabel.linkActivated.connect(self._register)

    def _setupPMRTab(self):
        self._pmr_widget = PMRWorkflowWidget(self)
        self._pmr_widget.setImport(False)
        self._pmr_widget.setExport(False)
        self._pmr_widget.setSearchDomain([ontological_search_string, plain_text_search_string])

        layout = self._ui.pmrTab.layout()
        layout.addWidget(self._pmr_widget)

    def setState(self, state):
        self._ui.identifierLineEdit.setText(state._identifier)
        self._ui.localLineEdit.setText(state._local_location)
        self._pmr_widget.setWorkspaceUrl(state._pmr_location)
        self._ui.imageSourceTypeComboBox.setCurrentIndex(state._image_type)
        self._ui.tabWidget.setCurrentIndex(state._current_tab)
        self._ui.previousLocationLabel.setText(state._previous_local_location)

    def getState(self):
        state = ConfigureDialogState(
            self._ui.identifierLineEdit.text(),
            self._ui.localLineEdit.text(),
            self._pmr_widget.workspaceUrl(),
            self._ui.imageSourceTypeComboBox.currentIndex(),
            self._ui.tabWidget.currentIndex(),
            self._ui.previousLocationLabel.text())

        return state

    def _localLocationClicked(self):
        location = QFileDialog.getExistingDirectory(self, 'Select Image File(s) Location', self._ui.previousLocationLabel.text())

        if location:
            self._ui.previousLocationLabel.setText(location)
            self._ui.localLineEdit.setText(location)

    def _workspaceChanged(self, text):
        pass

    def _localLocationEdited(self):
        self.validate()

    def localLocation(self):
        return self._ui.localLineEdit.text()

    def validate(self):
        identifierValid = len(self._ui.identifierLineEdit.text()) > 0
        localValid = os.path.exists(self._ui.localLineEdit.text())
        valid = identifierValid

        self._ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(valid)

        if identifierValid:
            self._ui.identifierLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.identifierLineEdit.setStyleSheet(REQUIRED_STYLE_SHEET)

        return valid and localValid


