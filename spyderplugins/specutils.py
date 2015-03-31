from PySide import QtCore

from spyderplugins.spectracer import Spectracer
from speclib.core import DataSourceFactory


class SpectracerHelper:
    def __init__(self, main):
        self.main = main
        self.specs = []
        self.spec_widgets = []
        self.context = QtCore.QObject()
        self.dataSourceFactory = DataSourceFactory(self.context)
    def add_spec(self):
        spec = Spectracer(self.context, self.main, len(self.specs))
        self.specs.append(spec.chart_manager)
        self.spec_widgets.append(spec)
        self.main.add_dockwidget(spec)
        self.refresh_menu()
        return spec.chart_manager
    def remove_spec(self, spec):
        for w in self.main.widgetlist:
            if isinstance(w, Spectracer) and w.chart_manager == spec:
                self.main.removeDockWidget(w.dockwidget)
                w.dockwidget.close()
                w.close()
                self.main.widgetlist.remove(w)
                self.specs.remove(spec)
                spec.chartWidget.clear()
                break
        self.refresh_menu()
    def refresh_menu(self):
        if self.main.plugins_menu:
            self.main.plugins_menu.clear()
            self.main.create_plugins_menu()