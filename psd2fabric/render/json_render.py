import json

from psd2fabric.fabric import FabricLayer, Fabric


def custom_default(obj):
    if isinstance(obj, (FabricLayer, Fabric)):
        return obj.__dict__
    return str(obj)


def render_json(obj: Fabric):
    # 将 Person 对象转换为 JSON 字符串
    return json.dumps(obj, default=custom_default, ensure_ascii=False)


def dump_json_file(obj, file):
    content = render_json(obj)
    with open(file, 'w') as file:
        # 将字符串写入文件
        file.write(content)

