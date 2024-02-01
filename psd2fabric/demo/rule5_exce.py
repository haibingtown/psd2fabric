import math

from PIL import Image

from psd2fabric.demo import demo_utils
from psd2fabric.demo.demo_utils import (FINAL_HEIGHT, FINAL_WIDTH, LOGO_BORDER,
                                        TEXT_BORDER)
from psd2fabric.fabric import Fabric
from psd2fabric.fabric.image import ImageFabricLayer
from psd2fabric.render.json_render import dump_json_file


def dump_rule5(fabric: Fabric, psd_file: str, product_img: str):
    tiled_layers = demo_utils.generate_tiled_layers(fabric=fabric)
    rule5_objs = []
    resize_img = generate_resize_img(product_img=product_img)
    resize_img_base64 = demo_utils.from_img_to_base64(ori_img=resize_img)
    rule5_objs.append(
        ImageFabricLayer("产品图", 0, 0, FINAL_WIDTH, FINAL_HEIGHT, resize_img_base64)
    )
    for tiled_layer in tiled_layers:
        if tiled_layer.name.startswith("logo"):
            tiled_layer.left = FINAL_WIDTH / 8 + LOGO_BORDER
            tiled_layer.top = LOGO_BORDER
            logo_scale2 = (
                FINAL_HEIGHT
                * FINAL_WIDTH
                * 9
                / 80
                / tiled_layer.width
                / tiled_layer.height
            )
            logo_scale = math.sqrt(logo_scale2)
            tiled_layer.scaleX = logo_scale
            tiled_layer.scaleY = logo_scale
            rule5_objs.append(tiled_layer)
    text_layer = demo_utils.get_text_layer(tiled_layers=tiled_layers)
    if text_layer:
        text_layer.left = FINAL_WIDTH - FINAL_WIDTH / 8 - TEXT_BORDER - text_layer.width
        text_layer.top = TEXT_BORDER
        rule5_objs.append(text_layer)
    rule_fabric = Fabric(
        rule5_objs,
        0,
        0,
        FINAL_WIDTH,
        FINAL_HEIGHT,
    )
    dump_file = demo_utils.get_out_put_file_path(
        psd_file=psd_file, out_put_file_name=f"rule5", product_img=product_img
    )
    rule_fabric.init_obj()
    dump_json_file(rule_fabric, dump_file)


def generate_resize_img(product_img: str):
    logo_pic = Image.open(product_img)
    logo_pic = logo_pic.crop(logo_pic.getbbox())
    new_width = FINAL_WIDTH
    new_height = FINAL_HEIGHT
    if logo_pic.width / logo_pic.height > 16 / 9:
        new_width = new_height * logo_pic.width / logo_pic.height
        bottom = 0
        top = new_height
        left = (new_width - FINAL_WIDTH) / 2
        right = new_width - left
    else:
        new_height = new_width * logo_pic.height / logo_pic.width
        left = 0
        right = new_width
        bottom = (new_height - FINAL_HEIGHT) / 2
        top = new_height - bottom
    resized_image = logo_pic.resize((int(new_width), int(new_height)), Image.LANCZOS)
    return resized_image.crop((int(left), int(bottom), int(right), int(top)))
