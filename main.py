import sys

from psd2fabric.fabric import dump_psd

if __name__ == '__main__':

    # 检查命令行参数数量
    if len(sys.argv) != 3:
        print("Usage: python main.py arg1 arg2")
        print("- arg1: source psd file")
        print("- arg2: target json file")
        sys.exit(1)

    # 从命令行参数获取值
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]

    dump_psd(arg1, arg2)