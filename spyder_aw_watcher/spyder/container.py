# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2022, Steven Masfaraud
#
# Licensed under the terms of the GNU General Public License v3
# ----------------------------------------------------------------------------
"""
Activity Watch Spyder plugin Main Container.
"""
# Spyder imports
from spyder.api.config.decorators import on_conf_change
from spyder.api.translations import get_translation
from spyder.api.widgets.main_container import PluginMainContainer

from spyder_aw_watcher.spyder.widgets import ActivityWatchStatus

_ = get_translation("spyder_aw_watcher.spyder")


class ActivityWatchSpyderpluginContainer(PluginMainContainer):

    # Signals

    # --- PluginMainContainer API
    # ------------------------------------------------------------------------
    def setup(self):
        self.activity_watch_status = ActivityWatchStatus(self)
        self.activity_watch_status.set_value('Starting watcher')

    def update_actions(self):
        pass

    # --- Public API
    # ------------------------------------------------------------------------
