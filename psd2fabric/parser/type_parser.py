from psd_tools.api.layers import TypeLayer

from psd2fabric.fabric.text import TextFabricLayer


def parse(layer: TypeLayer, relate_x, relate_y):
    text = layer.engine_dict['Editor']['Text'].value
    fontset = layer.resource_dict['FontSet']
    styleSheetSet = layer.resource_dict['StyleSheetSet']
    engineDict = layer.engine_dict
    runlength = engineDict["StyleRun"]["RunLengthArray"]
    rundata = engineDict["StyleRun"]["RunArray"]
    paragraph_rundata = engineDict['ParagraphRun']['RunArray']
    writingDirection = engineDict["Rendered"]["Shapes"]["WritingDirection"]
    index = 0
    for length, style, paragraph in zip(runlength, rundata, paragraph_rundata):
        # just use the first one
        # substring = text[index:index + length]
        stylesheet = style['StyleSheet']['StyleSheetData']
        paragraphsheet = paragraph['ParagraphSheet']['Properties']
        if 'Font' in stylesheet:
            fontType = stylesheet['Font']
        else:
            fontType = styleSheetSet[index]['StyleSheetData']['Font']

        font_size = stylesheet['FontSize']
        font_size = round(get_size(font_size, layer.transform), 2)
        font_name = fontset[fontType]['Name']
        font_color = get_color(stylesheet['FillColor']['Values'])
        break

    tlayer = TextFabricLayer(layer.name, layer.left - relate_x, layer.top - relate_y, layer.width, layer.height)
    text = get_text(text)
    tlayer.set_text(
        font_name,
        font_size,
        font_color,
        get_bold(stylesheet),
        get_align(paragraphsheet),
        text if writingDirection != 2 else "\n".join(list(text.replace("\n", "")))
    )
    return tlayer


def get_color(color):
    rgba_values = [round(c * 255, 0) for c in color]
    return f"rgba({','.join(map(str, rgba_values[1:]))},{rgba_values[0]})"


def get_size(font_size, transform):
    return font_size * transform[0]

def get_text(text):
    return text.replace('\r', '\n')

def get_align(paragraphsheet):
    if not 'Justification' in paragraphsheet:
        return 'left'

    if paragraphsheet['Justification'] == 1:
        return 'right'
    elif paragraphsheet['Justification'] == 2:
        return 'center'

    return 'left'

def get_bold(stylesheet):
    if 'FauxBold' in stylesheet:
        return stylesheet['FauxBold']
    return False