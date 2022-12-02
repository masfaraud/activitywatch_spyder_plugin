# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2022, Steven Masfaraud
#
# Licensed under the terms of the GNU General Public License v3
# ----------------------------------------------------------------------------
"""
Activity Watch Spyder plugin Plugin.
"""

# Third-party imports
from qtpy.QtGui import QIcon

# Spyder imports
from spyder.api.plugins import Plugins, SpyderPluginV2
from spyder.api.translations import get_translation
from spyder.api.plugin_registration.decorators import on_plugin_available

# Local imports
from spyder_aw_watcher.spyder.confpage import ActivityWatchSpyderpluginConfigPage
from spyder_aw_watcher.spyder.container import ActivityWatchSpyderpluginContainer

from datetime import datetime, timezone

from aw_core.models import Event
from aw_client import ActivityWatchClient

_ = get_translation("spyder_aw_watcher.spyder")


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

        self.client = ActivityWatchClient("test-client", testing=True)
        bucket_id = "{}_{}".format("test-client-bucket", self.client.client_hostname)
        connection_success = True
        
        # Try to access editor
        self.opened_file = None
        
        try:
            self.client.create_bucket(bucket_id, event_type="dummydata")
        except:
            self.aw_status.set_value('Cannot connect to AW')
            connection_success = False
            
        if connection_success:
            data = {'file': 'test.py', 'project': '/etc/test', 'language': 'python'}
            now = datetime.now(timezone.utc)
            event = Event(timestamp=now, data=data)
            inserted_event = self.client.insert_event(bucket_id, event)
            print(inserted_event)
            self.aw_status.set_value('Connected to AW')
        
        
    @on_plugin_available(plugin=Plugins.StatusBar)
    def on_statusbar_available(self):
        statusbar = self.get_plugin(Plugins.StatusBar)
        if statusbar:
            statusbar.add_status_widget(self.aw_status)

    @on_plugin_available(plugin=Plugins.Editor)
    def on_editor_available(self):
        editor = self.get_plugin(Plugins.Editor)
        if editor:
            print('editor found')
            print('editor.codeeditor', [k for k in sorted(editor.__dict__.keys())])
            print('editor.dockwidget', [k for k in sorted(editor.dockwidget.__dict__.keys())])
            print('')
            # editor.sig_filename_changed.connect(self._track_filename)
            # print('editor found')
            editor.sig_file_opened_closed_or_updated.connect(self.set_current_opened_file)
    
    def _track_filename(self):
        editor = self.get_plugin(Plugins.Editor)
        if editor:
            print('ee', editor.get_current_filename())

    def set_current_opened_file(self, path, _language):
        """
        Set path of current opened file in editor.
        Parameters
        ----------
        path: str
            Path of editor file.
        """
        print('path', path, _language)
        # self.get_widget().set_file_path(path)
            
    @property
    def aw_status(self):
        container = self.get_container()
        return container.activity_watch_status

    def check_compatibility(self):
        valid = True
        message = ""  # Note: Remember to use _("") to localize the string
        return valid, message

    def on_close(self, cancellable=True):
        return True

    # --- Public API
    # ------------------------------------------------------------------------
