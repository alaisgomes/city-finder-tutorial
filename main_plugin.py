# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import resources

class CityFilter:
    def __init__(self, iface):
        """ Construtor da classe.
        Classe principal que inicializa o plugin

        Atibutos de inicialização:
            iface: referência à interface principal do QGIS.
        """
        self.iface = iface

    def initGui(self):
        """ Inicializa a interface do plugin
            Definimos a QAction que vai iniciar a execução do plugin
            passando:
                - o ícone que desejamos adicionar
                - O Texto que descreve a ação
                - o parent que aquela ação pertence, se existir. No Caso, o parent
                é a janela principal do QGIS

        """
        # https://www.riverbankcomputing.com/static/Docs/PyQt4/qaction.html
        icon_path = ":/plugins/city_finder/icon.png"
        self.button_action = QAction(
                            QIcon(icon_path),
                            "Plugin de filtro de cidades",
                            self.iface.mainWindow()
                        )
        # Adiciona o texto de ajuda a mais
        self.button_action.setWhatsThis("Este plugin realiza o filtro de municípios...")
        # Quando a ação for acionada, executa alguma coisa, no caso, o metodo executar
        self.button_action.triggered.connect(self.executar)
        # Adicionar na interface do QGIS, no menu ToolBar de plugins, a ação desejada
        self.iface.addToolBarIcon(self.button_action)


    def executar(self):
        """ Função que executa o plugin
        """
        print("Executei!")
        pass

    def unload(self):
        """Remove o seu icone da QGIS GUI."""
        self.iface.removeToolBarIcon(self.button_action)


