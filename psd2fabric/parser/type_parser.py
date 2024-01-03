from psd_tools.api.layers import TypeLayer

from psd2fabric.fabric.text import TextFabricLayer


def parse(layer: TypeLayer, relate_x, relate_y):
    text = layer.engine_dict['Editor']['Text'].value
    fontset = layer.resource_dict['FontSet']
    runlength = layer.engine_dict['StyleRun']['RunLengthArray']
    rundata = layer.engine_dict['StyleRun']['RunArray']
    index = 0
    for length, style in zip(runlength, rundata):
        substring = text[index:index + length]
        stylesheet = style['StyleSheet']['StyleSheetData']
        font = fontset[stylesheet['Font']]
        fontSize = stylesheet['FontSize']
        fontName = fontset[stylesheet['Font']]['Name']
        print('%r gets %s' % (substring, font))
        index += length
        break

    tlayer = TextFabricLayer(layer.name, layer.left - relate_x, layer.top - relate_y, layer.width, layer.height)
    tlayer.set_text(fontName, fontSize * 10, text)
    return tlayer