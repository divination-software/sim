import xml.etree.ElementTree as ET

def parse_xml_data(xml_string):
    # tree = ET.parse('basic_flow.xml')
    # root = tree.getroot()
    root = ET.fromstring(xml_string)

    # Edges collection
    EDGES = {}
    # Nodes collection
    NODES = {}
    # Source-Edge collection. It looks up the outbound edge from a node
    SOURCE_EDGE = {}
    # Return the edges and nodes as a bundle
    RESULT = {}

    # Collect edges data
    for edgesData in root.iter('mxCell'):
        edgeId = edgesData.get('id')
        source = edgesData.get('source')
        target = edgesData.get('target')
        if source is not None and target is not None:
            EDGES[edgeId] = { 'source': source, 'target': target }
            SOURCE_EDGE[source] = edgeId
            # print(edgeId, EDGES[edgeId])

    # Collect nodes data
    for objectData in root.iter('object'):
        elementId = objectData.get('id')
        typeTemplate = objectData.get('label')
        delay = objectData.get('Delay')
        if delay is not None:
            delayData = delay;
        else:
            delayData = 0;
        outboundEdgeId = SOURCE_EDGE[elementId];
        if typeTemplate == 'Source':
            # Get next edgeId from the outbound of this Source
            # below the Basic and basic_args are hardcoded in dev
            NODES[elementId] = typeTemplate + '(env, Basic, basic_args, \'' + outboundEdgeId + '\' , ' + delayData + ')'
        elif typeTemplate == 'Process':
            # Get next edgeId from the outbound of this Process
            NODES[elementId] = typeTemplate + '(env, \'' + outboundEdgeId + '\' , ' + delayData + ')'
        # print(elementId, NODES[elementId])

    for exitData in root.iter('mxCell'):
        elementId = exitData.get('id')
        value = exitData.get('value')
        if value is not None:
            NODES[elementId] = value + '(env)';
            # print(elementId, NODES[elementId])

    RESULT['EDGES'] = EDGES
    RESULT['NODES'] = NODES
    # print(RESULT)
    return RESULT

#parse_xml_data('<mxGraphModel dx="880" dy="555" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" background="#ffffff"><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="8" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;exitX=1;exitY=0.5;entryX=0.008;entryY=0.425;entryPerimeter=0;jettySize=auto;orthogonalLoop=1;" edge="1" parent="1" source="6" target="7"><mxGeometry relative="1" as="geometry"/></mxCell><object label="Source" Delay="100" id="6"><mxCell style="shape=source;whiteSpace=wrap;html=1;" vertex="1" parent="1"><mxGeometry x="10" y="10" width="120" height="80" as="geometry"/></mxCell></object><mxCell id="10" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;jettySize=auto;orthogonalLoop=1;" edge="1" parent="1" source="7" target="9"><mxGeometry relative="1" as="geometry"/></mxCell><object label="Process" Delay="30" id="7"><mxCell style="shape=process;whiteSpace=wrap;html=1;" vertex="1" parent="1"><mxGeometry x="290" y="60" width="120" height="80" as="geometry"/></mxCell></object><mxCell id="9" value="Exit" style="shape=exit;whiteSpace=wrap,html=1;" vertex="1" parent="1"><mxGeometry x="540" y="100" width="120" height="80" as="geometry"/></mxCell></root></mxGraphModel>')
