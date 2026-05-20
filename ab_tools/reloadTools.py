# -*- coding: utf-8 -*-
"""
AB Tools 模块重载工具

用途：遍历 ab_tools 包内所有已加载模块并重新载入，
     确保代码修改即时生效，无需重启 Maya。

使用方式：
    from ab_tools import reload_all
    reload_all()
"""

import sys
import importlib


def reload_all():
    """重载 ab_tools 包内所有已加载的模块

    Returns:
        int: 成功重载的模块数量
    """
    prefix = "ab_tools"

    modules = [(n, m) for n, m in sys.modules.items()
               if n.startswith(prefix) and m is not None]

    # 反向排序：子模块先重载，父模块后重载
    modules.sort(key=lambda x: x[0], reverse=True)

    ok = 0
    for name, module in modules:
        try:
            importlib.reload(module)
            print(f"  [OK] {name}")
            ok += 1
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")

    print(f"AB Tools 重载完成，共 {ok}/{len(modules)} 个模块")
    return ok

