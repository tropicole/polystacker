# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PolyStacker
                                 A QGIS plugin
 This plugin stacks and scales polygons.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-01-31
        copyright            : (C) 2020 by C.Glover & M.Fisher of Aethon Aerial Solutions
        email                : cole.r.glover@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PolyStacker class from file PolyStacker.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .poly_stacker import PolyStacker
    return PolyStacker(iface)
