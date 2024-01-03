from psd_tools.api.layers import AdjustmentLayer, FillLayer

from psd2fabric.fabric import Fabric
from psd2fabric.fabric.group import GroupFabricLayer
from psd2fabric.parser import type_parser, image_parser


def parse_layers(psd_layers: list, relate_x, relate_y) -> list:
    res = []
    for layer in psd_layers:
        if not layer.visible:
            continue

        # 复杂图,暂时跳过
        if isinstance(layer, AdjustmentLayer) or isinstance(layer, FillLayer):
            continue

        if layer.is_group():
            group = GroupFabricLayer(layer.name, layer.left - relate_x, layer.top - relate_y, layer.width, layer.height)
            # group 内元素(left, top)默认是相对group center的
            children = parse_layers(layer._layers, layer.left + layer.width // 2, layer.top + layer.height // 2)
            group.add(children)
            res.append(group)
            continue

        print(f"==>{layer.layer_id}:{layer.name}:{layer.kind}")

        if layer.kind == 'type':
            tlayer = type_parser.parse(layer, relate_x, relate_y)
            res.append(tlayer)
            continue

        ilayer = image_parser.parse(layer, relate_x, relate_y)
        res.append(ilayer)

    return res


def psd_to_fabric(psd):
    layers = parse_layers(psd._layers, 0, 0)
    viewbox = psd.viewbox
    fb = Fabric(layers, viewbox[0], viewbox[1], viewbox[2] - viewbox[0], viewbox[3] - viewbox[1])
    return fb