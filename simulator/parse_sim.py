import xml.etree.ElementTree as ET
import re

class SimParseError(Exception):
    """Exception indicating the simulation couldn't be parsed."""
    def __init__(self, message, node_type=None, node_id=None):
        super(SimParseError, self).__init__(message)
        self.message = message
        self.node_type = node_type
        self.node_id = node_id

def parse_sim(xml_string):
    """Parse XML representing a simulation"""
    root = ET.fromstring(xml_string)

    if root.tag != 'mxGraphModel':
        raise Exception('Invalid Simulation XML: Root must be <mxGraphModel>')

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

    # print('edges', edges)
    # print('nodes', nodes)

    # Sanity tests

    # A simulation must have edges and nodes
    if not edges:
        raise Exception('Invalid Simulation: There are no edges.')
    if not nodes:
        raise Exception('Invalid Simulation: There are no nodes.')

    # A simulation must have at least one exit
    if len(node_ids['exit']) < 1:
        raise Exception('Invalid Simulation: No Exit.')

    # A simulation must have at least one source
    if len(node_ids['source']) < 1:
        raise Exception('Invalid Simulation: No Source.')

    for source_id in node_ids['source']:
        # Sources in the simulation must not have more than one outbound edge
        if len(get_outbound_edge_ids(source_id, edges)) > 1:
            raise Exception('Invalid Simulation: Source %s has more than one \
                            outbound edge.' % source_id)

        # Sources in the simulation must have at least one outbound edge
        elif len(get_outbound_edge_ids(source_id, edges)) == 0:
            raise Exception('Invalid Simulation: Source %s has no outbound \
                            edge.' % source_id)

        # Paths leading away from a Source must all end at an Exit
        elif not paths_all_lead_to_an_exit(source_id, edges, nodes):
            raise Exception('Invalid Simulation: Source %s has an outbound edge\
                            which doesn\'t lead to an Exit.' % source_id)

    for exit_id in node_ids['exit']:
        # Sources in the simulation must not have any outbound edges
        if len(get_outbound_edge_ids(exit_id, edges)) > 0:
            raise Exception('Invalid Simulation: Exit %s has outbound edge(s)'\
                            % exit_id)

    for process_id in node_ids['process']:
        # Processes in the simulation must have one outbound edge
        if len(get_outbound_edge_ids(process_id, edges)) > 1:
            raise Exception('Invalid Simulation: Process %s has outbound \
                            edge(s)' % process_id)

        # Processes in the simulation must have one outbound edge
        if len(get_outbound_edge_ids(process_id, edges)) == 0:
            raise Exception('Invalid Simulation: Process %s has no outbound \
                            edge(s)' % process_id)

    for decision_id in node_ids['decision']:
        # Processes in the simulation must have at least one outbound edge
        if len(get_outbound_edge_ids(decision_id, edges)) == 0:
            raise Exception('Invalid Simulation: Decision %s has nooutbound \
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


    """
    # tree = ET.parse('basic_flow.xml')
    # root = tree.getroot()
    root = ET.fromstring(xml_string)

    # Edges collection
    edges = {}
    # Nodes collection
    nodes = {}
    # Source-Edge collection. It looks up the outbound edge from a node
    source_edge = {}
    # Return the edges and nodes as a bundle
    result = {}

    # Collect edges data
    for edges_data in root.iter('mxCell'):
        edge_id = edges_data.get('id')
        source = edges_data.get('source')
        target = edges_data.get('target')
        if source is not None and target is not None:
            edges[edge_id] = {'source': source, 'target': target}
            source_edge[source] = edge_id

    # Collect nodes data
    for object_data in root.iter('object'):
        element_id = object_data.get('id')
        type_template = object_data.get('label')
        delay = object_data.get('Delay')

        if delay is not None:
            delay_data = delay
        else:
            delay_data = 0

        # outbound_edge_id = source_edge[element_id]

        nodes[element_id] = {'type': type_template}

        if type_template == 'Source':
            print('source')
            '''
            # Get next edge_id from the outbound of this Source
            # below the Basic and basic_args are hardcoded in dev
            nodes[element_id] = type_template + \
                '(env, Basic, basic_args, \'' + outbound_edge_id \
                + '\' , ' + delay_data + ')'
            '''
        elif type_template == 'Process':
            print('process')
            '''
            # Get next edge_id from the outbound of this Process
            nodes[element_id] = type_template + \
                '(env, \'' + outbound_edge_id + '\' , ' + delay_data + ')'
            '''

    for exit_data in root.iter('mxCell'):
        element_id = exit_data.get('id')
        value = exit_data.get('value')
        if value is not None:
            nodes[element_id] = {'type': value}

    print(nodes)
    print(edges)

    if not nodes or not edges:
        raise Exception('Missing Nodes or Edges')
    else:
        source_id = 0
        has_source = False
        exit_id = 0
        has_exit = False

        for key, value in nodes.items():
            if value == 'Source':
                if not has_source:
                    source_id = key
                    has_source = True
                if has_source:
                    raise Exception('There should only be one Source')
            if value == 'Exit':
                if not has_exit:
                    exit_id = key
                    has_exit = True
                if has_exit:
                    raise Exception('There should only be one Exit')

        if not has_source:
            raise Exception('Missing Source node')
        if not has_exit:
            raise Exception('Missing Exit node')
        if not assert_path_between(source_id, exit_id, edges):
            raise Exception('Missing path connecting Source and Exit ')

    return [nodes, edges]

def assert_path_between(node_id_a, node_id_b, edges):
    cur_node_id = node_id_a

    while cur_node_id != node_id_b:
        next_node_id = find_next_node(cur_node_id, edges)
        if next_node_id is None:
            return False
        cur_node_id = next_node_id

    return True

def find_next_node(node_id, edges):
    for key, value in edges.items():
        if value['source'] == node_id:
            return value['target']

    return None
    """

