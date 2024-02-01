import copy

from psd2fabric.demo import demo_utils
from psd2fabric.demo.demo_utils import (FINAL_HEIGHT, FINAL_WIDTH, LOGO_BORDER,
                                        TEXT_BORDER)
from psd2fabric.fabric import Fabric
from psd2fabric.fabric.image import ImageFabricLayer
from psd2fabric.render.json_render import dump_json_file


def dump_rule34(fabric: Fabric, psd_file: str, product_img: str):
    tiled_layers = demo_utils.generate_tiled_layers(fabric=fabric)
    all_scale = FINAL_HEIGHT / fabric.height
    rule_layers = []
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
    logo_layer = demo_utils.get_logo_layer(tiled_layer=logo_layer)
    rule3_lagers = copy.deepcopy(rule_layers)
    rule3_lagers.append(
        ImageFabricLayer(
            "产品图",
            int((FINAL_WIDTH - product_width) / 2),
            int((FINAL_HEIGHT - product_height) / 2),
            product_width,
            product_height,
            product_base64,
        )
    )
    if text_layer:
        text_layer.left = FINAL_WIDTH - FINAL_WIDTH / 8 - TEXT_BORDER - text_layer.width
        text_layer.top = TEXT_BORDER
        rule3_lagers.append(text_layer)
    if logo_layer:
        logo_layer.top = LOGO_BORDER
        logo_layer.left = FINAL_WIDTH / 8 + LOGO_BORDER
        rule3_lagers.append(logo_layer)
    final_left = 0
    final_right = FINAL_WIDTH
    rule3_fabric = Fabric(
        demo_utils.filter_on_window_layers(
            ori_layers=rule3_lagers,
            final_left=final_left,
            final_right=final_right,
        ),
        0,
        0,
        FINAL_WIDTH,
        FINAL_HEIGHT,
    )
    rule3_fabric.init_obj()
    dump_file = demo_utils.get_out_put_file_path(
        psd_file=psd_file, out_put_file_name=f"rule3", product_img=product_img
    )
    dump_json_file(rule3_fabric, dump_file)
    rule4_lagers = copy.deepcopy(rule_layers)
    curr_width = fabric.width * all_scale
    start_left = int(curr_width - FINAL_WIDTH)
    rule4_lagers.append(
        ImageFabricLayer(
            "产品图",
            int((FINAL_WIDTH - product_width) / 2 + start_left),
            int((FINAL_HEIGHT - product_height) / 2),
            product_width,
            product_height,
            product_base64,
        )
    )
    if text_layer:
        text_layer.left = int(
            FINAL_WIDTH - FINAL_WIDTH / 8 - TEXT_BORDER - text_layer.width + start_left
        )
        text_layer.top = TEXT_BORDER
        rule4_lagers.append(text_layer)
    if logo_layer:
        logo_layer.top = LOGO_BORDER
        logo_layer.left = FINAL_WIDTH / 8 + LOGO_BORDER + start_left
        rule4_lagers.append(logo_layer)
    final_left = start_left
    final_right = final_left + FINAL_WIDTH
    rule4_fabric = Fabric(
        demo_utils.filter_on_window_layers(
            ori_layers=rule4_lagers,
            final_left=final_left,
            final_right=final_right,
        ),
        start_left,
        0,
        FINAL_WIDTH,
        FINAL_HEIGHT,
    )
    rule4_fabric.init_obj()
    dump_file = demo_utils.get_out_put_file_path(
        psd_file=psd_file, out_put_file_name=f"rule4", product_img=product_img
    )
    dump_json_file(rule4_fabric, dump_file)
