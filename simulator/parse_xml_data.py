import xml.etree.ElementTree as ET

def parse_simulation_xml(xml_string):
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
            # print(edge_id, edges[edge_id])

    # Collect nodes data
    for object_data in root.iter('object'):
        element_id = object_data.get('id')
        type_template = object_data.get('label')
        delay = object_data.get('Delay')
        if delay is not None:
            delay_data = delay
        else:
            delay_data = 0
        outbound_edge_id = source_edge[element_id]
        if type_template == 'Source':
            # Get next edge_id from the outbound of this Source
            # below the Basic and basic_args are hardcoded in dev
            nodes[element_id] = type_template + \
                '(env, Basic, basic_args, \'' + outbound_edge_id \
                + '\' , ' + delay_data + ')'
        elif type_template == 'Process':
            # Get next edge_id from the outbound of this Process
            nodes[element_id] = type_template + \
                '(env, \'' + outbound_edge_id + '\' , ' + delay_data + ')'
        # print(element_id, nodes[element_id])

    for exit_data in root.iter('mxCell'):
        element_id = exit_data.get('id')
        value = exit_data.get('value')
        if value is not None:
            nodes[element_id] = value + '(env)'
            # print(element_id, nodes[element_id])

    result['edges'] = edges
    result['nodes'] = nodes
    # print(result)
    return result

#parse_xml_data('<mxGraphModel dx="880" dy="555" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" background="#ffffff"><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="8" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;exitX=1;exitY=0.5;entryX=0.008;entryY=0.425;entryPerimeter=0;jettySize=auto;orthogonalLoop=1;" edge="1" parent="1" source="6" target="7"><mxGeometry relative="1" as="geometry"/></mxCell><object label="Source" Delay="100" id="6"><mxCell style="shape=source;whiteSpace=wrap;html=1;" vertex="1" parent="1"><mxGeometry x="10" y="10" width="120" height="80" as="geometry"/></mxCell></object><mxCell id="10" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;jettySize=auto;orthogonalLoop=1;" edge="1" parent="1" source="7" target="9"><mxGeometry relative="1" as="geometry"/></mxCell><object label="Process" Delay="30" id="7"><mxCell style="shape=process;whiteSpace=wrap;html=1;" vertex="1" parent="1"><mxGeometry x="290" y="60" width="120" height="80" as="geometry"/></mxCell></object><mxCell id="9" value="Exit" style="shape=exit;whiteSpace=wrap,html=1;" vertex="1" parent="1"><mxGeometry x="540" y="100" width="120" height="80" as="geometry"/></mxCell></root></mxGraphModel>')
