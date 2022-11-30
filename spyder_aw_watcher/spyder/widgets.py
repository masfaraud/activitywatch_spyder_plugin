# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2022, Steven Masfaraud
#
# Licensed under the terms of the GNU General Public License v3
# ----------------------------------------------------------------------------
"""
Activity Watch Spyder plugin Main Widget.
"""



# Spyder imports
from spyder.api.config.decorators import on_conf_change
from spyder.api.translations import get_translation



from spyder.api.widgets.status import StatusBarWidget
from spyder.utils.icon_manager import ima

# Third party imports
import qtawesome as qta


# Localization
_ = get_translation("spyder_aw_watcher.spyder")



class ActivityWatchStatus(StatusBarWidget):
    """Status bar widget to display the pomodoro timer"""

    ID = "pomodoro_timer_status"
    CONF_SECTION = "spyder_activity_watch"

    def get_tooltip(self):
        """Override api method."""
        return "Activity watch"

    def get_icon(self):
        return qta.icon("ei.eye-open", color=ima.MAIN_FG_COLOR)