# coding=utf-8
from __future__ import absolute_import

# # (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import requests


class Dht22Plugin(octoprint.plugin.SettingsPlugin,
                  octoprint.plugin.AssetPlugin,
                  octoprint.plugin.TemplatePlugin):
    def on_after_startup(self):
        self._logger.info("Hello World! (more: %s)" % self._settings.get(["url"]))

    def get_settings_defaults(self):
        return dict(url="192.168.178.57")

    # ~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/dht22.js"],
            # "css": ["css/dht22.css"],
            # "less": ["less/dht22.less"]
        }

    # ~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "dht22": {
                "displayName": "Dht22 Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "N30Z",
                "repo": "OctoPrint-Dht22",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/N30Z/OctoPrint-Dht22/archive/{target_version}.zip",
            }
        }

    def _fetch_value_from_website(self):
        # Fetch the value from the website
        try:
            # Assuming you're fetching the value using requests library
            url = self._settings.get(["website_url"])
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                self._logger.error("Failed to fetch value from website. Status code: %d", response.status_code)
                return None
        except Exception as e:
            self._logger.error("Failed to fetch value from website: %s", str(e))
            return None


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Dht22 Plugin"

# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Dht22Plugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
