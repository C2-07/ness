import asyncio
from ness.server.plugins.plugin_manager import PluginManager

async def main():
    # Create a plugin manager instance
    manager = PluginManager()
    
    # Get and initialize the Spotify plugin
    # The import 'from ness.server.plugins import spotify' loads the module,
    # which registers the SpotifyPlugin with PluginBase
    print(manager.plugins_list())
    spotify_plugin = await manager.get_plugin("Spotify")
    
    # Execute some actions on the plugin
    await spotify_plugin.execute(action="play", track_name="Imagine - John Lennon")
    await spotify_plugin.execute(action="pause")
    
    # Print available plugins
    print("Available plugins:", manager.plugins_list())

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())