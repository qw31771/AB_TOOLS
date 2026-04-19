# -*- coding: utf-8 -*-
import os
import sys
import maya.cmds as cmds

def onMayaDroppedPythonFile(*args, **kwargs):
    """
    Maya 拖拽安装入口函数
    """
    # 获取当前 install.py 所在的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 将插件根目录添加到 Maya 的环境变量中 (如果不存在的话)
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    # 设置自启动脚本
    setup_user_script(current_dir)

    # 导入插件并执行初始化动作
    try:
        import ab_tools
        import importlib
        importlib.reload(ab_tools)  # 保证每次拖拽都能热更新，方便开发

        # 触发初始化
        ab_tools.init()

        # 提示用户安装成功
        cmds.inViewMessage(amg="<hl>AB Tools</hl> 安装成功！请点击上方AB_TOOLS工具架。",
                           pos='midCenterTop', fade=True)
    except Exception as e:
        import traceback
        traceback.print_exc()
        cmds.warning(f"AB Tools 安装失败，请查看脚本编辑器获取详细信息: {e}")

def setup_user_script(plugin_dir):
    """
    设置 Maya 自启动脚本，确保每次启动 Maya 时插件都能自动加载
    """
    import re

    # 获取 Maya 用户脚本目录
    user_script_dir = cmds.internalVar(uad=1)+'/scripts'

    # 定义自启动脚本的路径
    user_script_path = os.path.join(user_script_dir, "userSetup.py")

    # 定义要添加到 userSetup.py 中的代码
    init_code = f"""#[ AB TOOLS ]
import maya.cmds as cmds
import sys
import maya.utils as utils
plugin_dir = "{plugin_dir}"
if plugin_dir not in sys.path:
    sys.path.append(plugin_dir)
    
def startup_entry():
    import ab_tools
    ab_tools.init()

utils.executeDeferred(startup_entry)
"""

    # 如果 userSetup.py 不存在，则创建并写入代码
    if not os.path.exists(user_script_path):
        print(f"[AB Tools] 创建新的自启动脚本")
        with open(user_script_path, 'w', encoding="utf-8") as f:
            f.write(init_code)
        print(f"[AB Tools] 自启动脚本创建成功")
    else:
        # 如果 userSetup.py 已存在，检查是否已经包含 AB Tools 的初始化代码
        with open(user_script_path, 'r', encoding="utf-8") as f:
            content = f.read()

        if "import ab_tools" not in content:
            print(f"[AB Tools] 自启动脚本存在，但未包含AB Tools代码，正在追加")
            # 如果没有包含，则追加代码
            with open(user_script_path, 'a', encoding="utf-8") as f_append:
                f_append.write("\n\n" + init_code)
        else:
            # 如果已包含 AB Tools 代码，检查 plugin_dir 路径是否需要更新
            pattern = r'(plugin_dir\s*=\s*[\"\'])([^\"\']+)([\"\'])'
            match = re.search(pattern, content)

            if match:
                old_path = match.group(2)

                # 标准化路径进行比较（处理路径分隔符和大小写差异）
                norm_old_path = os.path.normpath(old_path)
                norm_new_path = os.path.normpath(plugin_dir)

                if norm_old_path.lower() != norm_new_path.lower():
                    print(f"[AB Tools] 插件目录已变更，正在更新路径")
                    # 替换路径部分，保持引号类型不变
                    new_content = content[:match.start(2)] + plugin_dir + content[match.end(2):]

                    with open(user_script_path, 'w', encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"[AB Tools] 插件目录更新成功")
            else:
                print(f"[AB Tools] 警告：未找到 plugin_dir 赋值语句，但包含 import ab_tools")
                # 如果找不到 plugin_dir 行，可能需要重新写入整个代码块
                # 这里可以追加新的代码块或替换，但为了安全，暂时只记录警告

