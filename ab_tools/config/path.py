# -*- coding: utf-8 -*-
"""通用资源路径（config 和 preferences 共用，不依赖任何模块）"""
import os

_FILE = os.path.abspath(__file__)
_PACKAGE = os.path.dirname(os.path.dirname(_FILE))
_ROOT = os.path.dirname(_PACKAGE)


class Path:
    ICONS: str = os.path.join(_PACKAGE, "icons")
    UI: str = os.path.join(_PACKAGE, "ui")
    TOOLS: str = os.path.join(_ROOT, "tools")
    PREFS: str = os.path.join(_PACKAGE, "prefs")
