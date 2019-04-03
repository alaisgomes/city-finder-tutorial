# -*- coding: utf-8 -*-
"""
    Chamamos a classe CityFilter (principal do plugin)
    passando a referência da interface principal do QGIS
    caso seja necessário o plugin se comunicar com o
    qgis em si.
"""


def classFactory(iface):
    from .main_plugin import CityFilter

    return CityFilter(iface)
