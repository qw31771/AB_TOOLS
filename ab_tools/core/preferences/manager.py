# -*- coding: utf-8 -*-
"""偏好存储引擎 — 基于 JSON 的模块化持久存储

每个 scope 对应一个独立的 JSON 文件，互不干扰。
"""
import json
import os
import threading


class ScopePrefs:
    """单个 scope 的偏好数据容器

    自动加载/写入 JSON，接口类似 dict。
    """

    def __init__(self, filepath: str):
        self._filepath = filepath
        self._lock = threading.Lock()
        self._data = self._load()

    # ---- 内部 ----

    def _load(self) -> dict:
        """从 JSON 文件加载数据"""
        if os.path.exists(self._filepath):
            try:
                with open(self._filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {}

    def _save(self):
        """写入 JSON 文件（线程安全）"""
        with self._lock:
            dir_path = os.path.dirname(self._filepath)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            with open(self._filepath, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)

    # ---- 公开 API ----

    def get(self, key: str, default=None):
        """读取指定 key 的值

        Args:
            key: str - 键名
            default: 任意 - 键不存在时的默认值

        Returns:
            对应值或 default
        """
        return self._data.get(key, default)

    def set(self, key: str, value):
        """写入键值对并立即保存

        Args:
            key: str - 键名
            value: 任意可 JSON 序列化的值
        """
        self._data[key] = value
        self._save()

    def remove(self, key: str):
        """删除指定 key"""
        if key in self._data:
            del self._data[key]
            self._save()

    def all(self) -> dict:
        """返回 scope 下全部数据的副本"""
        return dict(self._data)

    def clear(self):
        """清空当前 scope 全部数据"""
        self._data.clear()
        self._save()


class PreferencesManager:
    """偏好存储管理器 — 按 scope 分文件管理

    用法:
        manager = PreferencesManager("/path/to/prefs")
        manager.scope("window").set("collapsed", True)
        manager.scope("window").get("collapsed")  # True
    """

    def __init__(self, base_dir: str):
        """
        Args:
            base_dir: str - JSON 文件的存储目录
        """
        self._base_dir = base_dir
        self._scopes = {}

    def scope(self, name: str) -> ScopePrefs:
        """获取指定 scope 的偏好对象

        首次访问时自动创建 ScopePrefs 实例并缓存。

        Args:
            name: str - scope 名称，对应 {name}.json 文件

        Returns:
            ScopePrefs: 该 scope 的数据容器
        """
        if name not in self._scopes:
            filepath = os.path.join(self._base_dir, f"{name}.json")
            self._scopes[name] = ScopePrefs(filepath)
        return self._scopes[name]

    # ---- 快捷方法 ----

    def get(self, scope: str, key: str, default=None):
        """快捷读取：manager.get("window", "collapsed")"""
        return self.scope(scope).get(key, default)

    def set(self, scope: str, key: str, value):
        """快捷写入：manager.set("window", "collapsed", True)"""
        self.scope(scope).set(key, value)

    def remove(self, scope: str, key: str):
        """快捷删除：manager.remove("window", "collapsed")"""
        self.scope(scope).remove(key)
