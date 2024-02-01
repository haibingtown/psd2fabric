from psd_tools.api.effects import ColorOverlay

from psd2fabric.fabric import FabricLayer


def coloroverlay_parse(coloroverlay: ColorOverlay, fabric_layer: FabricLayer):
    fabric_layer.opacity = round(coloroverlay.opacity / 100, 2)
    # if not fabric_layer.filters:
    #     fabric_layer.filters = []
    #
    # fabric_layer.append("{}")
