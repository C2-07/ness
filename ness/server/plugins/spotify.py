from plugin_manager import PluginBase, PluginManager

# Plugin Example 1: Spotify Plugin
@PluginBase.register()
class SpotifyPlugin(PluginBase):
    def initialize(self, API_KEY: str=""):
        self.API_KEY = API_KEY
        # Initialize any resources needed
        self.client = "SpotifyClient"
        self.is_playing = False
        print(f"{self.client} initialized.")

    def execute(self, action, **kwargs):
        # Execute the requested action
        if action == "play":
            self.play(**kwargs)
        elif action == "pause":
            self.pause()
        else:
            print(f"Unknown action: {action}")

    def play(self, track_name):
        # Simulate playing a track
        self.is_playing = True
        print(f"Playing {track_name} on Spotify.")

    def pause(self):
        # Simulate pausing the track
        self.is_playing = False
        print("Paused Spotify.")

# Usage:
manager = PluginManager()

# Initialize the Spotify plugin (but not run it yet)
spotify_plugin = manager.get_plugin("spotifyplugin")

# Now the user can execute the play/pause actions with parameters
spotify_plugin.execute(action="play", track_name="Imagine - John Lennon")
spotify_plugin.execute(action="pause")

print(manager.plugins_list())