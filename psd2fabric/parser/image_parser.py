import base64
from io import BytesIO

from psd_tools.api.layers import Layer

from psd2fabric.fabric.image import ImageFabricLayer


def parse(layer: Layer, relate_x, relate_y):
    try:
        image = layer.composite()
        # image -> base64
        image_stream = BytesIO()
        image.save(image_stream, format="png")
        src = "data:image/png;base64," + base64.b64encode(
            image_stream.getvalue()
        ).decode("utf-8")
        # src = "xxx"
    except:
        return None
    return ImageFabricLayer(
        layer.name,
        layer.left - relate_x,
        layer.top - relate_y,
        layer.width,
        layer.height,
        src,
    )
