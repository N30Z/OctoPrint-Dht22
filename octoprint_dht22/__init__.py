# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
import requests
from flask import make_response


class Dht22Plugin(octoprint.plugin.SettingsPlugin,
                  octoprint.plugin.AssetPlugin,
                  octoprint.plugin.TemplatePlugin,
                  octoprint.plugin.SimpleApiPlugin):

    def on_after_startup(self):
        url = self._settings.get(["url"])
        self._logger.info("Hello World! (more: %s)" % url)
        self._logger.info("Current URL: %s" % url)  # Normal log message

    def get_settings_defaults(self):
        return dict(url="192.168.178.21/Tim.html")

    def on_settings_save(self, data):
        old_ip = self._settings.get(["url"])
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        url = self._settings.get(["url"])

        if old_ip != url:
            self._logger.info(f"Url changed from {old_ip} to {url}")

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

    @octoprint.plugin.BlueprintPlugin.route("/arduino_data", methods=["GET"])
    def get_arduino_data(self):
        arduino_ip = self._settings.get(["arduino_ip"])
        try:
            response = requests.get(f"http://{arduino_ip}")
            response.raise_for_status()
            data = response.text
            self._logger.info(data)
            return data, 200
        except requests.RequestException as e:
            self._logger.error("Failed to fetch data from Arduino: %s", e)
            return str(e), 500

    @octoprint.plugin.BlueprintPlugin.route("/initial_log", methods=["GET"])
    def get_initial_log(self):
        url = self._settings.get(["url"])
        log_message = f"Current URL: {url}"
        return make_response(log_message, 200)

    def get_template_configs(self):
        return [
            dict(type="navbar", template="dht22_navbar.jinja2"),
            dict(type="settings", template="dht22_settings.jinja2"),
            dict(type="tab", template="dht22_tab.jinja2", custom_bindings=False),
        ]

    def get_api_commands(self):
        return dict(fetch_data=[])

    def on_api_command(self, command, data):
        if command == "fetch_data":
            response = self._fetch_value_from_website()
            if response:
                return make_response(response, 200)
            else:
                return make_response("Failed to fetch data from Arduino.", 500)


__plugin_name__ = "Dht22 Plugin"
__plugin_pythoncompat__ = ">=3,<4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Dht22Plugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
