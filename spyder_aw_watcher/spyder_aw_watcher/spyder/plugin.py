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

# Local imports
from spyder_aw_watcher.spyder.confpage import ActivityWatchSpyderpluginConfigPage
from spyder_aw_watcher.spyder.container import ActivityWatchSpyderpluginContainer

_ = get_translation("spyder_aw_watcher.spyder")


class ActivityWatchSpyderplugin(SpyderPluginV2):
    """
    Activity Watch Spyder plugin plugin.
    """

    NAME = "spyder_aw_watcher"
    REQUIRES = []
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
        print('ActivityWatchSpyderplugin initialized!')

    def check_compatibility(self):
        valid = True
        message = ""  # Note: Remember to use _("") to localize the string
        return valid, message

    def on_close(self, cancellable=True):
        return True

    # --- Public API
    # ------------------------------------------------------------------------
