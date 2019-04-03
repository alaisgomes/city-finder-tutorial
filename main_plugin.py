# -*- coding: utf-8 -*-
from qgis.core import *

class CityFilter:
    def __init__(self, iface):
        """ Classe principal que inicializa o plugin

        Atibutos de inicialização:
            iface: referência à interface principal do QGIS.
        """
        self.iface = iface

