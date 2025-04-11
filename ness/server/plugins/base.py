# server/plugins/base.py
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @abstractmethod
    def name(self) -> str:
        """Return a unique name for the plugin"""
        pass

    @abstractmethod
    def execute(self, **kwargs):
        """Main function to run the plugin"""
        pass
