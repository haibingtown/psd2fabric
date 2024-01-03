from psd_tools import PSDImage

from psd2fabric.parser.psd_parser import psd_to_fabric
from psd2fabric.render.json_render import dump_json_file


def dump_psd(psd_file, dump_file):
    psd = PSDImage.open(psd_file)
    fabric = psd_to_fabric(psd)
    dump_json_file(fabric,dump_file)




