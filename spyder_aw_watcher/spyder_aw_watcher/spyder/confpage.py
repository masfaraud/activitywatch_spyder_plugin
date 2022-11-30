# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2022, Steven Masfaraud
#
# Licensed under the terms of the GNU General Public License v3
# ----------------------------------------------------------------------------
"""
Activity Watch Spyder plugin Preferences Page.
"""
from spyder.api.preferences import PluginConfigPage
from spyder.api.translations import get_translation

_ = get_translation("spyder_aw_watcher.spyder")


class ActivityWatchSpyderpluginConfigPage(PluginConfigPage):

    # --- PluginConfigPage API
    # ------------------------------------------------------------------------
    def setup_page(self):
        pass
