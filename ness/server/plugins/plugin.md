# 🔌 Plugin System Guide

This document explains how to use and create plugins for the **Ness Server**.

---

## 📦 Plugin Folder Structure

```
ness/
├── server/
│   ├── plugins/
│   │   ├── __init__.py          ← Plugin loader and registry
│   │   ├── base.py              ← Abstract base plugin class
│   │   └── my_plugin/
│   │       └── __init__.py      ← Your plugin implementation
```

---

## 🚀 How It Works

1. **Base class** `BasePlugin` defines the interface every plugin must implement.
2. Plugins are placed in subfolders under `plugins/`.
3. Each plugin must define a class and register it using `register_plugin()`.
4. Plugins are auto-loaded when the app starts.

---

## 🧱 Create a Plugin

### 1. Define a Plugin Class

In a new subfolder inside `server/plugins/`, create an `__init__.py`:

```python
# server/plugins/greet/__init__.py
from server.plugins.base import BasePlugin
from server.plugins import register_plugin

class GreetPlugin(BasePlugin):
    def name(self) -> str:
        return "greet"

    def execute(self, **kwargs):
        user = kwargs.get("user", "there")
        return f"Hello, {user}! Welcome to the server."

register_plugin(GreetPlugin)
```

### 2. Required Plugin Structure

Each plugin **must**:

- Inherit from `BasePlugin`
- Implement:
  - `name(self) -> str` – returns a unique name for the plugin
  - `execute(self, **kwargs)` – performs the plugin's task

---

## ⚙️ BasePlugin Spec

```python
class BasePlugin(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def execute(self, **kwargs):
        pass
```

---

## 🔍 Accessing Plugins

You can access all loaded plugins using:

```python
from server.plugins import registered_plugins

response = registered_plugins["greet"].execute(user="Gourav")
print(response)
```

---

## 🐛 Troubleshooting

- Make sure plugin folders have an `__init__.py`
- Plugin folder names must not start with `_`
- Run your project using:

  ```bash
  python -m server.main
  ```

  (From the root of the project)

---

## 📌 Tips

- Keep plugin names unique.
- Use plugins to add modular features (e.g. music, weather, tasks).
- Each plugin can wrap a full feature with multiple internal helpers.

---
