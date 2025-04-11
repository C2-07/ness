from plugins.base import BasePlugin

class HelloPlugin(BasePlugin):
    # Plugin Name
    def name(self):
        return "hello"

    def execute(self, **kwargs):
        return f"Hello, {kwargs.get('user', 'world')}!"
