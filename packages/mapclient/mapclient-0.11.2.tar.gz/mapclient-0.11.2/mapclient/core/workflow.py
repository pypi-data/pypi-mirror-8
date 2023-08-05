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

from PySide import QtCore

from mapclient.settings import info
from mapclient.core.workflowscene import WorkflowScene
from mapclient.core.workflowerror import WorkflowError
from mapclient.core.workflowrdf import serializeWorkflowAnnotation

_PREVIOUS_LOCATION_STRING = 'previousLocation'

def _getWorkflowConfiguration(location):
#     print('get workflow confiburation: ' + location)
    return QtCore.QSettings(_getWorkflowConfigurationAbsoluteFilename(location), QtCore.QSettings.IniFormat)

def _getWorkflowConfigurationAbsoluteFilename(location):
#     print('get workflow configuration abs filename: ' + os.path.join(location, info.DEFAULT_WORKFLOW_PROJECT_FILENAME))
    return os.path.join(location, info.DEFAULT_WORKFLOW_PROJECT_FILENAME)

def _getWorkflowMetaAbsoluteFilename(location):
    return os.path.join(location, info.DEFAULT_WORKFLOW_ANNOTATION_FILENAME)

class WorkflowManager(object):
    '''
    This class manages (models?) the workflow.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.name = 'WorkflowManager'
#        self.widget = None
#        self.widgetIndex = -1
        self._location = ''
        self._workspace_location = None
        self._conf_filename = None
        self._previousLocation = None
        self._saveStateIndex = 0
        self._currentStateIndex = 0

        self._title = None

        self._scene = WorkflowScene(self)

    def title(self):
        self._title = info.APPLICATION_NAME
        if self._location:
            self._title = self._title + ' - ' + self._location
        if self._saveStateIndex != self._currentStateIndex:
            self._title = self._title + ' *'

        return self._title

    # Why set/get? all _prefix are public anyway, just use attributes...
    # if they need to be modified they can be turned into properties
    def setLocation(self, location):
        self._location = location

    def location(self):
        return self._location

    def setPreviousLocation(self, location):
        self._previousLocation = location

    def previousLocation(self):
        return self._previousLocation

    def scene(self):
        return self._scene

    def undoStackIndexChanged(self, index):
        self._currentStateIndex = index

    def identifierOccursCount(self, identifier):
        return self._scene.identifierOccursCount(identifier)

    def execute(self):
        self._scene.execute()

    def isModified(self):
        return self._saveStateIndex != self._currentStateIndex

    def new(self, location):
        '''
        Create a new workflow at the given location.  The location is a directory, it must exist
        it will not be created.  A file '.workflow.conf' is created in the directory at 'location' which holds
        information relating to the workflow.
        '''
        if location is None:
            raise WorkflowError('No location given to create new Workflow.')

        if not os.path.exists(location):
            raise WorkflowError('Location %s does not exist.' % location)

        self._location = location
        wf = _getWorkflowConfiguration(location)
        wf.setValue('version', info.VERSION_STRING)
#        self._title = info.APPLICATION_NAME + ' - ' + location
        self._scene.clear()

    def exists(self, location):
        '''
        Determines whether a workflow exists in the given location.
        Returns True if a valid workflow exists, False otherwise.
        '''
        if location is None:
            return False

        if not os.path.exists(location):
            return False

        wf = _getWorkflowConfiguration(location)
        if wf.contains('version'):
            return True

        return False

    def load(self, location):
        '''
        Open a workflow from the given location.
        :param location:
        '''
        if location is None:
            raise WorkflowError('No location given to open Workflow.')

        if not os.path.exists(location):
            raise WorkflowError('Location %s does not exist' % location)

        wf = _getWorkflowConfiguration(location)
        if not wf.contains('version'):
            raise WorkflowError('The given Workflow configuration file is not valid.')

        workflow_version = versionTuple(wf.value('version'))
        software_version = versionTuple(info.VERSION_STRING)
        if not workflow_version[0:2] == software_version[0:2]:
            # compare first two elements of version (major, minor)
            raise WorkflowError(
                'Major/Minor version number mismatch - '
                'application version: %s; workflow version: %s.' %
                    (info.VERSION_STRING, wf.value('version'))
            )
        if not workflow_version[2] <= software_version[2]:
            raise WorkflowError(
                'Patch version number of the workflow cannot be newer than '
                'application - '
                'application version: %s; workflow version: %s' %
                    (info.VERSION_STRING, wf.value('version'))
            )

        self._location = location
#        wf = _getWorkflowConfiguration()
        self._scene.loadState(wf)
        self._saveStateIndex = self._currentStateIndex = 0
#        self._title = info.APPLICATION_NAME + ' - ' + location

    def save(self):
        wf = _getWorkflowConfiguration(self._location)
        self._scene.saveState(wf)
        self._saveStateIndex = self._currentStateIndex
        af = _getWorkflowMetaAbsoluteFilename(self._location)
        f = open(af, 'w')
        f.write(serializeWorkflowAnnotation())
        self._scene.saveAnnotation(f)
        f.close()

#        self._title = info.APPLICATION_NAME + ' - ' + self._location

    def close(self):
        '''
        Close the current workflow
        '''
        self._location = ''
        self._saveStateIndex = self._currentStateIndex = 0
#        self._title = info.APPLICATION_NAME

    def isWorkflowOpen(self):
        return True  # not self._location == None

    def writeSettings(self, settings):
        settings.beginGroup(self.name)
        settings.setValue(_PREVIOUS_LOCATION_STRING, self._previousLocation)
        settings.endGroup()

    def readSettings(self, settings):
        settings.beginGroup(self.name)
        self._previousLocation = settings.value(_PREVIOUS_LOCATION_STRING, '')
        settings.endGroup()

def versionTuple(v):
    return tuple(map(int, (v.split("."))))
