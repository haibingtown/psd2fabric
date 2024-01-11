import colorsys
from colorsys import hsv_to_rgb

from psd_tools.api.layers import TypeLayer

from psd2fabric.fabric.text import TextFabricLayer


def parse(layer: TypeLayer, relate_x, relate_y):
    text = layer.engine_dict['Editor']['Text'].value
    fontset = layer.resource_dict['FontSet']
    styleSheetSet = layer.resource_dict['StyleSheetSet']
    runlength = layer.engine_dict['StyleRun']['RunLengthArray']
    rundata = layer.engine_dict['StyleRun']['RunArray']
    index = 0
    for length, style in zip(runlength, rundata):
        substring = text[index:index + length]
        stylesheet = style['StyleSheet']['StyleSheetData']
        if 'Font' in stylesheet:
            fontType = stylesheet['Font']
        else:
            fontType = styleSheetSet[index]['StyleSheetData']['Font']

        font_size = stylesheet['FontSize']
        font_size = round(get_size(font_size, layer.transform), 2)
        font_name = fontset[fontType]['Name']
        font_color = get_color(stylesheet['FillColor']['Values'])

        print(f"{font_name}:{font_size}:{font_color}")
        index += length
        break

    tlayer = TextFabricLayer(layer.name, layer.left - relate_x, layer.top - relate_y, layer.width, layer.height)
    tlayer.set_text(font_name, font_size, font_color, text)
    return tlayer


def get_color(color):
    rgba_values = [round(c * 255, 0) for c in color]
    return f"rgba({','.join(map(str, rgba_values[1:]))},{rgba_values[0]})"


def get_size(font_size, transform):
    return font_size * transform[0]