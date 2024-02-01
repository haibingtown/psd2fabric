import copy

from psd2fabric.demo import demo_utils
from psd2fabric.demo.demo_utils import (FINAL_HEIGHT, FINAL_WIDTH, LOGO_BORDER,
                                        TEXT_BORDER)
from psd2fabric.fabric import Fabric
from psd2fabric.fabric.image import ImageFabricLayer
from psd2fabric.render.json_render import dump_json_file


def dump_rule1(fabric: Fabric, psd_file: str, product_img: str):
    tiled_layers = demo_utils.generate_tiled_layers(fabric=fabric)
    all_scale = FINAL_HEIGHT / fabric.height
    sum_width = int(fabric.width * all_scale)
    rule_layers = []
    ori_product_layers = []
    logo_layer = None
    for tiled_layer in tiled_layers:
        if (
            tiled_layer.type == "image"
            and not tiled_layer.name.startswith("产品")
            and not tiled_layer.name.startswith("logo")
        ):
            tiled_layer.scaleX = all_scale
            tiled_layer.scaleY = all_scale
            tiled_layer.top = int(all_scale * tiled_layer.top)
            tiled_layer.left = int(all_scale * tiled_layer.left)
            rule_layers.append(tiled_layer)
        elif tiled_layer.name.startswith("产品"):
            ori_product_layers.append(tiled_layer)
        elif tiled_layer.name.startswith("logo"):
            logo_layer = tiled_layer
    (
        product_base64,
        product_width,
        product_height,
    ) = demo_utils.generate_base64_from_image_and_area(
        product_img=product_img, area=int(FINAL_HEIGHT * FINAL_WIDTH * 3 / 4 * 0.6)
    )
    text_layer = demo_utils.get_text_layer(tiled_layers=tiled_layers)
    logo_layer = demo_utils.get_logo_layer(logo_layer)
    if len(ori_product_layers) > 0:
        index = 0
        for ori_product_layer in ori_product_layers:
            curr_rule_layers = copy.deepcopy(rule_layers)
            ori_center_x = int(
                (ori_product_layer.left + ori_product_layer.width / 2) * all_scale
            )
            ori_center_y = int(
                (ori_product_layer.top + ori_product_layer.height / 2) * all_scale
            )
            curr_product_left = int(ori_center_x - product_width / 2)
            curr_product_top = int(ori_center_y - product_height / 2)
            curr_rule_layers.append(
                ImageFabricLayer(
                    "产品图",
                    curr_product_left,
                    curr_product_top,
                    product_width,
                    product_height,
                    product_base64,
                )
            )
            final_left = ori_center_x - FINAL_WIDTH / 2
            final_left = final_left if final_left > 0 else 0
            final_left = (
                final_left
                if final_left + FINAL_WIDTH < sum_width
                else sum_width - FINAL_WIDTH
            )
            if text_layer:
                text_layer.left = (
                    FINAL_WIDTH
                    - FINAL_WIDTH / 8
                    - TEXT_BORDER
                    - text_layer.width
                    + final_left
                )
                text_layer.top = TEXT_BORDER
                curr_rule_layers.append(text_layer)
            if logo_layer:
                logo_layer.top = LOGO_BORDER
                logo_layer.left = FINAL_WIDTH / 8 + LOGO_BORDER + final_left
                curr_rule_layers.append(logo_layer)
            final_right = final_left + FINAL_WIDTH
            curr_fabric = Fabric(
                demo_utils.filter_on_window_layers(
                    ori_layers=curr_rule_layers,
                    final_left=final_left,
                    final_right=final_right,
                ),
                final_left,
                0,
                FINAL_WIDTH,
                FINAL_HEIGHT,
            )
            curr_fabric.init_obj()
            dump_file = demo_utils.get_out_put_file_path(
                psd_file=psd_file,
                out_put_file_name=f"rule1-{index}",
                product_img=product_img,
            )
            dump_json_file(curr_fabric, dump_file)
            index = index + 1
