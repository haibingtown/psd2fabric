import copy
import os
import random

from psd_tools import PSDImage

from psd2fabric.demo import demo_utils
from psd2fabric.demo.demo_utils import PRODUCT_IMAGE_DIR, PSD_DIR
from psd2fabric.demo.rule1_exce import dump_rule1
from psd2fabric.demo.rule5_exce import dump_rule5
from psd2fabric.demo.rule34_exce import dump_rule34
from psd2fabric.parser.psd_parser import psd_to_fabric
from psd2fabric.render.json_render import dump_json_file


def dump_psd():
    psd_file = "/Users/sandog/sandog/ai/psd/丰玥小笼-特批套餐图.psd"
    dump_file = "/Users/sandog/sandog/ai/fab_json/丰玥小笼-特批套餐图.json"
    psd = PSDImage.open(psd_file)
    fabric = psd_to_fabric(psd)
    # fabric.objs = demo_utils.generate_tiled_layers(fabric=fabric)
    fabric.init_obj()
    dump_json_file(fabric, dump_file)


def exce_demo(psd_file: str, product_img: str):
    psd = PSDImage.open(psd_file)
    main_fabric = psd_to_fabric(psd)
    dump_rule1(
        fabric=copy.deepcopy(main_fabric), psd_file=psd_file, product_img=product_img
    )
    dump_rule34(
        fabric=copy.deepcopy(main_fabric), psd_file=psd_file, product_img=product_img
    )
    dump_rule5(
        fabric=copy.deepcopy(main_fabric), psd_file=psd_file, product_img=product_img
    )


if __name__ == "__main__":
    psd_files = os.listdir(PSD_DIR)
    product_imgs = os.listdir(PRODUCT_IMAGE_DIR)
    for psd_file in psd_files:
        if psd_file.endswith(".psd"):
            for product_img in product_imgs:
                if (
                    product_img.endswith(".png")
                    or product_img.endswith(".jpeg")
                    or product_img.endswith(".jpg")
                ):
                    exce_demo(
                        psd_file=f"{PSD_DIR}/{psd_file}",
                        product_img=f"{PRODUCT_IMAGE_DIR}/{product_img}",
                    )
