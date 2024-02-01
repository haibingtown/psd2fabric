import base64
import math
import os
import random
from io import BytesIO

from PIL import Image

from psd2fabric.fabric import Fabric, FabricLayer
from psd2fabric.fabric.group import GroupFabricLayer

FINAL_WIDTH = 1600
FINAL_HEIGHT = 900

LOGO_BORDER = 11
TEXT_BORDER = 40


PSD_DIR = "/Users/sandog/sandog/ai/psd2"
PRODUCT_IMAGE_DIR = "/Users/sandog/sandog/ai/product_img"
OUT_JSON_DIR = "/Users/sandog/sandog/ai/fab_json"

font_array = ["font1", "font2", "font3"]


def from_img_to_base64(ori_img: Image.Image):
    try:
        image_stream = BytesIO()
        ori_img.save(image_stream, format="png")
        return "data:image/png;base64," + base64.b64encode(
            image_stream.getvalue()
        ).decode("utf-8")
    except:
        return None


def get_text_layer(tiled_layers):
    font_map = {}
    max_font_count = 0
    for tiled_layer in tiled_layers:
        if tiled_layer.type == "i-text":
            if font_map.get(str(tiled_layer.fontFamily)) is None:
                font_map.setdefault(str(tiled_layer.fontFamily), 1)
            else:
                font_map.setdefault(
                    str(tiled_layer.fontFamily),
                    font_map.get(str(tiled_layer.fontFamily)) + 1,
                )
            if font_map.get(str(tiled_layer.fontFamily)) > max_font_count:
                max_font_count = font_map.get(str(tiled_layer.fontFamily))
    for key in font_map.keys():
        val = font_map.get(key)
        if val == max_font_count:
            for tiled_layer in tiled_layers:
                if tiled_layer.type == "i-text" and str(tiled_layer.fontFamily) == key:
                    tiled_layer.text = "菜品名称"
                    tiled_layer.name = "菜品名称"
                    tiled_layer.fontFamily = f"'{font_array[random.randint(0, len(font_array) - 1)]}'"
                    tiled_layer.fontSize = 80
                    tiled_layer.width = 320
                    tiled_layer.height = 90
                    tiled_layer.top = -45
                    tiled_layer.left = -160
                    text_layer_group = GroupFabricLayer(
                        "文字图层组", 0, 0, tiled_layer.width, tiled_layer.height
                    )
                    text_layer_group.add([tiled_layer])
                    return text_layer_group


def get_logo_layer(tiled_layer):
    if not tiled_layer:
        return tiled_layer
    logo_scale2 = (
        FINAL_HEIGHT * FINAL_WIDTH * 3 / 50 / tiled_layer.width / tiled_layer.height
    )
    logo_scale = math.sqrt(logo_scale2)
    tiled_layer.scaleX = logo_scale
    tiled_layer.scaleY = logo_scale
    return tiled_layer


def generate_tiled_layers(fabric: Fabric):
    # 打平psd中嵌套的group层级，获得平铺的图层
    product_layers = []
    for ori_obj in fabric.objs:
        generate_tiled_obj(
            rule1_obj=ori_obj,
            product_layers=product_layers,
            parent_left=0,
            parent_top=0,
        )
    return product_layers


def generate_tiled_obj(
    rule1_obj: FabricLayer, product_layers: [], parent_left: int, parent_top: int
):
    if rule1_obj.type == "group":
        group_objs = rule1_obj.objects
        new_group_objs = []
        for group_obj in group_objs:
            group_rule1_obj = generate_tiled_obj(
                rule1_obj=group_obj,
                product_layers=product_layers,
                parent_top=parent_top + rule1_obj.top + (rule1_obj.height / 2),
                parent_left=parent_left + rule1_obj.left + (rule1_obj.width / 2),
            )
            if group_rule1_obj:
                new_group_objs.append(group_rule1_obj)
        rule1_obj.objects = new_group_objs
        return rule1_obj
    else:
        rule1_obj.left = rule1_obj.left + parent_left
        rule1_obj.top = rule1_obj.top + parent_top
        product_layers.append(rule1_obj)


def generate_base64_from_image_and_area(product_img: str, area: int):
    logo_pic = Image.open(product_img)
    logo_pic = logo_pic.crop(logo_pic.getbbox())
    product_scale = math.sqrt(area / logo_pic.width / logo_pic.height)
    new_width, new_height = int(logo_pic.width * product_scale), int(
        logo_pic.height * product_scale
    )
    resized_image = logo_pic.resize((new_width, new_height), Image.LANCZOS)
    return from_img_to_base64(resized_image), new_width, new_height


def get_out_put_file_path(psd_file: str, product_img: str, out_put_file_name: str):
    if not os.path.exists(OUT_JSON_DIR):
        os.mkdir(OUT_JSON_DIR)
    psd_file_paths = psd_file.split("/")
    psd_file_name = psd_file_paths[len(psd_file_paths) - 1].replace(".psd", "")
    product_img_paths = product_img.split("/")
    product_img_file_name = product_img_paths[len(product_img_paths) - 1]
    product_img_paths = product_img_file_name.split(".")
    product_img_file_name = product_img_paths[0]
    psd_dir_path = f"{OUT_JSON_DIR}/{psd_file_name}"
    if not os.path.exists(psd_dir_path):
        os.mkdir(psd_dir_path)
    dir_path = f"{psd_dir_path}/{product_img_file_name}"
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    if not out_put_file_name.endswith(".json"):
        out_put_file_name = f"{out_put_file_name}.json"
    return f"{dir_path}/{out_put_file_name}"


def filter_on_window_layers(ori_layers: [], final_left: int, final_right: int):
    return [
        curr_rule_layer
        for curr_rule_layer in ori_layers
        if (final_left <= curr_rule_layer.left <= final_right)
        or (final_left <= curr_rule_layer.left + curr_rule_layer.width <= final_right)
        or (
            final_left >= curr_rule_layer.left
            and final_right <= curr_rule_layer.left + curr_rule_layer.width
        )
    ]
