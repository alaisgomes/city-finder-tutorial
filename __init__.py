# -*- coding: utf-8 -*-

def classFactory(iface):
    from .main_plugin import FeatureFinder
    return FeatureFinder(iface)
