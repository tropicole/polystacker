# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PolyStacker
                                 A QGIS plugin
 This plugin takes selected polygons and stacks them onto a point
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-01-31
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Polygon Stacker
        email                : cole.r.glover@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import random
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.core import QgsProject

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .poly_stacker_dialog import PolyStackerDialog
import os.path


class PolyStacker:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PolyStacker_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Polygon Stacker')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PolyStacker', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/poly_stacker/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'PolyStacker'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Polygon Stacker'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""
        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = PolyStackerDialog()

        # Fetch the currently loaded layers
        layers = QgsProject.instance().layerTreeRoot().children()
        # Clear the contents of the comboBox from previous runs
        self.dlg.comboBox.clear()
        # Populate the comboBox with names of all the loaded layers
        self.dlg.comboBox.addItems([layer.name() for layer in layers])

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed

        #for running in Python Console:
        #def layerSelection():
        #canvas = qgis.utils.iface.mapCanvas()
        #layer = qgis.utils.iface.activeLayer()
            
        #for running as a Plugin:
        def layerSelection(self):
            #fetch the current layer index
            selectedLayerIndex = self.dlg.comboBox.currentIndex()
            #define the selected layer
            activeLayer = layers[selectedLayerIndex].layer()
            
            #get features of the selected layer               
            features = activeLayer.selectedFeatures()
            selectedIds = activeLayer.selectedFeatureIds()
            #start editing the selected layer 
            activeLayer.startEditing()
            return activeLayer, features, selectedIds

        def stackPolygon(self):
            activeLayer, features, selectedIds = layerSelection(self)          
            #randomly selected an ID to snap selected (sheep) features to
            wolfFeature = random.choice(features)
            wolfGeom = wolfFeature.geometry()
            wolfCentre = wolfGeom.centroid()
            wolfX = wolfCentre.asPoint().x()
            wolfY = wolfCentre.asPoint().y()
            #wolfPoly = wolfGeom.asMultiPolygon

            #get geometries of Ids you want to "follow" wolfFeature  
            for sheep in selectedIds:
                print(" -- FID: {0}".format(str(sheep)))
                sheepFeature = activeLayer.getFeature(sheep)
                sheepGeom = sheepFeature.geometry()
                sheepCentre = sheepGeom.centroid()
                sheepX = sheepCentre.asPoint().x()
                sheepY = sheepCentre.asPoint().y()
                #sheepPoly = sheepGeom.asMultiPolygon
                
            #determine distance from sheep to wolf
                dX = (wolfX - sheepX)
                dY = (wolfY - sheepY)
                print("    dX/dY: ({0}, {1})".format(str(dX), str(dY)))
                #return dX,dY, sheepFeature
                
            #iterate through selected sheep and move once which =/= wolf
                if (dX != 0.0 or dY != 0.0):
                    print("    tryna herd these sheep")
                    sheepGeom.translate(dX, dY)
                    activeLayer.dataProvider().changeGeometryValues({sheep : sheepGeom})     
        if result:
            print(stackPolygon(self))
