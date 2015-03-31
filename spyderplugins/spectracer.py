# -*- coding:utf-8 -*-
#
# Copyright © 2009-2011 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see spyderlib/__init__.py for details)


from spyderlib.qt.QtGui import QInputDialog, QVBoxLayout, QGroupBox, QLabel
from spyderlib.qt.QtCore import Signal, Qt

# Local imports
from spyderlib.baseconfig import get_translation
_ = get_translation("spectracer", dirname="spyderplugins")
from spyderlib.utils.qthelpers import get_icon, create_action
from spyderlib.plugins import SpyderPluginMixin, PluginConfigPage

from spyderplugins.widgets.spectracergui import SpectracerWidget
from core import ChartManager


class Spectracer(SpectracerWidget, SpyderPluginMixin):
    """Python source code analysis based on pylint"""
    CONF_SECTION = 'spectracer'
    edit_goto = Signal(str, int, str)

    def __init__(self, context, parent=None, index=0):
        SpectracerWidget.__init__(self, parent=parent)
        SpyderPluginMixin.__init__(self, parent)

        self.index = index
        # Initialize plugin
        self.initialize_plugin()
        self.chart_manager = ChartManager(context, self.chart)
        
    #------ SpyderPluginWidget API --------------------------------------------
    def title_suffix(self):
        return " {0}".format(self.index + 1) if self.index > 0 else ""
    def get_plugin_title(self):
        """Return widget title"""
        return _("Spectracer") + self.title_suffix()
    
    def get_plugin_icon(self):
        """Return widget icon"""
        return get_icon('pylint.png')
    
    def get_focus_widget(self):
        """
        Return the widget to give focus to when
        this plugin's dockwidget is raised on top-level
        """
        return self.chart
    
    def get_plugin_actions(self):
        """Return a list of actions related to plugin"""
        return []

    def on_first_registration(self):
        """Action to be performed on first plugin registration"""
        self.main.tabify_plugins(self.main.inspector, self)
        self.dockwidget.hide()

    def register_plugin(self):
        """Register plugin in Spyder's main window"""
        self.edit_goto.connect(self.main.editor.load)
        self.redirect_stdio.connect(self.main.redirect_internalshell_stdio)
        self.main.add_dockwidget(self)

    def refresh_plugin(self):
        """Refresh widget"""
        pass

    def closing_plugin(self, cancelable=False):
        """Perform actions before parent main window is closed"""
        return True
            
    def apply_plugin_settings(self, options):
        """Apply configuration file's plugin settings"""
        # The history depth option will be applied at 
        # next Spyder startup, which is soon enough
        pass
