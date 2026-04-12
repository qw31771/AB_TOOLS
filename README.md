# AB Tools - Maya通用工具插件

## 项目概述

AB Tools是一个Maya通用工具插件，旨在集成外部脚本到Maya环境变量中，提供一个统一的UI界面来集中管理和快速启动各种工具脚本。用户自己编写的脚本也可以快速添加到UI中，大大提高工作效率。

## 特性

- 🚀 **集中管理**: 将所有Maya工具脚本集中在一个UI界面中
- 🔧 **快速启动**: 一键执行常用工具脚本
- 📂 **脚本集成**: 自动扫描并集成外部Python脚本
- 🎨 **用户友好**: 基于PySide2的现代化界面
- ⚙️ **高度可配置**: 丰富的设置选项
- 🔌 **易于扩展**: 简单的脚本添加机制

## 系统要求

- Maya 2022及以上版本
- Python 3
- PySide2（Maya自带）

## 安装方法

### 方法1：拖放安装（推荐）
1. 将`install.py`文件拖放到Maya视图窗口中
2. 按照提示完成安装

### 方法2：手动安装
1. 将插件目录复制到Maya脚本目录：
   - Windows: `Documents\maya\<版本>\scripts\`
   - Mac: `~/Library/Preferences/Autodesk/maya/<版本>/scripts/`
2. 在Maya中运行以下Python命令：
   ```python
   import sys
   sys.path.append("你的插件路径")
   import ab_tools.main
   ab_tools.main.initialize_plugin()
   ```

## 使用方法

### 启动插件
安装后，在Maya工具架上会出现"AB Tools"按钮，点击即可打开主界面。

### 添加自定义脚本
1. 点击"添加自定义脚本"按钮
2. 选择你的Python脚本文件
3. 脚本将自动添加到工具列表中

### 脚本编写规范
要在AB Tools中使用的脚本应遵循以下规范：

```python
"""
脚本名称
脚本描述
"""

# @name: 工具显示名称
# @description: 工具描述
# @type: 工具类型
# @author: 作者
# @version: 版本号
# @category: 分类

def main():
    """
    主函数 - 将在工具执行时被调用
    返回执行结果
    """
    import maya.cmds as cmds
    # 你的代码...
    return "执行成功"
```

## 项目结构

```
AB_TOOLS/
├── install.py              # Maya拖放安装脚本
├── base.md                # 项目基础信息
├── README.md              # 项目说明文档
├── ab_tools/              # 主插件模块
│   ├── __init__.py
│   └── main.py            # 插件主入口
├── ui/                    # 用户界面模块
│   ├── __init__.py
│   ├── main_window.py     # 主窗口
│   └── settings_dialog.py # 设置对话框
├── tools/                 # 工具脚本模块
│   ├── __init__.py
│   ├── manager.py         # 工具管理器
│   ├── example_tools.py   # 示例工具1
│   └── example_tools2.py  # 示例工具2
├── config/                # 配置模块
│   ├── __init__.py
│   └── settings.py        # 设置管理
└── resources/             # 资源文件
    ├── __init__.py
    └── README.md
```

## 开发指南

### 模块说明

#### 主插件模块 (`ab_tools/`)
- `main.py`: 插件初始化和生命周期管理
- 负责创建工具架按钮和启动UI

#### UI模块 (`ui/`)
- `main_window.py`: 主界面窗口
- `settings_dialog.py`: 设置对话框
- 基于PySide2，与Maya界面集成

#### 工具管理模块 (`tools/`)
- `manager.py`: 工具脚本的管理、注册和执行
- 支持动态加载Python脚本
- 提供脚本元数据提取功能

#### 配置模块 (`config/`)
- `settings.py`: 插件设置管理
- 支持设置保存、加载和导入导出

### 扩展插件

#### 添加新功能
1. 在相应模块中添加新的类或函数
2. 在UI中集成新功能
3. 更新设置管理（如需要）

#### 添加新工具类型
1. 在`tools/manager.py`中扩展工具注册逻辑
2. 在UI中增加相应的显示和处理逻辑

## 常见问题

### Q: 插件安装后没有出现工具架按钮
A: 检查Maya脚本编辑器中的错误信息，确保插件目录已正确添加到Python路径。

### Q: 自定义脚本无法执行
A: 检查脚本是否符合规范，确保脚本中没有语法错误。

### Q: 插件界面显示异常
A: 尝试重置插件设置或重新安装插件。

### Q: 如何卸载插件
A: 删除插件目录，并在Maya中运行：
```python
import maya.cmds as cmds
if cmds.shelfButton("abToolsButton", exists=True):
    cmds.deleteUI("abToolsButton")
```

## 版本历史

### v1.0.0 (2026-04-12)
- 初始版本发布
- 基本插件框架
- 工具脚本管理功能
- PySide2用户界面
- 设置管理系统

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进这个项目。

## 许可证

本项目采用MIT许可证。详见LICENSE文件。

## 联系方式

- 作者: abin
- 邮箱: qw31771@gmail.com
- 项目地址: [GitHub仓库地址]

---

**注意**: 此插件仍在开发中，可能会存在一些问题。请在使用过程中及时反馈问题。