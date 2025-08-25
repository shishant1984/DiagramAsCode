import xml.etree.ElementTree as ET
import yaml
import html

# Import YAML
with open("network_repo.yaml", "r") as f:
    network_data = yaml.safe_load(f)

# List of stencils icons
cisco_styles = {
    "router": "sketch=0;points=[[0.5,0,0],[1,0.5,0],[0.5,1,0],[0,0.5,0],[0.145,0.145,0],[0.8555,0.145,0],[0.855,0.8555,0],[0.145,0.855,0]];verticalLabelPosition=bottom;html=1;verticalAlign=top;aspect=fixed;align=center;pointerEvents=1;shape=mxgraph.cisco19.rect;prIcon=router;fillColor=#FAFAFA;strokeColor=#005073;",
    "switch": "sketch=0;points=[[0.015,0.015,0],[0.985,0.015,0],[0.985,0.985,0],[0.015,0.985,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];verticalLabelPosition=bottom;html=1;verticalAlign=top;aspect=fixed;align=center;pointerEvents=1;shape=mxgraph.cisco19.rect;prIcon=nexus_9300;fillColor=#FAFAFA;strokeColor=#005073;",
    "firewall": "image;html=1;image=img/lib/clip_art/networking/Firewall_02_128x128.png",
    "ISP": "ellipse;shape=cloud;whiteSpace=wrap;",
    "sdwan": "shape=mxgraph.cisco.routers.router;sketch=0;html=1;pointerEvents=1;dashed=0;fillColor=#036897;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;align=center;outlineConnect=0;"
}
# Set up page of drawio
root = ET.Element("mxfile", host="app.diagrams.net")
diagram = ET.SubElement(root, "diagram", name="Network Diagram")
graph = ET.SubElement(diagram, "mxGraphModel")
root_cell = ET.SubElement(graph, "root")

ET.SubElement(root_cell, "mxCell", id="0")
ET.SubElement(root_cell, "mxCell", id="1", parent="0")

# Add devices
gap=100
for device in network_data["devices"]:
    style = cisco_styles.get(device["type"], "shape=rectangle;")
    cell = ET.SubElement(root_cell, "mxCell",
                         id=device["id"],
                         value=device.get("label", device["id"]),
                         style= style ,
                         vertex="1",
                         parent="1",
                         )
    geom = ET.SubElement(cell, "mxGeometry",
                         x="200", y="200",
                         width="80", height="80")
    geom.set("as", "geometry")

# Add links
for i, link in enumerate(network_data["links"], start=100):
    port_label = f"{link['src_port']} {link['dst_port']}" 
    if link.get("label"):
        port_label = port_label + f" {link['label']}"


    color = link.get("color","#000000")
    cell = ET.SubElement(root_cell, "mxCell",
                         id=str(i),
                         value=port_label,
                         edge="1",
                         parent="1",
                         source=link["src"],
                         target=link["dst"],
                         style=f"edgeStyle=orthogonalEdgeStyle,endArrow=none;startArrow=none;strokeColor={color};noEdgeStyle=1;orthogonal=1;endArrow=none;endFill=0;strokeWidth=3;rounded=0;curved=0;shape=wire;dashed=1;fontSize=8")
    geom = ET.SubElement(cell, "mxGeometry", relative="1")
    geom.set("as", "geometry")
    print (port_label)


tree = ET.ElementTree(root)
with open("network_diagram.drawio", "wb") as f:
    tree.write(f, encoding="utf-8", xml_declaration=True)