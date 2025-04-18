from abc import ABC, abstractmethod

class PluginBase(ABC):
    _plugins = []
    
    @classmethod
    def register(cls):
        def decorator(subclass):
            cls._plugins.append(subclass)
            return subclass
        return decorator

    @abstractmethod
    def initialize(self, *args):
        pass

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
    

class PluginManager:
    def __init__(self):
        self.instances = {}

    def get_plugin(self, plugin_name):
        plugin_class = next((p for p in PluginBase._plugins if p.__name__.lower() == plugin_name), None)

        if plugin_class:
            if plugin_name not in self.instances:
                plugin_instance = plugin_class()
                plugin_instance.initialize()  # Initialize the plugin
                self.instances[plugin_name] = plugin_instance
            return self.instances[plugin_name]
        else:
            raise ValueError(f"Plugin {plugin_name} not found.")

    @staticmethod
    def plugins_list():
        return [p.__name__ for p in PluginBase._plugins]