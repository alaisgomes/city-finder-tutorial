# City Finder
Plugin-tutorial do QGIS, documentado em português para versão 2.18.X

## Instalação e Configuração do QGIS
Siga as instruções no site oficial, atentados-se à versão utilizada.

- https://qgis.org/debian-ltr/
- https://qgis.org/en/site/forusers/alldownloads.html#linux

```sh
sudo apt-get update
sudo apt-get install qgis python-qgis qgis-plugin-grass python-qt4  python-qt4-dev
sudo apt-get install pyqt4-dev-tools qt4-designer
```

## Inicializando
Um plugin do QGIS possui uma estrutura básica com seguintes arquivos:

- \_\_init\_\_.py (__obrigatório__): Onde o plugin é inicializado. Deve conter o método `ClassFactory()` passando o a classe principal do seu plugin para indicar ao qgis por onde começar a carregar seu plugin.
- main_plugin.py (__obrigtório__): O arquivo que contém a classe principal e o código principal do seu plugin. Este arquivo pode ser nomeado de qualquer forma, desde que o `import` no arquivo de `init` seja feito apropriadamente.
- metadata.txt (__obrigatório__): Contém informações gerais de um plugin, como sua versão, nome e outros metadados.
- resources.qrc: Um arquivo `.xml` que pode ser criado pelo QtDesigner. Contém os caminhos relativos para recursos visuais (como imagens) e outros. Neste tutorial, criaremos este arquivo manualmente para carregar apenas o ícone do plugin.
- resources.py: É o compilado do `resources.qrc`
- icon.png: O arquivo do ícone do nosso plugin, obtido no site [iconfinder.com](//www.iconfinder.com/). Créditos ao autor [Aleksandr Reva](https://www.iconfinder.com/icons/1267304/bank_location_map_office_pin_icon).

## Compilando o arquivo .qrc
Para que os recursos visuais (ícones) sejam carregados no qgis pelo python, é necessário compilar o arquivo `.qrc`. Para isso, abra o terminal do OSGEO4W Shell, caso esteja no Windows, ou terminal normal do Linux e execute o comando, dentro da pasta do projeto:

```sh
pyrcc4 -o resources.py resources.qrc
```

Lembre-se que este comando só estará disponível no Linux após instalar a bilbioteca `pyqt4-dev-tools`.

## Adicionando o ícone
Vamos adicionar o ícone do plugin na barra de ferramentas de plugins. O QGIS reconhece automaticamente caso você declare um método na classe do seu plugin chamada `initGui`. Esse método é utilizado para inicializar a parte principal gráfica da interface do seu plugin. No caso, no momento, vamos apenas adicionar um ícone.

Os ícones nas barras de ferramentas são uma instância de [QAction](https://doc.qt.io/archives/qt-4.8/qaction.html) do QT pois executam uma ação quando ativados. Uma QAction pertence a biblioteca de `QtGui` e pode ter vários atributos associada a ela, como um ícone, uma descrição, um texto de ajuda e etc.

| Não se esqueça de importar o arquivo de resources gerado!

```python
from PyQt4.QtGui import *
import resources
...

def initGui(self):
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
    # executa o que tiver que executar no plugin
    print("Executou")
    pass

```

Vamos abrir o qgis e ativar o plugin! Vá ao menu de Complementos/Plugins e abra a janela de carregar plugins. Em  configurações, ative a opção de visualizar plugins experimentais. Volte na aba de plugins instalados e ative o nosso __City Filter__. Agora podemos ver nosso plugin! Caso clique no botão na barra de ferramentas (ao lado do ícone do Python), ele vai imprimir a mensagem de execução.

Toda vez que você fizer uma atualização no seu plugin, no entanto, será necessário reiniciar o QGIS. Para facilitar o desenvolvimento, existe um outro plugin chamado [Plugin Reloader](https://plugins.qgis.org/plugins/plugin_reloader/) que torna possível recarregar seu plugin que está sendo desenvolvido sem precisar reiniciar o QGIS. Vá em frente em plugins e instale-o!

Para usar o Realoder, no entanto, é necessário fazer uma alteração no nosso próprio plugin. Devemos adicionar um método de 'unload()`: um método que define o que é preciso ser feito para finalizar e fechar o plugin, como por exemplo, se houver um processo sendo executado em uma thread, finalizá-lo apropriadamente antes de reiniciar o plugin. No nosso caso, apenas queremos remover o icone e adicioná-lo novamente no menu, além de atualizar o código a ser executado.

```python
def unload(self):
    """Remove o seu icone da QGIS GUI."""
    self.iface.removeToolBarIcon(self.button_action)
```

## Menu Inicial e Interface
Vamos criar um menu inicial que será aberto assim que clicarmos no botão do nosso plugin usando o [QtDesigner](https://doc.qt.io/archives/qt-4.8/designer-manual.html). Abra o QtDesigner e escolha criar um novo Widget do tipo "[QDockWidget](https://doc.qt.io/archives/qt-4.8/qdockwidget.html)". Faça algo semelhante ao exemplo a seguir, seguindo a nomeação dos objetos:

![Screenshot1](./img/screenshot1.png)

Aqui, teremos uma QComboBox que permitirá filtrar dados com base na opção escolhida e apenas um botão que ativará uma opção de selecionar um município ao clicar sobre ele.

Crie um diretório chamado `ui/` em seu projeto e salve o arquivo como `main_docker.ui`.

Agora, crie um novo arquivo chamado main_docker.py e cole o código abaixo:

```python
# -*- utf-8 -*-
import os
from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'main_docker.ui'))


class CityFilterDockWidget(QtGui.QDockWidget, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(CityFilterDockWidget, self).__init__(parent)
        self.setupUi(self)
```

Aqui, é possível percebeber que estamos criando a classe da nossa interface estendendo a classe de `QtGui.QDockWidget` usando o código de interface gerado pelo designer. Assim, caso você tenha criado no designer um outro tipo de classe (QDialog - janela de diálogo, por exemplo) é necessário modificar o tipo da classe.

Esse código permite que você altere o arquivo `.ui` como quiser no qt designer e o que for construído lá será sempre carregado no Python com as devidas alterações.

Vamos agora carregar o Widget na interface do QGIS. Para isso, vamos importar a classe criada no arquivo criado anteriormente (`main_docker.py`) no plugin principal e vamos inicializar a instância do objeto no construtor de interface `initGui()` da classe:

```python
def initGui(self):
    ...
    self.docker = CityFilterDockWidget()
```

Vamos agora fazer com que o Widget seja adicionado à interface sempre que clicarmos na ação do plugin. Ou seja, adicionar o código que abre a interface dentro do método `executar()`. Ele agora fica assim:

```python
def executar(self):
    """ Função que executa o plugin
    """
    self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.docker)
    self.docker.show()
```

Escolhemos inicializar nosso docker no lado esquerdo da interface principal(`Qt.LeftDockWidgetArea`) e chamamos seu método de inicializar a interface `show()`.

## Criando as Funcionalidades do Plugin
No nosso docker, temos duas funcionalidades: `Filtrar por` `Selecionar Municípios`. A primeira, com base nas opções dentro da combo box, faremos com que as feições doos municípios que se enquadram naquele filtro sejam selecionados.

Antes de qualquer coisa, precisamos realizar o download das camadas que serão utilizadas no nosso projeto. [Acesse o link de download](https://drive.google.com/open?id=1-snIv2yOjBYMlX0UDEm4PBlmXUlrqjiK), descompacte a pasta e carregue as camadas no QGIS como demonstra a imagem a seguir:

![QGIS com camadas](./img/ss2.png)

Abrindo a tabela de atributos das duas camadas, vemos que os estados possuem nome (NM_ESTADO), uma região associada (NM_REGIAO) e um código (CD_GEOCUF). Já os municípios posssuem um nome (NM_MUNICIP) e um código (CD_GEOCMU). O código de cada município está atrelado ao estado ao qual pertence: os dois primeiros dígidos correspondem ao código de cada estado. Dessa forma, conseguimos combinar os dados nas duas tabelas para atingir nosso objetivo.

Vamos então adicionar funcionalidade aos botões que existem no nosso docker. para acessar os botões, lembre-se do nome dado a cada objeto criado no QtDesigner. Por exemplo, se abrirmos o arquivo xml `main_docker.ui` e procurarmos por algum objeto do tipo `QPushButton` podemos encontrar uma declaração do tipo:

```xml
<widget class="QPushButton" name="filtrar_button">
    <property name="text">
        <string>Filtrar</string>
    </property>
</widget>
```

A o valor da propriedade `name` será a que utilizaremos para acessar o nosso botão. No caso, o botão que possui o texto 'Filtrar`se chama `filtrar_button` e o botão que tem o texto se chama `selecionar_button`. Caso os seus botões possuem nomes que não são amigáveis como `button_1`, você pode alterá-los antes de começar a usá-los em código, mas o nome deve sempre coincidir com o que se chama no código Python.

Voltando então, vamos adicionar funcionalidade aos nossos botões. Assim que clicarmos no botão, queremos executar algum método que executará algum código que desejarmos. Então, após instanciar 'self.docker`, vamos chamar seus botões:

```python
def initGui(self):
    ...
    self.docker = CityFilterDockWidget()
    self.docker.filtrar_button.clicked.connect(self.filtrar)

def filtrar(self):
    print("Vamos Filtrar algo")
```

Aqui, estamos dizendo que, ao clicar no botão `filtrar_button`, chamamos a função `filtrar()` que foi criada e ela executa algo, que por enquanto é imprimir uma mensagem no terminal.

Antes de adicionar a funcionalidades no método `filtrar()`, vamos popular a combo box com as opções de filtro. Nossas opções de filtro são por: Estado ou Região. Vamos criar então uma lista (de texto mesmo) para então adicionar esses valores à combobox. Nossa combobox, no arquivo da interface do docket se chama `filtro_box`.

Antes, vale lembrar que, por "Região" ser uma palavra em português que precisa de codificação de caracteres e pelo QGIS 2 usar Python 2, vamos indicar explicitamente que essa string está em unicode com o `u`:

```python
def initGui(self):
    ...

    self.valores_combobox = [u'Estado', u'Região'] # lista com as opções
    self.docker.filtro_box.addItems(self.valores_combobox) # populando combobox

    self.docker.filtrar_button.clicked.connect(self.filtrar) # código anterior
```

### Pegando a Referência das Camadas
Neste tutorial, vamos levar em consideração que as camadas serão carregadas com o nome pré-definido e o nome não será alterado.

Para pegar a referência das camadas carregadas no QGIS, vamos usar o acesso ao canvas (`mapCanvas()`) da interface principal (`iface`) e identificaremos as camadas que vamos usar por seus nomes: __estados__ e __municipios__. Ambas camadas são camadas vetoriais [QgsVectorLayer](https://qgis.org/api/2.18/classQgsVectorLayer.html).

Criamos então um método que retorne as duas camadas necessárias e que, idependente de quais outras camadas estejam carregadas no mapa, retornaremos sempre as camadas de interesse.

```python
def pegar_camadas(self):
    municipios_layer = None
    estados_layer = None

    for layer in self.iface.mapCanvas().layers():

        if layer.name() == 'municipios':
            municipios_layer = layer
        elif layer.name() == 'estados':
            estados_layer = layer

    return municipios_layer, estados_layer
```

No método, inicializamos as variáveis que vão conter as camadas para que, caso as camadas de interesse não estejam carregadas, o retorno será nulo. Iteramos então sobre todas as camadas carregadas no QGIS `iface.mapCanvas().layers()` e verificamos o nome de cada uma. Se o nome coincidir com o nome que desejamos, salvamos a referência da camada para retornar.

Vamos agora fazer a chamada deste método no método `filtrar()` e vamos mandar imprimir o nome de ambas camadas se elas existirem:

```python
def filtrar(self):
    municipios_layer, estados_layer = self.pegar_camadas()
    if municipios_layer and estados_layer: # se ambas nao forem nulas
        print(municipios_layer.name())
        print(estados_layer.name())
```

Ao executar o plugin, se tudo der certo, veremos o nome de cada camada impresso no terminal Python.

### Método filtrar()
No código anterior, vamos adicionar o código a ser adicionado dependendo da opção escolhida. Se for por Estado, executa um método, se for por regiões, executa outro. isso pode ser feito acessando o valor atual (após o botão ter sido apertado) da combobox do docker e fazendo comparações. O método `filtrar()` então vai ficar assim.

```python
def filtrar(self):
    municipios_layer, estados_layer = self.pegar_camadas()

    if municipios_layer and estados_layer: # se ambas nao forem nulas
        # se opção selecionada for por Estado, executa metodo equivalente
        if self.docker.filtro_box.currentText() == u'Estado':
            self.por_estado(municipios_layer, estados_layer)

        #se opção selecionada for por Região, executa metodo equivalente
        elif self.docker.filtro_box.currentText() == u'Região':
            self.por_regiao(municipios_layer, estados_layer)
```

Note que estamos passando a referência das camadas úteis, pois precisaremos delas para acessar os dados e fazer os filtros. As strings, novamente, estão sendo tratadas como _unicode_.

Agora vamos desenvolver a lógica o método `por_estado()`. A lógica deve seguir os seguintes passos:

1. Criar uma classe de janela de diálogo ([QDialog](https://www.riverbankcomputing.com/static/Docs/PyQt4/qdialog.html)) que permita o usuário escolher, em uma combo box, qual estado ou região ele deseja filtrar por;
2. Identificar o index da coluna *NM_STADO* (ou *NM_REGIAO*) na tabela;
3. Pegar a lista dos valores únicos que existem nesta coluna (caso exista um estado com nome repetido, o segundo será ignorado e no caso de regiões, pegaremos apenas os valores distintos)
4. Popular a combobox e criar a instância da janela de diálogo;
5. Executar a janela de diálogo e, se tudo estiver ok, pegar o valor que foi escolhido (nome do estado ou região desejado);
6. Pegar a referência da feição que representa aquele estado (ou feições, se estivermos filtrando por região que contenha mais de um estado);
7. Criar um filtro que será executado na camada de municipios, selecionando todos os municípios que o código comece com o código do estado escolhido (a query de busca é do tipo SQL!). No caso da região, criaremos uma SQL que o filtro englobe um estado __ou__ outro __ou__ outro, etc.

Alguns desses passos, no momento, não terão explicações muito aprofundadas, pois o objetivo deste tutorial é introduzir o desenvolvimento de plugins. Ao final desta página, serão apresentados algumas referências e exercícios de continuação, caso queira aprofundar seus estudos no assunto (QGIS, Python ou QT).




