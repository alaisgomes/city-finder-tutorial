# -*- coding: utf-8 -*-

# from qgis.core import *
from qgis.gui import QgsMapTool, QgsMapToolIdentify

"""
    Ferramenta de seleção customizada do QGIS
"""

class SelectTool(QgsMapTool):
    def __init__(self, canvas, municipios_layer):
        QgsMapTool.__init__(self, canvas)
        self.municipios_layer = municipios_layer
        self.canvas = canvas

    def canvasPressEvent(self, event):
        """ Sobrescrevendo método da QgsMapTool herdada para que execute
            as funcionalidades desejadas.
            Usamos a QgsMapToolIdentify para identificar feições de
            camadas no mapa. Para mais Informações consulte a documentação
        """

        if not self.municipios_layer.isValid():
            return
        # pega a camada de municipios
        layer = self.municipios_layer

        # Aqui estamos definindo como a identificação deve ser feita
        inicio_identificacao = QgsMapToolIdentify.TopDownStopAtFirst

        # usando  a ferramenta para ver se o local onde clicamos (x,y do evento de clique)
        # pertence a uma feição da camada
        feicoes_clicadas = QgsMapToolIdentify(self.canvas).identify(
            event.x(),
            event.y(),
            [layer],
            inicio_identificacao
        )

        # se existir, seleciona só a primeira feição retornada na identificação
        if len(feicoes_clicadas) > 0:
            municipio_selecionado = feicoes_clicadas[0].mFeature
            self.municipios_layer.select(municipio_selecionado.id())