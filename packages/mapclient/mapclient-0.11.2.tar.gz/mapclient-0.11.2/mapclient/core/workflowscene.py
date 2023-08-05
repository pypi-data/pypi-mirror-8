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
from PySide import QtCore

from mapclient.mountpoints.workflowstep import workflowStepFactory
from mapclient.core.workflowerror import WorkflowError

class Item(object):


    def __init__(self):
        self._selected = True

    def selected(self):
        return self._selected


class MetaStep(Item):


    Type = 'Step'

    def __init__(self, step):
        Item.__init__(self)
        self._step = step
        self._pos = QtCore.QPoint(0, 0)

    def pos(self):
        return self._pos

    def getIdentifier(self):
        return self._step.getIdentifier()

class Connection(Item):


    Type = 'Connection'

    def __init__(self, source, sourceIndex, destination, destinationIndex):
        Item.__init__(self)
        self._source = source
        self._sourceIndex = sourceIndex
        self._destination = destination
        self._destinationIndex = destinationIndex

    def source(self):
        return self._source

    def sourceIndex(self):
        return self._sourceIndex

    def destination(self):
        return self._destination

    def destinationIndex(self):
        return self._destinationIndex


class WorkflowDependencyGraph(object):


    def __init__(self, scene):
        self._scene = scene
        self._dependencyGraph = {}
        self._reverseDependencyGraph = {}
        self._topologicalOrder = []
        self._current = -1

    def _findAllConnectedNodes(self):
        '''
        Return a list of all the nodes that have a connection.
        '''
        nodes = []
        for item in self._scene.items():
            if item.Type == Connection.Type:
                if item.source() not in nodes:
                    nodes.append(item.source())
                if item.destination() not in nodes:
                    nodes.append(item.destination())

        return nodes

    def _nodeIsDestination(self, graph, node):
        '''
        Determine whether or not the given node features
        in a destination of another node.  Return True if
        the node is a destination, False otherwise..
        '''
        for graph_node in graph:
            if node in graph[graph_node]:
                return True

        return False

    def _findStartingSet(self, graph, nodes):
        '''
        Find the set of all nodes that are connected but are
        not destinations for any other node.
        '''
        starting_set = []
        for node in nodes:
            # Determine if node is a destination, if it is it is not a starting node
            if not self._nodeIsDestination(graph, node):
                starting_set.append(node)

        return starting_set

    def _determineTopologicalOrder(self, graph, starting_set):
        '''
        Determine the topological order of the graph.  Returns
        an empty list if the graph contains a loop.
        '''
        # Find topological order
        temp_graph = graph.copy()
        topologicalOrder = []
        while len(starting_set) > 0:
            node = starting_set.pop()
            topologicalOrder.append(node)
            if node in temp_graph:
                for m in temp_graph[node][:]:
                    temp_graph[node].remove(m)
                    if len(temp_graph[node]) == 0:
                        del temp_graph[node]
                    if not self._nodeIsDestination(temp_graph, m):
                        starting_set.append(m)

        # If the graph is not empty we have detected a loop,
        # or independent graphs.
        if temp_graph:
            return []

        return topologicalOrder

    def _calculateDependencyGraph(self):
        graph = {}
        for item in self._scene.items():
            if item.Type == Connection.Type:
                graph[item.source()] = graph.get(item.source(), [])
                graph[item.source()].append(item.destination())

        return graph

    def _connectionsForNodes(self, source, destination):
        connections = []
        for item in self._scene.items():
            if item.Type == Connection.Type:
                if item.source() == source and item.destination() == destination:
                    connections.append(item)

        return connections

    def canExecute(self):
        self._dependencyGraph = self._calculateDependencyGraph()
        self._reverseDependencyGraph = reverseDictWithLists(self._dependencyGraph)
        # Find all connected nodes in the graph
        nodes = self._findAllConnectedNodes()
        # Find starting point set, uses helper graph
        starting_set = self._findStartingSet(self._dependencyGraph, nodes)

        self._topologicalOrder = self._determineTopologicalOrder(self._dependencyGraph, starting_set)

        configured = [metastep for metastep in self._topologicalOrder if metastep._step.isConfigured()]
        can = len(configured) == len(self._topologicalOrder) and len(self._topologicalOrder) >= 0
        return can and self._current == -1

    def execute(self):
        self._current += 1
        if self._current >= len(self._topologicalOrder):
            self._current = -1
        else:
            # Form input requirements
            current_node = self._topologicalOrder[self._current]
            if current_node in self._reverseDependencyGraph:
                connections = []
                for node in self._reverseDependencyGraph[current_node]:
                    # Find connection information and extract outputs from steps
                    new_connections = self._connectionsForNodes(node, current_node)
                    connections.extend([c for c in new_connections if c not in connections])
                    if len(new_connections) == 0:
                        raise WorkflowError('Connection in workflow not found, something has gone horribly wrong')

                for connection in connections:
                    dataIn = connection.source()._step.getPortData(connection.sourceIndex())
                    current_node._step.setPortData(connection.destinationIndex(), dataIn)

            current_node._step.execute()


class WorkflowScene(object):
    '''
    This is the authoratative model for the workflow scene.
    '''

    def __init__(self, manager):
        self._manager = manager
        self._items = {}
        self._dependencyGraph = WorkflowDependencyGraph(self)

    def saveAnnotation(self, f):
        pass

    def saveState(self, ws):
        connectionMap = {}
        stepList = []
        for item in self._items:
            if item.Type == MetaStep.Type:
                stepList.append(item)
            elif item.Type == Connection.Type:
                if item.source() in connectionMap:
                    connectionMap[item.source()].append(item)
                else:
                    connectionMap[item.source()] = [item]

        location = self._manager.location()
        ws.remove('nodes')
        ws.beginGroup('nodes')
        ws.beginWriteArray('nodelist')
        nodeIndex = 0
        for metastep in stepList:
            if metastep._step.isConfigured():
                metastep._step.serialize(location)
            ws.setArrayIndex(nodeIndex)
            ws.setValue('name', metastep._step.getName())
            ws.setValue('position', metastep._pos)
            ws.setValue('selected', metastep._selected)
            identifier = metastep._step.getIdentifier()
            if not identifier:
                identifier = ''
            ws.setValue('identifier', identifier)
            ws.beginWriteArray('connections')
            connectionIndex = 0
            if metastep in connectionMap:
                for connectionItem in connectionMap[metastep]:
                    ws.setArrayIndex(connectionIndex)
                    ws.setValue('connectedFromIndex', connectionItem.sourceIndex())
                    ws.setValue('connectedTo', stepList.index(connectionItem.destination()))
                    ws.setValue('connectedToIndex', connectionItem.destinationIndex())
                    ws.setValue('selected', connectionItem.selected())
                    connectionIndex += 1
            ws.endArray()
            nodeIndex += 1
        ws.endArray()
        ws.endGroup()

    def loadState(self, ws):
        self.clear()
        location = self._manager.location()
        ws.beginGroup('nodes')
        nodeCount = ws.beginReadArray('nodelist')
        metaStepList = []
        connections = []
        for i in range(nodeCount):
            ws.setArrayIndex(i)
            name = ws.value('name')
            position = ws.value('position')
            selected = ws.value('selected', 'false') == 'true'
            identifier = ws.value('identifier')
            step = workflowStepFactory(name, location)
            step.registerIdentifierOccursCount(self.identifierOccursCount)
            step.setIdentifier(identifier)
            metastep = MetaStep(step)
            metastep._pos = position
            metastep._selected = selected
            metaStepList.append(metastep)
            self.addItem(metastep)
            # Deserialize after adding the step to the scene, this is so
            # we can validate the step identifier
            step.deserialize(location)
            arcCount = ws.beginReadArray('connections')
            for j in range(arcCount):
                ws.setArrayIndex(j)
                connectedTo = int(ws.value('connectedTo'))
                connectedToIndex = int(ws.value('connectedToIndex'))
                connectedFromIndex = int(ws.value('connectedFromIndex'))
                selected = ws.value('selected', 'false') == 'true'
                connections.append((i, connectedFromIndex, connectedTo, connectedToIndex, selected))
            ws.endArray()
        ws.endArray()
        ws.endGroup()
        for arc in connections:
            node1 = metaStepList[arc[0]]
            node2 = metaStepList[arc[2]]
            c = Connection(node1, arc[1], node2, arc[3])
            c._selected = arc[4]
            self.addItem(c)

    def manager(self):
        return self._manager

    def canExecute(self):
        return self._dependencyGraph.canExecute()

    def execute(self):
        self._dependencyGraph.execute()

    def clear(self):
        self._items.clear()

    def items(self):
        return self._items.keys()

    def addItem(self, item):
        self._items[item] = item

    def removeItem(self, item):
        if item in self._items:
            del self._items[item]

    def setItemPos(self, item, pos):
        if item in self._items:
            self._items[item]._pos = pos

    def setItemSelected(self, item, selected):
        if item in self._items:
            self._items[item]._selected = selected

    def identifierOccursCount(self, identifier):
        '''
        Return the number of times the given identifier occurs in
        all the steps present in the workflow.  The count stops at two
        and returns indicating an excess number of the given identifier.
        An empty identifier will return the value 2 also, this is used
        to signify that the identifier is invalid.
        '''
        if len(identifier) == 0:
            return 2

        identifier_occurrence_count = 0
        for key in self._items:
            item = self._items[key]
            if item.Type == MetaStep.Type and identifier == item.getIdentifier():
                identifier_occurrence_count += 1
                if identifier_occurrence_count > 1:
                    return identifier_occurrence_count

        return identifier_occurrence_count

def reverseDictWithLists(inDict):
    reverseDictOut = {}  # defaultdict(list)
    for k, v in inDict.items():
        for rk in v:
            reverseDictOut[rk] = reverseDictOut.get(rk, [])
            reverseDictOut[rk].append(k)

    return reverseDictOut
