# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2022, Steven Masfaraud
#
# Licensed under the terms of the GNU General Public License v3
# ----------------------------------------------------------------------------
"""
Activity Watch Spyder plugin Plugin.
"""

import os
import time

# Third-party imports
from qtpy.QtGui import QIcon

# Spyder imports
from spyder.api.plugins import Plugins, SpyderPluginV2
from spyder.api.translations import get_translation
from spyder.api.plugin_registration.decorators import on_plugin_available, on_plugin_teardown

# Local imports
from spyder_aw_watcher.spyder.confpage import ActivityWatchSpyderpluginConfigPage
from spyder_aw_watcher.spyder.container import ActivityWatchSpyderpluginContainer

from datetime import datetime, timezone

from aw_core.models import Event
from aw_client import ActivityWatchClient

_ = get_translation("spyder_aw_watcher.spyder")

SEND_DELAY = 10.0


class ActivityWatchSpyderplugin(SpyderPluginV2):
    """
    Activity Watch Spyder plugin plugin.
    """

    NAME = "spyder_aw_watcher"
    REQUIRES = [Plugins.StatusBar, Plugins.Editor]
    OPTIONAL = []
    CONTAINER_CLASS = ActivityWatchSpyderpluginContainer
    CONF_SECTION = NAME
    CONF_WIDGET_CLASS = ActivityWatchSpyderpluginConfigPage

    # --- Signals

    # --- SpyderPluginV2 API
    # ------------------------------------------------------------------------
    def get_name(self):
        return _("Activity Watch Spyder plugin")

    def get_description(self):
        return _("ActivityWatch watcher plugin for spyder")

    def get_icon(self):
        return QIcon()

    def on_initialize(self):
        container = self.get_container()

        # print('=== container ===')
        # for k in sorted(dir(container)):
        #     print(k)

        self.last_send = 0.0
        self.last_file_changed = time.time()
        self.current_file = None
        self.current_language = None

        # print('parent', self.parent())
        # for k in dir(self.parent()):
        #     print(k)

        self.client = ActivityWatchClient("test-client", testing=False)
        self.bucket_id = "{}_{}".format("spyder", self.client.client_hostname)
        connection_success = True

        # Try to access editor
        self.opened_file = None

        if not self.test_aw_connection():
            self.aw_status.set_value("AW Down")
        else:
            self.aw_status.set_value("AW Up")

    @on_plugin_available(plugin=Plugins.StatusBar)
    def on_statusbar_available(self):
        statusbar = self.get_plugin(Plugins.StatusBar)
        if statusbar:
            statusbar.add_status_widget(self.aw_status)

    @on_plugin_available(plugin=Plugins.Editor)
    def on_editor_available(self):
        editor = self.get_plugin(Plugins.Editor)
        if editor:
            editor.sig_file_opened_closed_or_updated.connect(self.update_filename)

    @on_plugin_teardown(plugin=Plugins.Editor)
    def on_editor_teardown(self):
        editor = self.get_plugin(Plugins.Editor)
        if editor:
            editor.sig_file_opened_closed_or_updated.disconnect(self.update_filename)

    def update_filename(self, path, language):
        """
        Set path of current opened file in editor.
        Parameters
        ----------
        path: str
            Path of editor file.
        """
        # editor = self.get_plugin(Plugins.Editor)
        # print(self.parent().parent())
        # print(self.parent().parent().hasFocus())

        if self.last_send == 0.0:
            self.current_file = path
            self.current_language = language

        # self.aw_status.set_value(f"{path}  {self.current_file}")

        if path != self.current_file:
            self.current_file = path
            self.current_language = language
            self.last_file_changed = time.time()

        self.send_data()

    @property
    def aw_status(self):
        container = self.get_container()
        return container.activity_watch_status

    def test_aw_connection(self):
        try:
            self.client.create_bucket(self.bucket_id, event_type="app.editor.activity¶")
            return True
        except:
            return False

    def send_data(self):
        # self.aw_status.set_value(str(time.time() - self.last_send))
        duration = time.time() - self.last_send
        if duration > SEND_DELAY:
            # Sending data to aw
            last_slash_index = self.current_file.rfind(os.sep)
            path = self.current_file[:last_slash_index]
            file = self.current_file[last_slash_index + 1 :]
            data = {"file": file, "project": path, "language": self.current_language}
            now = datetime.now(timezone.utc)
            event = Event(timestamp=now, data=data, duration=duration)
            inserted_event = self.client.insert_event(self.bucket_id, event)
            self.aw_status.set_value("Send OK")

            self.last_send = time.time()

    def check_compatibility(self):
        valid = True
        message = ""  # Note: Remember to use _("") to localize the string
        return valid, message

    def on_close(self, cancellable=True):
        return True

    # --- Public API
    # ------------------------------------------------------------------------
