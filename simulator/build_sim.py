"""Parse a given simulation

Simulations are represented by XML and contain nodes and edges. Not all XML
strings are valid simulations. This module parses a given string of XML and
raises appropriate exceptions if the XML is not a valid simulation.
"""

import xml.etree.ElementTree as ET
import re
from simulator.errors import SimBuildError

def parse_xml(xml_string):
    """Attempt to parse the given XML."""
    root = None
    try:
        root = ET.fromstring(xml_string)
    except:
        raise SimBuildError('Failed to parse XML into simulation.')

    return root

def test_xml(root):
    """Perform basic tests on the parsed XML to ensure it adheres to expected
    template."""
    if root.tag != 'mxGraphModel':
        raise SimBuildError('Root must be <mxGraphModel>')

def parse_metadata(metadata_object):
    """Parse metadata information from the wrapper object"""
    metadata = None
    if metadata_object is not None:
        metadata = {}
        metadata_type = metadata_object.get('type')
        delay_type = metadata_object.get('delayType')
        min_value = metadata_object.get('min')
        mid_value = metadata_object.get('mid')
        max_value = metadata_object.get('max')
        val_value = metadata_object.get('val')
        decision_value = metadata_object.get('decision')
        node_type = metadata_object.get('nodeType')
        resource_type = metadata_object.get('resource')

        if metadata_type is not None:
            metadata[metadata_type] = {}

        if delay_type is not None:
            metadata[metadata_type]['type'] = delay_type

        if decision_value is not None:
            metadata['decision'] = decision_value

        if node_type is not None and node_type == 'resource':
            resource_name = metadata_object.get('Name')
            resource_count = metadata_object.get('Count')
            metadata = {'name': resource_name,
                        'count': resource_count}

        if (delay_type is not None or
                min_value is not None or
                mid_value is not None or
                max_value is not None or
                val_value is not None or
                resource_type is not None):
            metadata[metadata_type]['args'] = {}

        if min_value is not None:
            metadata[metadata_type]['args']['min'] = min_value

        if mid_value is not None:
            metadata[metadata_type]['args']['mid'] = mid_value

        if max_value is not None:
            metadata[metadata_type]['args']['max'] = max_value

        if val_value is not None:
            metadata[metadata_type]['args']['val'] = val_value

        if resource_type is not None:
            metadata[metadata_type]['args']['resource'] = resource_type

    return metadata

def parse_sim(xml_string):
    """Parse XML representing a simulation.

    Each node has different arguments which are required for its construction.
    All arguments must be supplied as JSON-stringified strings.

    Nodes
    -----

    Format:
        <Node Type>
            <Key> (<Required?>): <Type>
                <Description>
                <Example of properly-formatted argument>

        Keys are case insensitive.

    Source:
        Delay (required): (see Delay)
            The amount of time between entity births.

            Ex: (see Delay)

    Exit:
        None

    Process:
        WillDelay (required): Boolean
            Will the process force entities to delay before proceeding?

            Ex: true || false

        Delay (required if WillDelay is true): (see Delay)
            Time between entity births

            Ex: (see Delay)

        WillRelease (required): Boolean
            Will the process force entities to release one or more resources, if
            the entity has any of those resources, before proceeding?

            Ex: true || false

        ToBeReleased (required if WillRelease is true): Object
            The resources and amounts of each to be released by each entity.
            Keys in the object are resource ids. Entities which don't possess
            the resource(s) specified will pass through without error.

            Currently supports releasing up to one of each type of available
            resource for each entity.

            Ex: {
                "cashier": 1,
                "pen": 1,
            }

        MustSeize (required if MaySeize is not present): JSON Stringified boolean
            Will the process force entities to seize one or more resources
            before proceeding? Entities will not proceed until they successfully
            seize the specified resource(s).

            Ex: true || false

        MaySeize (required if MustSeize is not present): JSON Stringified boolean
            Will the process have entities attempt to seize one or more
            resources before proceeding? Entities will proceed regardless of
            whether or not they obtain the resource(s).

            Ex: true || false

        ToBeSeized (required if May/MustSeize is true): JSON Stringified object
            The resources and amounts of each to be seized by each entity. Keys
            in the object are resource ids.

            Currently supports seizing up to one of each type of available
            resource for each entity.

            Ex: {
                "cashier": 1,
                "pen": 1,
            }

    Decision:
        Condition (required): (see Condition)
            Branching condition for the decision. The entity will proceed along
            the top branch if the condition resolves as true. It will continue
            along the bottom branch if the condition resolves as false.

            Ex: (see Condition)

    Spread:
        ProbabilityDistribution (required): JSON Stringified array
            The probability of taking each branch available from the Spread, in
            order from top-to-bottom.

            Each probability is represented as an integer less than 100. These
            integers must sum to 100.

            Ex: [10, 30, 45, 15]

    Modify:
        Undocumented. Not implemented yet.

    Spread:
        Undocumented. Not implemented yet.

    Other
    -----

    Format:
        <Key> (<Required?>): <Type>
            <Description>

            <Nested Key> (<Required?>): <Type>
                <Description>

            <Example of properly-formatted arguments>

        Keys are case insensitive.

    Delay (see node for requirements): JSON Stringified object
        A pair of key-values which identify which delay to use, and which
        arguments to pass to it.

        Type (required): String
            Specify the type of delay to be applied. Must be one of the
            following strings:
                Constant: A constant delay
                Triangle: A random delay based on a triangular distribution

        Args (required): Object
            Arguments for the delay. Each type of delay has its own required
            arguments.

            Constant:
                Length (required): Integer
                    The length of the delay as a constant integer.

            Triangle:
                Min (required): Integer
                    The minimum delay length

                Avg (required): Integer
                    The average delay length. Must be greater than or equal to
                    the minimum.

                Max (required): Integer
                    The maximum delay length. Must be greater than or equal to
                    the average.

        Ex: Constant
            {
                "type": "constant",
                "args": {
                    "length": 40,
                }
            }

        Ex: Triangle
            {
                "type": "triangle",
                "args": {
                    "min": 10,
                    "avg": 20,
                    "max": 30,
                }
            }

    Condition (see node for requrements): JSON Stringified object
        A pair of key-values which identify which condition to use, and which
        arguments to pass to it.

        Type (required): String
            Specify the type of condition to be applied. Must be one of the
            following strings:
                HasResource: Does the entity possess a resource?

        Args (required): Object
            Arguments for the condition. Each type of condition has its own
            required arguments.

            HasResource:
                Resource (required): String
                    The type of resource to test the entity for.

                Amount (required): Integer
                    The amount of the resource to test the entity for.

                Comparator (required): String
                    The method of comparison to use when testing the entity.
                    Must be one of:
                        "eq": Equal (==)
                        "lt": Less than (<)
                        "lteq": Less than or equal to (<=)
                        "gt": Greater than (>)
                        "gteq": Greater than or equal to(>=)

        Ex: HasResource
            {
                "type": "hasresource",
                "args": {
                    "resource": "cashier",
                    "amount": 1,
                    "comparator": "gt",
                }
            }

    """

    root = parse_xml(xml_string)
    test_xml(root)

    # Nodes and Edges are represented as <mxCell> tags and may be wrapped in
    # <object> tags which, for nodes, will contain important configuration
    # information.
    #
    # Bare:
    #   <mxCell></mxCell>
    #
    # Wrapped:
    #   <object>
    #       <mxCell></mxCell>
    #   </object>
    bare_cells = root.findall('./root/mxCell')
    wrapper_objects = root.findall('./root/object')

    # Nodes will have a style attribute in their <mxCell> tag which contains a
    # key-value pair of 'shape=?'. That shape is our indicator for which type of
    # node the <mxCell> represents.
    #
    # Edges are also represented by <mxCell> tags but lack the 'shape=?'
    # key-value pair in their style attribute.
    #
    # There are also a few bare <mxCell>s which are added in automatically by
    # mxGraph. We can safely ignore these as they have nothing to do with the
    # simulation.
    #
    # Resources dictionary contains a collection of resources
    #
    edges = {}
    nodes = {}
    node_ids = {}
    resources = {}

    for cell in bare_cells:
        # Ensure this cell is a edge/node
        if cell.get('style') is not None:
            matches = re.search('shape=([^;]+);', cell.get('style'))
            if matches:
                shape = matches.group(1)
                nodes[cell.get('id')] = {'type': shape}

                if shape not in node_ids:
                    node_ids[shape] = []
                node_ids[shape].append(cell.get('id'))
            else:
                edges[cell.get('id')] = {
                    'target': cell.get('target'),
                    'source': cell.get('source')}

    for wrapper_object in wrapper_objects:
        cell = wrapper_object.find('mxCell')
        metadata = parse_metadata(wrapper_object)
        wrapper_object_id = wrapper_object.get('id')
        matches = re.search('shape=([^;]+);', cell.get('style'))
        if matches:
            shape = matches.group(1)
            node_type = wrapper_object.get('nodeType')
            # Get resource object
            if node_type == 'resource':
                resources[wrapper_object_id] = {'type': node_type}
                if metadata is not None:
                    resources[wrapper_object_id].update(metadata)
            else: # just other shape object
                if metadata is not None:
                    nodes[wrapper_object_id] = {'type': shape,
                                                'metadata': metadata}
                else:
                    nodes[wrapper_object_id] = {'type': shape}

                if shape not in node_ids:
                    node_ids[shape] = []
                node_ids[shape].append(wrapper_object_id)

            # for attrib in wrapper_object.keys():
            #     if attrib not in ['label', 'id']:
            #         nodes[wrapper_object.get('id')][attrib] = \
            #           wrapper_object.get(attrib)

            # if nodes:
            #     object_id = wrapper_object_id
            #     if object_id in nodes:
            #         print(nodes[wrapper_object_id])

            # if resources:
            #     resource_id = wrapper_object_id
            #     if resource_id in resources:
            #         print(resources[resource_id])

    for edge_id in edges:
        # Edges must have a source and a target node
        if edges[edge_id]['source'] is None:
            raise SimBuildError('All edges must have a source node.')
        elif edges[edge_id]['target'] is None:
            raise SimBuildError('All edges must have a target node.')

        edge_source_id = edges[edge_id]['source']
        if 'outbound_edges' in nodes[edge_source_id]:
            nodes[edge_source_id]['outbound_edges'].append(
                edge_id)
        else:
            nodes[edge_source_id]['outbound_edges'] = \
                [edge_id]

    return [nodes, node_ids, edges, resources]

def test_sim_sources(nodes, edges, source_node_ids):
    """Test all Sources in the simulation

    Tests:
        - Sources must have exactly one outbound edge.
        - Paths leading out from a Source must end at an Exit.
    """
    for source_id in source_node_ids:
        # Sources in the simulation must not have more than one outbound edge
        if len(get_outbound_edge_ids(source_id, edges)) > 1:
            raise SimBuildError('Source %s has more than one \
                            outbound edge.' % source_id)

        # Sources in the simulation must have at least one outbound edge
        elif len(get_outbound_edge_ids(source_id, edges)) == 0:
            raise SimBuildError('Source %s has no outbound \
                            edge.' % source_id)

        # Paths leading away from a Source must all end at an Exit
        elif not paths_all_lead_to_an_exit(source_id, edges, nodes):
            raise SimBuildError('Source %s has an outbound edge\
                            which doesn\'t lead to an Exit.' % source_id)

def test_sim_exits(nodes, edges, exit_node_ids):
    """Test all Exits in the simulation

    Tests:
        - Exits cannot have any outbound edges.
    """
    for exit_id in exit_node_ids:
        # Sources in the simulation must not have any outbound edges
        if len(get_outbound_edge_ids(exit_id, edges)) > 0:
            raise SimBuildError('Exit %s has outbound edge(s)'\
                            % exit_id)

def test_sim_processes(nodes, edges, process_node_ids):
    """Test all Processes in the simulation

    Tests:
        - Processes must have exactly one outbound edge
    """
    for process_id in process_node_ids:
        # Processes in the simulation must have one outbound edge
        if len(get_outbound_edge_ids(process_id, edges)) > 1:
            raise SimBuildError('Process %s has outbound \
                            edge(s)' % process_id)

        # Processes in the simulation must have one outbound edge
        if len(get_outbound_edge_ids(process_id, edges)) == 0:
            raise SimBuildError('Process %s has no outbound \
                            edge(s)' % process_id)


def test_sim_decisions(nodes, edges, decision_node_ids):
    """Test all Decisions in the simulation

    Tests:
        - Decisions must have at least one outbound edge.
    """
    for decision_id in decision_node_ids:
        # Processes in the simulation must have at least one outbound edge
        if len(get_outbound_edge_ids(decision_id, edges)) == 0:
            raise SimBuildError('Decision %s has no outbound \
                            edges' % decision_id)

def test_sim(nodes, node_ids, edges):
    """Assert that the parsed simulation is valid."""

    # A simulation must have edges and nodes
    if not edges:
        raise SimBuildError('There are no edges.')
    if not nodes:
        raise SimBuildError('There are no nodes.')

    # A simulation must have at least one exit
    if len(node_ids['exit']) < 1:
        raise SimBuildError('No Exit.')

    # A simulation must have at least one source
    if len(node_ids['source']) < 1:
        raise SimBuildError('No Source.')

    # Required nodes
    test_sim_sources(nodes, edges, node_ids['source'])
    test_sim_exits(nodes, edges, node_ids['exit'])

    # Optional nodes
    if 'process' in node_ids:
        test_sim_processes(nodes, edges, node_ids['process'])
    if 'decision' in node_ids:
        test_sim_decisions(nodes, edges, node_ids['decision'])

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

def build_sim(xml_string):
    """Build a representation of a given simulation which can be run in
    SimPy."""
    nodes, node_ids, edges, resources = parse_sim(xml_string)
    test_sim(nodes, node_ids, edges)
    return [nodes, edges, resources]
