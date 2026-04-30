# -*- coding: utf-8 -*-
"""
ic52ic_racional.py — Main plugin class for IC52IC Rational Method.
QGIS 4.0 / Qt6.
"""

import os

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from qgis.core import QgsApplication


class IC52ICRacionalPlugin:
    """IC 5.2-IC Rational Method QGIS Plugin."""

    def __init__(self, iface):
        self.iface = iface
        self._action = None
        self._dialog = None
        self.plugin_dir = os.path.dirname(__file__)

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, "icon.png")
        icon = QIcon(icon_path) if os.path.exists(icon_path) else QIcon()

        self._action = QAction(
            icon,
            "IC52Rational — Método Racional IC 5.2-IC",
            self.iface.mainWindow(),
        )
        self._action.setToolTip(
            "Cálculo de caudales por el Método Racional (IC 5.2-IC, Cap. 2)\n"
            "T = 10, 100, 500 años"
        )
        self._action.triggered.connect(self._run)
        self.iface.addToolBarIcon(self._action)
        self.iface.addPluginToMenu("IC52Rational", self._action)

    def unload(self):
        self.iface.removePluginMenu("IC52Rational", self._action)
        self.iface.removeToolBarIcon(self._action)
        if self._dialog is not None:
            self._dialog.close()
            self._dialog = None

    def _run(self):
        if self._dialog is None:
            from .ic52ic_dialog import IC52ICDialog
            self._dialog = IC52ICDialog(self.iface, self.iface.mainWindow())
            self._dialog.finished.connect(self._on_dialog_closed)
        self._dialog.show()
        self._dialog.raise_()
        self._dialog.activateWindow()

    def _on_dialog_closed(self):
        self._dialog = None
