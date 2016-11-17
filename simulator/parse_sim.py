"""Parse a given simulation

Simulations are represented by XML and contain nodes and edges. Not all XML
strings are valid simulations. This module parses a given string of XML and
raises appropriate exceptions if the XML is not a valid simulation.
"""

import xml.etree.ElementTree as ET
import re
import simulator.errors
from simulator.errors import SimParseError


def parse_sim(xml_string):
    """Parse XML representing a simulation"""
    root = None
    try:
        root = ET.fromstring(xml_string)
    except:
        raise SimParseError('Failed to parse XML into simulation.')

    if root.tag != 'mxGraphModel':
        raise SimParseError(
            'Invalid Simulation XML: Root must be <mxGraphModel>')

    '''
    Nodes and Edges are represented as <mxCell> tags and may be wrapped in
    <object> tags which, for nodes, will contain important configuration
    information.

    Bare:
        <mxCell></mxCell>

    Wrapped:
        <object>
            <mxCell></mxCell>
        </object>
    '''
    bare_cells = root.findall('./root/mxCell')
    objects_wrapping_cells = root.findall('./root/object/mxCell/..')

    '''
    Nodes will have a style attribute in their <mxCell> tag which contains a
    key-value pair of 'shape=???'. That shape is our indicator for which type of
    node the <mxCell> represents.

    Edges are also represented by <mxCell> tags but lack the 'shape=???'
    key-value pair in their style attribute.

    There are also a few bare <mxCell>s which are added in automatically by
    mxGraph. We can safely ignore these as they have nothing to do with the
    simulation.
    '''
    edges = {}
    nodes = {}
    # Take not of when we encounter an Exit or Source node as there must be one,
    # and only one, Exit and Source node per simulation.
    node_ids = {
        'source': [],
        'exit': [],
        'process': [],
        'decision': [],
    }
    for cell in bare_cells:
        # Ensure this cell is a edge/node
        if cell.get('style') is not None:
            matches = re.search('shape=([^;]+);', cell.get('style'))
            if matches:
                shape = matches.group(1)
                nodes[cell.get('id')] = {'type': shape}
                node_ids[shape].append(cell.get('id'))
            else:
                edges[cell.get('id')] = {
                    'target': cell.get('target'),
                    'source': cell.get('source')}

    for cell in objects_wrapping_cells:
        child = cell.find('mxCell')
        matches = re.search('shape=([^;]+);', child.get('style'))
        if matches:
            shape = matches.group(1)
            nodes[cell.get('id')] = {'type': shape}
            node_ids[shape].append(cell.get('id'))
            for attrib in cell.keys():
                if attrib not in ['label', 'id']:
                    nodes[cell.get('id')][attrib] = cell.get(attrib)

    for edge_id in edges:
        # Edges must have a source and a target node
        if edges[edge_id]['source'] is None:
            raise SimParseError('All edges must have a source node.')
        elif edges[edge_id]['target'] is None:
            raise SimParseError('All edges must have a target node.')

        edge_source_id = edges[edge_id]['source']
        if 'outbound_edges' in nodes[edge_source_id]:
            nodes[edge_source_id]['outbound_edges'].append(
                edge_id)
        else:
            nodes[edge_source_id]['outbound_edges'] = \
                [edge_id]

    # print('edges', edges)
    # print('nodes', nodes)

    # Sanity tests

    # A simulation must have edges and nodes
    if not edges:
        raise SimParseError('There are no edges.')
    if not nodes:
        raise SimParseError('There are no nodes.')

    # A simulation must have at least one exit
    if len(node_ids['exit']) < 1:
        raise SimParseError('No Exit.')

    # A simulation must have at least one source
    if len(node_ids['source']) < 1:
        raise SimParseError('No Source.')

    for source_id in node_ids['source']:
        # Sources in the simulation must not have more than one outbound edge
        if len(get_outbound_edge_ids(source_id, edges)) > 1:
            raise SimParseError('Source %s has more than one \
                            outbound edge.' % source_id)

        # Sources in the simulation must have at least one outbound edge
        elif len(get_outbound_edge_ids(source_id, edges)) == 0:
            raise SimParseError('Source %s has no outbound \
                            edge.' % source_id)

        # Paths leading away from a Source must all end at an Exit
        elif not paths_all_lead_to_an_exit(source_id, edges, nodes):
            raise SimParseError('Source %s has an outbound edge\
                            which doesn\'t lead to an Exit.' % source_id)

    for exit_id in node_ids['exit']:
        # Sources in the simulation must not have any outbound edges
        if len(get_outbound_edge_ids(exit_id, edges)) > 0:
            raise SimParseError('Exit %s has outbound edge(s)'\
                            % exit_id)

    for process_id in node_ids['process']:
        # Processes in the simulation must have one outbound edge
        if len(get_outbound_edge_ids(process_id, edges)) > 1:
            raise SimParseError('Process %s has outbound \
                            edge(s)' % process_id)

        # Processes in the simulation must have one outbound edge
        if len(get_outbound_edge_ids(process_id, edges)) == 0:
            raise SimParseError('Process %s has no outbound \
                            edge(s)' % process_id)

    for decision_id in node_ids['decision']:
        # Processes in the simulation must have at least one outbound edge
        if len(get_outbound_edge_ids(decision_id, edges)) == 0:
            raise SimParseError('Decision %s has nooutbound \
                            edges' % decision_id)

    return [nodes, edges]


def get_outbound_edge_ids(node_id, edges):
    """Return list of edge ids of outbound edges for a given node_id"""
    outbound_edge_ids = []

    for key in edges:
        if edges[key]['source'] == node_id:
            outbound_edge_ids.append(key)

    return outbound_edge_ids

def get_outbound_edge_target_ids(node_id, edges):
    """Return list of target ids of outbound edges for a given node_id"""
    outbound_edge_target_ids = []

    for key in edges:
        if edges[key]['source'] == node_id:
            outbound_edge_target_ids.append(edges[key]['target'])

    return outbound_edge_target_ids

def search_for_exit(cur_id, nodes_seen, edges, nodes):
    """Recursively traverse the simulation to find an Exit node"""
    if nodes[cur_id]['type'] == 'exit':
        return True

    if cur_id in nodes_seen:
        # Cycle detected
        return False
    else:
        nodes_seen.append(cur_id)

    # TODO: Are there more node types that have multiple outbound edges?
    node_types_that_branch = ['decision', 'spread']
    if nodes[cur_id]['type'] in node_types_that_branch:
        outbound_edge_target_ids = get_outbound_edge_target_ids(cur_id, edges)
        valid_path_found = False
        index = 0
        while index < len(outbound_edge_target_ids) and not valid_path_found:
            target_id = outbound_edge_target_ids[index]
            # Recurse with a cloned copy of nodes_seen so recursive calls don't
            # interfere with each other.
            valid_path_found = search_for_exit(
                target_id, list(nodes_seen), edges, nodes)
            index += 1
        return valid_path_found
    else:
        outbound_edge_target_id = get_outbound_edge_target_ids(
            cur_id, edges)[0]
        return search_for_exit(
            outbound_edge_target_id, nodes_seen, edges, nodes)

def paths_all_lead_to_an_exit(source_id, edges, nodes):
    """Test if all edges branching out from a given source node eventually end
    at an Exit node"""
    return search_for_exit(source_id, [], edges, nodes)
