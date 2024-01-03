import base64
import json
from io import BytesIO
import uuid

from PIL import Image
from psd_tools import PSDImage
from psd_tools.api.layers import AdjustmentLayer, FillLayer


class Layer:
    def __init__(self, name, type, left, top, width, height):
        self.type = type
        self.version = "5.3.0"
        self.originX = "left"
        self.originY = "top"
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.scaleX = 1
        self.scaleY = 1
        self.angle = 0
        self.flipX = False
        self.flipY = False
        self.opacity = 1
        self.visible = True
        self.backgroundColor = ""
        self.skewX = 0
        self.skewY = 0
        self.selectable = True
        self.hasControls = True
        self.id = str(uuid.uuid4())
        self.name = name

class ImageLayer(Layer):
    def __init__(self, name, left, top, width, height, img):
        # 调用父类的构造方法
        super().__init__(name, "image", left, top, width, height)
        self.from_pil(img)

    def from_pil(self, image: Image):
        # 将图像转换为Base64编码
        image_stream = BytesIO()
        image.save(image_stream, format="png")
        self.src = "data:image/png;base64," + base64.b64encode(image_stream.getvalue()).decode('utf-8')


class GroupLayer(Layer):
    def __init__(self, name, left, top, width, height):
        # 调用父类的构造方法
        super().__init__(name, "group", left, top, width, height)
        self.fill = "null"
        self.fillRule = "nonzero"
        self.paintFirst = "fill"
        self.globalCompositeOperation = "source-over"
        self.objects = []

    def add(self, objs: list):
        for obj in objs:
            # print(obj)
            self.objects.append(obj)


class TextLayer(Layer):
    def __init__(self, name, left, top, width, height):
        # 调用父类的构造方法
        super().__init__(name, "i-text", left, top, width, height)
        self.pathAlign = None
        self.pathSide = None
        self.pathStartOffset = None
        self.direction = None
        self.styles = None
        self.charSpacing = None
        self.textBackgroundColor = None
        self.lineHeight = None
        self.fontStyle = None
        self.textAlign = None
        self.linethrough = None
        self.overline = None
        self.underline = None
        self.fontWeight = None
        self.fontSize = None
        self.fontFamily = None

    def set_text(self, font_family, font_size, text):
        self.fontFamily = font_family
        self.fontSize = font_size
        self.text = text
        self.fontWeight = "normal"
        self.underline = False
        self.overline = False
        self.linethrough = False
        self.textAlign = "left"
        self.fontStyle = "normal"
        self.lineHeight = 0.86
        self.textBackgroundColor = ""
        self.charSpacing = 0
        self.styles = []
        self.direction = "ltr"
        self.pathStartOffset = 0
        self.pathSide = "left"
        self.pathAlign = "baseline"


class Fabric:
    def __init__(self, objs, left, top, width, height):
        self.version = "5.3.0"
        self.objects = []
        self.clipPath = {
            "type": "rect",
            "version": "5.3.0",
            "originX": "left",
            "originY": "top",
            "left": left,
            "top": top,
            "width": width,
            "height": height
        }

        workspace = {
            "type": "rect",
            "version": "5.3.0",
            "originX": "left",
            "originY": "top",
            "left": left,
            "top": top,
            "width": width,
            "height": height,
            "fill": "#FC7245",
            "id": "workspace",
            "selectable": False,
            "hasControls": False
        }

        self.objects.append(workspace)
        for obj in objs:
            # print(obj)
            self.objects.append(obj)


def custom_default(obj):
    if isinstance(obj, (Layer, Fabric)):
        return obj.__dict__
    return str(obj)


def dump_json(obj: Fabric):
    # 将 Person 对象转换为 JSON 字符串
    return json.dumps(obj, default=custom_default)


def dump_json_file(obj, file):
    content = dump_json(obj)
    with open(file, 'w') as file:
        # 将字符串写入文件
        file.write(content)


def dump_fabric(objs, left, top, right, bottom, file):
    fb = Fabric(objs, left, top, right - left, bottom - top)
    dump_json_file(fb, file)


def dump_psd(psd_file, dump_file):
    psd = PSDImage.open(psd_file)
    layers = parse_layers(psd._layers, 0, 0)
    viewbox = psd.viewbox
    dump_fabric(layers, viewbox[0], viewbox[1], viewbox[2], viewbox[3], dump_file)


def parse_layers(psd_layers: list, relate_x, relate_y) -> list:
    res = []
    for layer in psd_layers:
        if not layer.visible:
            continue

        # 复杂图,暂时跳过
        if isinstance(layer, AdjustmentLayer) or isinstance(layer, FillLayer):
            continue

        if layer.is_group():
            group = GroupLayer(layer.name, layer.left - relate_x, layer.top - relate_y, layer.width, layer.height)
            # group 内元素(left, top)默认是相对group center的
            children = parse_layers(layer._layers, layer.left + layer.width // 2, layer.top + layer.height // 2)
            group.add(children)
            res.append(group)
            continue

        print(f"==>{layer.layer_id}:{layer.name}:{layer.kind}")

        if layer.kind == 'type':
            text = layer.engine_dict['Editor']['Text'].value
            fontset = layer.resource_dict['FontSet']
            runlength = layer.engine_dict['StyleRun']['RunLengthArray']
            rundata = layer.engine_dict['StyleRun']['RunArray']
            index = 0
            for length, style in zip(runlength, rundata):
                substring = text[index:index + length]
                stylesheet = style['StyleSheet']['StyleSheetData']
                font = fontset[stylesheet['Font']]
                fontSize = stylesheet['FontSize']
                fontName = fontset[stylesheet['Font']]['Name']
                print('%r gets %s' % (substring, font))
                index += length
                break

            tlayer = TextLayer(layer.name, layer.left - relate_x, layer.top - relate_y, layer.width, layer.height)
            tlayer.set_text(fontName, fontSize * 10, text)
            res.append(tlayer)
            continue

        image = layer.composite()
        res.append(ImageLayer(layer.name, layer.left - relate_x, layer.top - relate_y, layer.width, layer.height, image))

    return res