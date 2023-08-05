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

import os, platform

from PySide import QtCore, QtGui

from mapclient.widgets.utils import createDefaultImageIcon

from mapclient.tools.pluginwizard.skeleton import SkeletonOptions
from mapclient.tools.pluginwizard.ui_output import Ui_Output
from mapclient.tools.pluginwizard.ui_name import Ui_Name
from mapclient.tools.pluginwizard.ui_ports import Ui_Ports
from mapclient.tools.pluginwizard.ui_config import Ui_Config
from mapclient.tools.pluginwizard.ui_misc import Ui_Misc

# Registered field names:
OUTPUT_DIRECTORY_FIELD = 'output_directory'
NAME_FIELD = 'name'
IMAGE_FILE_FIELD = 'image_file'
PACKAGE_NAME_FIELD = 'package_name'
PORTS_FIELD = 'ports_table'
IDENTIFIER_CHECKBOX = 'identifier_checkbox'
CATEGORY_FIELD = 'category'
AUTHOR_NAME_FIELD = 'author_name'
# Style sheets
REQUIRED_STYLE_SHEET = 'background-color: rgba(239, 16, 16, 20%)'
DEFAULT_STYLE_SHEET = ''

class WizardDialog(QtGui.QWizard):


    def __init__(self, parent=None):
        super(WizardDialog, self).__init__(parent)
        self.setWindowTitle('Workflow Step Wizard')
        self.setFixedSize(675, 550)

        if platform.system() == 'Darwin':
            self.setWizardStyle(QtGui.QWizard.MacStyle)
        else:
            self.setWizardStyle(QtGui.QWizard.ModernStyle)
        # set pages
        self.addPage(createIntroPage())
        self.addPage(NameWizardPage())
        self.addPage(PortsWizardPage())
        self.addPage(ConfigWizardPage())
        self.addPage(MiscWizardPage())
        self.addPage(OutputWizardPage())

        # set images banner, logo, watermark and background
        self.setPixmap(QtGui.QWizard.LogoPixmap, QtGui.QPixmap(':/wizard/images/logo.png'))
        self.setPixmap(QtGui.QWizard.BannerPixmap, QtGui.QPixmap(':/wizard/images/banner.png'))
#         self.setPixmap(QtGui.QWizard.WatermarkPixmap, QtGui.QPixmap(':/wizard/images/watermark.png'))
#         self.setPixmap(QtGui.QWizard.BackgroundPixmap, QtGui.QPixmap(':/wizard/images/background.png'))
        self._options = SkeletonOptions()

    def getOptions(self):
        return self._options

    def accept(self):
        self._options.setOutputDirectory(self.field(OUTPUT_DIRECTORY_FIELD))
        self._options.setImageFile(self.field(IMAGE_FILE_FIELD))
        self._options.setName(self.field(NAME_FIELD))
        self._options.setPackageName(self.field(PACKAGE_NAME_FIELD))

        # Registered field failed to return table, may need to set up
        # default property for this to work.  Currently using workaround
        # by directly getting desired widget
        ports_table = self.page(2)._ui.portTableWidget
        row_index = 0
        while row_index < ports_table.rowCount():
            self._options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#' + ports_table.cellWidget(row_index, 0).currentText(),
                                   ports_table.item(row_index, 1).text())
            row_index += 1

        if self.page(3)._ui.identifierCheckBox.isChecked():
            self._options.addConfig('identifier', '')

        configs_table = self.page(3)._ui.configTableWidget
        row_index = 0
        while row_index < configs_table.rowCount():
            config_label = configs_table.item(row_index, 0)
            config_default_value = configs_table.item(row_index, 1)
            if config_label is not None:
                self._options.addConfig(config_label.text(),
                                        '' if config_default_value is None else config_default_value.text())
            row_index += 1

        self._options.setCategory(self.field(CATEGORY_FIELD))
        self._options.setAuthorName(self.field(AUTHOR_NAME_FIELD))

        super(WizardDialog, self).accept()


def createIntroPage():
    page = QtGui.QWizardPage()
    page.setTitle('Introduction')
    page.setSubTitle('Create skeleton Python code to get started creating a workflow step.')
    label = QtGui.QLabel('This wizard will help get you started creating your own plugin for the MAP Client.')
    label.setWordWrap(True)

    layout = QtGui.QVBoxLayout()
    layout.addWidget(label)
    page.setLayout(layout)

    page.setPixmap(QtGui.QWizard.WatermarkPixmap, QtGui.QPixmap(':/wizard/images/watermark.png'))
    page.setPixmap(QtGui.QWizard.BackgroundPixmap, QtGui.QPixmap(':/wizard/images/background.png'))
    page.setPixmap(QtGui.QWizard.BannerPixmap, QtGui.QPixmap(':/wizard/images/banner.png'))

    return page


class NameWizardPage(QtGui.QWizardPage):

    def __init__(self, parent=None):
        super(NameWizardPage, self).__init__(parent)

        self.setTitle('Identify Workflow Step')
        self.setSubTitle('Set the name and icon (optional) for the workflow step.')

        self._ui = Ui_Name()
        self._ui.setupUi(self)

        self._invalidPixmap = QtGui.QPixmap(':wizard/images/cross.png')
        self._invalidNameLabel = QtGui.QLabel(self)
        self._invalidNameLabel.setStyleSheet('border: none; padding: 0px;')
        self._invalidPackageLabel = QtGui.QLabel(self)
        self._invalidPackageLabel.setStyleSheet('border: none; padding: 0px;')
        self._invalidIconLabel = QtGui.QLabel(self)
        self._invalidIconLabel.setStyleSheet('border: none; padding: 0px;')

        self._updateImage()

        self._makeConnections()
        self._defineFields()
        self._packageNameEdited = False

    def _defineFields(self):
        self.registerField(NAME_FIELD, self._ui.nameLineEdit)
        self.registerField(PACKAGE_NAME_FIELD, self._ui.packageNameLineEdit)
        self.registerField(IMAGE_FILE_FIELD, self._ui.iconLineEdit)

    def _makeConnections(self):
        self._ui.nameLineEdit.textChanged.connect(self._nameChanged)
        self._ui.nameLineEdit.textChanged.connect(self._updateImage)
        self._ui.packageNameLineEdit.textEdited.connect(self._packageNameChanged)
        self._ui.iconLineEdit.textChanged.connect(self._updateImage)
        self._ui.iconButton.clicked.connect(self._chooseImage)

    def _nameChanged(self):
        self.completeChanged.emit()
        if not self._packageNameEdited:
            package_name = self._ui.nameLineEdit.text().lower()
            package_name = package_name.replace(' ', '')
            self._ui.packageNameLineEdit.setText(package_name + 'step')

    def _packageNameChanged(self):
        self._packageNameEdited = True

    def _chooseImage(self):
        image, _ = QtGui.QFileDialog.getOpenFileName(self, caption='Choose Image File', options=QtGui.QFileDialog.ReadOnly)
        if len(image) > 0:
            self._ui.iconLineEdit.setText(image)

    def _updateImage(self):

        image_file = self._ui.iconLineEdit.text()
        if image_file:
            image = QtGui.QPixmap(image_file)
            if image:
                self._ui.iconPictureLabel.setPixmap(image.scaled(64, 64, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation))
        else:
            image = createDefaultImageIcon(self._ui.nameLineEdit.text())
            self._ui.iconPictureLabel.setPixmap(QtGui.QPixmap.fromImage(image).scaled(64, 64, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation))

        self.completeChanged.emit()

    def resizeEvent(self, event):
        rect = self._ui.nameLineEdit.rect()
        pos = self._ui.nameLineEdit.pos()
        self._invalidNameLabel.setPixmap(self._invalidPixmap.scaledToHeight(rect.height() / 2))
        self._invalidNameLabel.move(pos.x() - rect.height() / 2, pos.y() + rect.height() / 4)
        self._invalidNameLabel.setFixedSize(self._invalidNameLabel.sizeHint())
        rect = self._ui.packageNameLineEdit.rect()
        pos = self._ui.packageNameLineEdit.pos()
        self._invalidPackageLabel.setPixmap(self._invalidPixmap.scaledToHeight(rect.height() / 2))
        self._invalidPackageLabel.move(pos.x() - rect.height() / 2, pos.y() + rect.height() / 4)
        self._invalidPackageLabel.setFixedSize(self._invalidPackageLabel.sizeHint())
        rect = self._ui.iconLineEdit.rect()
        pos = self._ui.iconLineEdit.pos()
        self._invalidIconLabel.setPixmap(self._invalidPixmap.scaledToHeight(rect.height() / 2))
        self._invalidIconLabel.move(pos.x() - rect.height() / 2, pos.y() + rect.height() / 4)
        self._invalidIconLabel.setFixedSize(self._invalidIconLabel.sizeHint())

    def isComplete(self):
        name_status = False
        if len(self._ui.nameLineEdit.text()) > 0:
            name_status = True

        package_status = isValidPythonPackageName(self._ui.packageNameLineEdit.text())

        image_status = os.path.exists(self._ui.iconLineEdit.text()) if len(self._ui.iconLineEdit.text()) > 0 else True

        self._invalidNameLabel.setVisible(not name_status)
        self._invalidPackageLabel.setVisible(not package_status)
        self._invalidIconLabel.setVisible(not image_status)

        return name_status and package_status and image_status


class PortsWizardPage(QtGui.QWizardPage):

    def __init__(self, parent=None):
        super(PortsWizardPage, self).__init__(parent)

        self.setTitle('Set Step Ports')
        self.setSubTitle('Set the ports for the workflow step.')

        self._ui = Ui_Ports()
        self._ui.setupUi(self)

        self._ui.portTableWidget.setColumnCount(2)
        self._ui.portTableWidget.setShowGrid(False)
        self._ui.portTableWidget.setHorizontalHeaderLabels(['Type', 'Object'])
        horizontal_header = self._ui.portTableWidget.horizontalHeader()
        horizontal_header.setStretchLastSection(True)

        self._updateUi()
        self._defineFields()
        self._makeConnections()

    def _defineFields(self):
        self.registerField(PORTS_FIELD, self._ui.portTableWidget)

    def _updateUi(self):
        have_selected_rows = len(self._ui.portTableWidget.selectedIndexes()) > 0
        self._ui.removeButton.setEnabled(have_selected_rows)

    def _makeConnections(self):
        self._ui.addButton.clicked.connect(self._addPort)
        self._ui.removeButton.clicked.connect(self._removePort)
        self._ui.portTableWidget.itemSelectionChanged.connect(self._updateUi)

    def _addPort(self):

        def createPortTypeComboBox():
            cb = QtGui.QComboBox()
            cb.addItems(['provides', 'uses'])

            return cb

        next_row = self._ui.portTableWidget.rowCount()
        self._ui.portTableWidget.insertRow(next_row)
        self._ui.portTableWidget.setCellWidget(next_row, 0, createPortTypeComboBox())

    def _removePort(self):
        indexes = self._ui.portTableWidget.selectedIndexes()
        reversed_rows = indexes[::2]
        reversed_rows.reverse()
        for row in reversed_rows:
            self._ui.portTableWidget.removeRow(row.row())

class ConfigWizardPage(QtGui.QWizardPage):

    def __init__(self, parent=None):
        super(ConfigWizardPage, self).__init__(parent)

        self.setTitle('Configure Workflow Step')
        self.setSubTitle('Setup the configuration for the workflow step.')

        self._ui = Ui_Config()
        self._ui.setupUi(self)

        self._ui.identifierCheckBox.setChecked(True)

        horizontal_header = self._ui.configTableWidget.horizontalHeader()
        horizontal_header.setStretchLastSection(True)
#         self._addConfigurationRow()
#         self._ui.configTableWidget.setItem(0, 0, QtGui.QTableWidgetItem('Identifier'))
#         self._ui.configTableWidget.setItem(0, 1, QtGui.QTableWidgetItem(''))

        self._updateUi()
        self._makeConnections()

    def _defineFields(self):
        self.registerField(IDENTIFIER_CHECKBOX, self._ui.identifierCheckBox)

    def _makeConnections(self):
        self._ui.addButton.clicked.connect(self._addConfigurationRow)
        self._ui.removeButton.clicked.connect(self._removeConfigurationRow)
        self._ui.configTableWidget.itemSelectionChanged.connect(self._updateUi)

    def _updateUi(self):
        have_selected_rows = len(self._ui.configTableWidget.selectedIndexes()) > 0
        self._ui.removeButton.setEnabled(have_selected_rows)

    def _addConfigurationRow(self):
        next_row = self._ui.configTableWidget.rowCount()
        self._ui.configTableWidget.insertRow(next_row)

    def _removeConfigurationRow(self):
        indexes = self._ui.configTableWidget.selectedIndexes()
        reversed_rows = indexes[::2]
        reversed_rows.reverse()
        for row in reversed_rows:
            self._ui.configTableWidget.removeRow(row.row())


class MiscWizardPage(QtGui.QWizardPage):

    def __init__(self, parent=None):
        super(MiscWizardPage, self).__init__(parent)

        self.setTitle('Miscellaneous Options')
        self.setSubTitle('Specify miscellaneous options for the plugin.')

        self._ui = Ui_Misc()
        self._ui.setupUi(self)

        self.registerField(AUTHOR_NAME_FIELD, self._ui.authorNameLineEdit)
        self.registerField(CATEGORY_FIELD, self._ui.categoryLineEdit)

class OutputWizardPage(QtGui.QWizardPage):

    def __init__(self, parent=None):
        super(OutputWizardPage, self).__init__(parent)

        self.setTitle('Output Files')
        self.setSubTitle('Specify where you want the wizard to put the generated skeleton code.')

        self._ui = Ui_Output()
        self._ui.setupUi(self)

        self._invalidPixmap = QtGui.QPixmap(':wizard/images/cross.png')
        self._invalidDirectoryLabel = QtGui.QLabel(self)
        self._invalidDirectoryLabel.setStyleSheet('border: none; padding: 0px;')

        self.registerField(OUTPUT_DIRECTORY_FIELD, self._ui.directoryLineEdit)

        self._makeConnections()

    def _makeConnections(self):
        self._ui.directoryLineEdit.textChanged.connect(self.completeChanged)
        self._ui.directoryButton.clicked.connect(self._chooseDirectory)

    def _chooseDirectory(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, caption='Select Output Directory', directory=self._ui.directoryLineEdit.text(), options=QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ReadOnly)
        if len(directory) > 0:
            self._ui.directoryLineEdit.setText(directory)

    def resizeEvent(self, event):
        rect = self._ui.directoryLineEdit.rect()
        pos = self._ui.directoryLineEdit.pos()
        self._invalidDirectoryLabel.setPixmap(self._invalidPixmap.scaledToHeight(rect.height() / 2))
        self._invalidDirectoryLabel.move(pos.x() - rect.height() / 2, pos.y() + rect.height() / 4)
        self._invalidDirectoryLabel.setFixedSize(self._invalidDirectoryLabel.sizeHint())

    def isComplete(self):
        status = False
        directory = self._ui.directoryLineEdit.text()
        if os.path.isdir(directory) and os.access(directory, os.W_OK | os.X_OK):
            status = True

        self._invalidDirectoryLabel.setVisible(not status)

        return status

def isValidPythonPackageName(name):
    return True

