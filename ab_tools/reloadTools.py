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

# 全局基础设施模块 — 必须在 UI 等消费模块之前重载
_PRIORITY_PREFIXES = [
    "ab_tools.config",
    "ab_tools.core",
    "ab_tools.ui.sidebar",
]


def _reload_key(name):
    """排序键：基础设施优先，同组内子模块先于父模块"""
    for i, pfx in enumerate(_PRIORITY_PREFIXES):
        if name == pfx or name.startswith(pfx + "."):
            return (i, -len(name))
    return (len(_PRIORITY_PREFIXES), -len(name))


def reload_all():
    """重载 ab_tools 包内所有已加载的模块

    Returns:
        int: 成功重载的模块数量
    """
    prefix = "ab_tools"

    modules = [(n, m) for n, m in sys.modules.items()
               if n.startswith(prefix) and m is not None]

    # 全局基础设施优先 → 其余模块 → 根模块最后
    modules.sort(key=lambda x: _reload_key(x[0]))
    # 将 ab_tools 根模块挪到最后
    root = None
    filtered = []
    for name, module in modules:
        if name == "ab_tools":
            root = ("ab_tools", module)
        else:
            filtered.append((name, module))
    if root:
        filtered.append(root)
    modules = filtered

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

