# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
import requests


class Dht22Plugin(octoprint.plugin.SettingsPlugin,
                  octoprint.plugin.AssetPlugin,
                  octoprint.plugin.TemplatePlugin):

    def on_after_startup(self):
        self._logger.info("Hello World! (more: %s)" % self._settings.get(["url"]))

    def get_settings_defaults(self):
        return dict(url="http://192.168.178.21/Tim.html")

    def get_assets(self):
        return {
            "js": ["js/dht22.js"],
            "css": ["css/dht22.css"],
        }

    def get_update_information(self):
        return {
            "dht22": {
                "displayName": "Dht22 Plugin",
                "displayVersion": self._plugin_version,
                "type": "github_release",
                "user": "N30Z",
                "repo": "OctoPrint-Dht22",
                "current": self._plugin_version,
                "pip": "https://github.com/N30Z/OctoPrint-Dht22/archive/{target_version}.zip",
            }
        }

    def _fetch_value_from_website(self):
        try:
            url = self._settings.get(["url"])
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                self._logger.error("Failed to fetch value from website. Status code: %d", response.status_code)
                return None
        except Exception as e:
            self._logger.error("Failed to fetch value from website: %s", str(e))
            return None

    def get_template_configs(self):
        return [
            dict(type="navbar", template="dht22_navbar.jinja2"),
            dict(type="settings", template="dht22_settings.jinja2"),
            dict(type="tab", template="dht22_tab.jinja2", custom_bindings=False),
        ]


__plugin_name__ = "Dht22 Plugin"
__plugin_pythoncompat__ = ">=3,<4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Dht22Plugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
