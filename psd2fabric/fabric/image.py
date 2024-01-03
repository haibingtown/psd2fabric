from psd2fabric.fabric import FabricLayer


class ImageFabricLayer(FabricLayer):
    def __init__(self, name, left, top, width, height, img):
        # 调用父类的构造方法
        super().__init__(name, "image", left, top, width, height)
        self.src = None
        self.set_image(img)

    def set_image(self, src: str):
        # 将图像转换为Base64编码
        self.src = src
