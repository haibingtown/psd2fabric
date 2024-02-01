import uuid


class FabricLayer:
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

    def set_stroke(self, color, size):
        self.stroke = color
        self.strokeWidth = size


class Fabric:
    def __init__(self, objs, left, top, width, height):
        self.objects = []
        self.version = "5.3.0"
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.objs = objs
        self.clipPath = {
            "type": "rect",
            "version": "5.3.0",
            "originX": "left",
            "originY": "top",
            "left": left,
            "top": top,
            "width": width,
            "height": height,
        }

    def init_obj(self):
        self.objects = []
        workspace = {
            "type": "rect",
            "version": "5.3.0",
            "originX": "left",
            "originY": "top",
            "left": self.left,
            "top": self.top,
            "width": self.width,
            "height": self.height,
            "fill": "#FC7245",
            "id": "workspace",
            "selectable": False,
            "hasControls": False,
        }
        self.objects.append(workspace)
        for obj in self.objs:
            self.objects.append(obj)
        self.objs = None
