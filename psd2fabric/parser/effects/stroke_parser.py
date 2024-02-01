from psd_tools.api.effects import Stroke

from psd2fabric.fabric import FabricLayer


#
def stroke_parse(stroke: Stroke, fabric_layer: FabricLayer):
    r = int(stroke.color["Rd  "])
    g = int(stroke.color["Grn "])
    b = int(stroke.color["Bl  "])
    a = int(stroke.opacity)
    fabric_layer.set_stroke(f"rgba({r},{g},{b},{a})", stroke.size)
