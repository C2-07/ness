"""
Plugin system for the AI Discord Assistant

This module automatically imports all plugins in subdirectories.
Each plugin should have its own directory with an __init__.py file that defines a subclass of BasePlugin.
"""

import os
import logging
import importlib
import inspect
from typing import Dict, Type
from plugins.base import BasePlugin

logger = logging.getLogger(__name__)

# Dictionary to store all registered plugins
registered_plugins: Dict[str, BasePlugin] = {}

def register_plugin(plugin_class: Type[BasePlugin]) -> None:
    """
    Register a plugin class with the system

    Args:
        plugin_class: The plugin class (must inherit from BasePlugin)
    """
    if not issubclass(plugin_class, BasePlugin):
        logger.warning(f"Tried to register non-plugin: {plugin_class}")
        return
    
    plugin_instance = plugin_class()
    plugin_name = plugin_instance.name()

    registered_plugins[plugin_name] = plugin_instance
    logger.info(f"Registered plugin: {plugin_name}")

# Dynamically import all plugin packages and register subclasses
def _import_plugins():
    plugins_dir = os.path.dirname(__file__)

    for item in os.listdir(plugins_dir):
        if os.path.isdir(os.path.join(plugins_dir, item)) and not item.startswith('_'):
            try:
                module = importlib.import_module(f"plugins.{item}")
                logger.info(f"Loaded plugin module: {item}")

                # Auto-register all subclasses of BasePlugin
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BasePlugin) and obj is not BasePlugin:
                        register_plugin(obj)

            except ImportError as e:
                logger.error(f"Failed to import plugin {item}: {e}")

# Import and register all plugins
_import_plugins()
logger.info(f"Plugins registered: {list(registered_plugins.keys())}")

