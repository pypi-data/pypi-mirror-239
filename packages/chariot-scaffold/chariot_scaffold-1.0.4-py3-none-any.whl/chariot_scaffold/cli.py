import os
import sys
import argparse
import importlib
from chariot_scaffold.core.plugin import Pack
from chariot_scaffold import version


def main():
    # CLI
    parser = argparse.ArgumentParser(description=f'千乘CLI工具 v{version}')
    parser.add_argument("plugin", help="插件文件", type=str)
    parser.add_argument("-y", "--yml", help="生成yml文件", action="store_true")
    parser.add_argument("-g", "--generate", help="生成插件项目文件", action="store_true")
    parser.add_argument("-mki", "--mkimg", help="生成离线包, 需要联网", action="store_true")
    parser.add_argument("-tb", "--tarball", help="生成在线包", action="store_true")


    # args
    args = parser.parse_args()
    assert ".py" in args.plugin, ValueError("请检查传入的文件是否是插件文件")


    # path
    path = os.path.split(args.plugin)
    dir_path = os.path.dirname(os.path.abspath(args.plugin))
    file_path = os.path.abspath(args.plugin)
    sys.path.append(dir_path)


    # import
    module = path[-1].replace('.py', '')
    lib = importlib.import_module(module)

    pack: Pack | None = None
    for k, v in lib.__dict__.items():
        if "__" not in k and "Pack" != k:
            try:
                attr = getattr(v, "plugin_config_init")
                if attr:
                    pack = v()
                    break
            except Exception as e:  # noqa
                pass

    assert pack is not None, ImportError("导入插件失败, 请检查插件代码")


    # param check
    if args.mkimg and args.tarball:
        raise AssertionError("生成离线包和生成在线包不可同时使用")


    # call
    if args.yml:
        pack.create_yaml(dir_path)

    if args.generate:
        pack.generate_project(dir_path)

    if args.mkimg:
        pack.generate_offline_pack(file_path)

    if args.tarball:
        pack.generate_online_pack(file_path)

