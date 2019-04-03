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
Um plugin do QGIS possui uma estrutura básica com seguitnes arquivos:

- \_\_init\_\_.py (__obrigatório__): Onde o plugin é inicialiado. Dece conter o método  `ClassFactory()` passando o a classe principal do seu plugin para indicar ao qgis por onde começar a carregar seu plugin.
- main_plugin.py (__obrigtório__): O arquivo que contém a classe principal e o código principal do seu plugin. Este arquivo pode conter qualquer nome, desde que o import no arquivo de init seja feito apropriadamente.
- metadata.txt (__obrigatório__): Contém informações gerais de um plugin, como sua versão, nome e outros metadados.
- resources.qrc: Um arquivo `.xml` que pode ser criado pelo QtDesigner. Contém os caminhos relativos para recursos visuais (como imagens) e outros. Neste tutorial, criaremos este arquivo na mão para carregar apenas o íncone do plugin.
- resources.py: É o compilado do `resources.qrc`
​- icon.png: O arquivo do ícone do nosso plugin, obtido no ite iconfider.com. Créditos ao autor [Aleksandr Reva](https://www.iconfinder.com/icons/1267304/bank_location_map_office_pin_icon).


## Compilando o arquivo .qrc
Para que os recursos visuais (ícones) sejam carregados no qgis pelo python, é necessário compilar o arquivo .qrc. Para isso, abra o terminal do OSGEO4W Shell, caso esteja no windows, ou terminal normal do Linux e execute o comando, dentro da pasta do projeto:

```sh
pyrcc4 -o resources.py resources.qrc
```
## Adicionando o ícone
Vamos adicionar o ícone do plugin na barra de ferramentas de plugins. o QGIS reconhece automaticamente caso você declare um método na classe do seu plugin chamada `initGui`. Esse método é utilizado para inicializar a parte principal gráfica da interface do seu plugin. No caso, no momento, vamos apenas adicionar um ícone.

Os ícones nas barras de ferramentas são uma instância de QAction do qt pois executam uma ação quando ativados. Uma QAction pertence a biblioteca de `QtGui` e pode ter vários atributos associada a ela, como um ícone, uma destrição um texto de ajuda etc.

Não se esqueça de importar o arquivo de resources gerado!


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

Vamos abrir o qgis q ativar o plugin! Vá ao menu de Complementos/Plugins e abra a janela de carregar plugins. Em  configurações, ative a opção de visualizar plugins experimentais. Volte na aba de plugins instalados e ative o nosso City Filter. Agora podemos ver nosso plugin! Caso clique no botão na barra de ferramentas (ao lado do ícone do Python), ele vai imprimir a mensagem de execução.

Toda vez que você fizer uma atualização no seu plugin, no entanto, será necessário reiniciar o QGIS. Para facilitar o desenvolvimento, existe um outro plugin chamado [Plugin Reloader](https://plugins.qgis.org/plugins/plugin_reloader/) que você consegue recarregar seu plugin que está sendo desenvolvido sem precisar reiniciar o QGIS. Vá em frente e plugins e instale-o!

Para usar o Realoder, no entanto, é necessário fazer uma alteração no nosso próprio plugin: adicionar um método de unload: um método que define o que é preciso ser feito para finalizar e fechar o plugin, como por exemplo, se houver um processo sendo executadoem uma thread, finalizá-lo apropriadamente antes de reiniciar o plugin. No nosso caso, apenas queremos remover o icone e adicioná-lo novamente no menu, além de atualizar o código a ser executado.

```python
def unload(self):
    """Remove o seu icone da QGIS GUI."""
    self.iface.removeToolBarIcon(self.button_action)
```





