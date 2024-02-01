from psd2fabric.fabric import FabricLayer


class GroupFabricLayer(FabricLayer):
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
            self.objects.append(obj)
