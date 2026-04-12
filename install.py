import os
import sys

def onMayaDroppedPythonFile(*args):
    plugin_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"插件地址: {plugin_dir}")
    
    if plugin_dir not in sys.path:
        sys.path.append(plugin_dir+'/ab_tools')
        print(f"插件路径已添加到: {plugin_dir+'/ab_tools'}")
    else:
        print(f"插件路径已存在: {plugin_dir+'/ab_tools'}")

