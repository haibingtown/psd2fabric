from psd_tools.api.effects import Stroke
from psd_tools.api.layers import AdjustmentLayer, FillLayer, Layer

from psd2fabric.fabric import Fabric, FabricLayer
from psd2fabric.fabric.group import GroupFabricLayer
from psd2fabric.parser import image_parser, type_parser
from psd2fabric.parser.effects.stroke_parser import stroke_parse


def parse_layers(psd_layers: list, relate_x, relate_y) -> list:
    res = []
    for layer in psd_layers:
        try:
            if not layer.visible:
                continue
            # 复杂图,暂时跳过
            elif isinstance(layer, AdjustmentLayer):
                continue

            if layer.is_group():
                fabric_layer = GroupFabricLayer(
                    layer.name,
                    layer.left - relate_x,
                    layer.top - relate_y,
                    layer.width,
                    layer.height,
                )
                # group 内元素(left, top)默认是相对group center的
                children = parse_layers(
                    layer._layers,
                    layer.left + layer.width // 2,
                    layer.top + layer.height // 2,
                )
                fabric_layer.add(children)
                common_parse(layer, fabric_layer)
            elif layer.kind == "type":

                fabric_layer = type_parser.parse(layer, relate_x, relate_y)
                common_parse(layer, fabric_layer)
            else:
                fabric_layer = image_parser.parse(layer, relate_x, relate_y)

            if fabric_layer:
                print(f"==>{layer.layer_id}:{layer.name}:{layer.kind}")
                res.append(fabric_layer)
        except:
            print("error")

    return res


def psd_to_fabric(psd):
    layers = parse_layers(psd._layers, 0, 0)
    viewbox = psd.viewbox
    fb = Fabric(
        layers, viewbox[0], viewbox[1], viewbox[2] - viewbox[0], viewbox[3] - viewbox[1]
    )
    return fb


def common_parse(layer: Layer, fabric_layer: FabricLayer):
    fabric_layer.opacity = round(layer.opacity / 255, 2)
    # effect parse
    # 仅处理字体类型的effect，其他类型的effect 通过 composite 已经体现在图片上
    if len(layer.effects.items) > 0:
        for effect in layer.effects.items:
            effects_parse(effect, fabric_layer)
    # other parser append here


def effects_parse(effect, fabric_layer: FabricLayer):
    if isinstance(effect, Stroke):
        stroke_parse(effect, fabric_layer)
    # if isinstance(effect, ColorOverlay):
    #     coloroverlay_parse(effect, fabric_layer)
