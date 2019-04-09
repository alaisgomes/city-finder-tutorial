# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from ui.main_docker import CityFilterDockWidget
from ui.filter_dialog import FilterDialog
import resources


class CityFilter():
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

        # Cria docker, cria lista com os valores que serão mostrados na
        # combobox e insere esses valores na mesma
        self.docker = CityFilterDockWidget()
        self.valores_combobox = [u'Estado', u'Região']
        self.docker.filtro_box.addItems(self.valores_combobox)
        self.docker.filtrar_button.clicked.connect(self.filtrar)

    def executar(self):
        """ Função que executa o plugin ao clicar no botão de ação """
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.docker)
        self.docker.show()

    def filtrar(self):
        """ Opção de filtrar municipios por estado ou região """
        # pega as camadas de interesse
        municipios_layer, estados_layer = self.pegar_camadas()

        # se ambas camadas existirem, continua
        if municipios_layer and estados_layer:

            # se opção selecionada for por Estado, executa metodo equivalente
            if self.docker.filtro_box.currentText() == u'Estado':
                self.por_estado(municipios_layer, estados_layer)

            #se opção selecionada for por Região, executa metodo equivalente
            elif self.docker.filtro_box.currentText() == u'Região':
                self.por_regiao(municipios_layer, estados_layer)

    def pegar_camadas(self):
        """ Método que retorna as camadas de interesse
            (ou nulo se não existirem)

            Retorna:
                camada1 (QgsVectorLayer) - contendo os municipios
                camada2 (QgsVectorLayer) - contendo os estados
        """
        municipios_layer = None
        estados_layer = None

        for layer in self.iface.mapCanvas().layers():

            if layer.name() == 'municipios':
                municipios_layer = layer

            elif layer.name() == 'estados':
                estados_layer = layer

        return municipios_layer, estados_layer

    def pegar_por_nome(self, camada, tipo_campo, nome):
        """ Filtra uma camada de interesse de acordo com um campo
            e seu valor equivalente na tabela de atributos
            retornando as feições correspondentes ao filtro

            Argumentos:
                camada (QgsVectorLayer): a camada que vai retornar as feições
                tipo_campo (string): o nome do campo que será feito o filtro
                nome (string): o valor que deve corresponder no campo da tabela

            Retorna:
                (list): lista de feições que correspondem ao filtro
        """

        expression = QgsExpression(
            '"{tipo}" LIKE \'{nome}\''.format(
                tipo=tipo_campo, nome=nome)
            )

        features_iterator = camada.getFeatures(QgsFeatureRequest(expression))

        return [feat for feat in features_iterator]

    def por_estado(self, municipios, estados):
        """ Mostra uma janela de filtro para o usuário para que escolha
            o estado de interesse e realize a seleção das feições correspondentes

            Argumentos:
                municipios(QgsVectorLayer): camada de municipios
                estados(QgsVectorLayer): camada de estados

        """
        # pega o index na tabela de atributos da coluna com nome de NM_ESTADO
        index_coluna = estados.fieldNameIndex('NM_ESTADO')

        # pega valores unicos na coluna NM_ESTADO
        lista_de_estados = estados.uniqueValues(index_coluna)

        # Cria uma janela de dialogo com a lista de estados existentes na camada
        janela_filtro = FilterDialog(lista_de_estados)

        # se execução da janela de dialogo tiver sucesso, continua
        if janela_filtro.exec_():

            # pega o valor atual (nome escolhido) na janela de filtro
            nome_estado = janela_filtro.valor_atual()

            # obtem a feição/feature correspondende ao estado escolhido
            estado_escolhido = self.pegar_por_nome(estados, 'NM_ESTADO', nome_estado)[0]

            # pega código ID do estado
            id_estado = estado_escolhido['CD_GEOCUF']

            # cria uma expressão estilo SQL que filtra os municipios por estado 'id%'
            filtro_municipio = '"CD_GEOCMU" LIKE \'{id}%\''.format(id=id_estado)
            municipios.selectByExpression(filtro_municipio) # seleciona as features desejadas


    def por_regiao(self, municipios, estados):
        """ Mostra uma janela de filtro para o usuário para que escolha
            a regiao de interesse e realize a seleção das feições correspondentes

            Argumentos:
                municipios(QgsVectorLayer): camada de municipios
                estados(QgsVectorLayer): camada de estados

        """
        # pega o index na tabela de atributos da coluna com nome de NM_REGIAO
        index_coluna = estados.fieldNameIndex('NM_REGIAO')

        # pega valores unicos na coluna NM_REGIAO
        lista_de_regioes = estados.uniqueValues(index_coluna)

        # Cria uma janela de dialogo com a lista de regiões existentes na camada
        janela_filtro = FilterDialog(lista_de_regioes)

        # se sucesso, continua
        if janela_filtro.exec_():
            # pega o nome da região escolhida
            nome_regiao = janela_filtro.valor_atual()

            # pega a lista dos estados dentro da região
            estados_na_regiao = self.pegar_por_nome(estados, 'NM_REGIAO', nome_regiao)

            # inicia a expressão SQL
            filtro_municipio = ''

            # para cada estado, adiciona uma expressão de filtro de municipios
            for estado in estados_na_regiao:
                id_estado = estado['CD_GEOCUF']

                # se ja existir algo na expressão, adiciona um OR pra continuar criando
                if filtro_municipio:
                    filtro_municipio += ' OR '

                filtro_municipio += '"CD_GEOCMU" LIKE \'{id}%\''.format(id=id_estado)

            # seleciona todos os municipios que correspondem a expressao
            municipios.selectByExpression(filtro_municipio)


    def unload(self):
        """Remove o seu icone da QGIS GUI."""
        self.iface.removeToolBarIcon(self.button_action)


