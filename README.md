# City Finder
Plugin-tutorial do QGIS, documentado em português para versão 2.18.X


## Inicializando
Um plugin do QGIS possui uma estrutura básica com seguitnes arquivos:

- \_\_init\_\_.py (__obrigatório__): Onde o plugin é inicialiado. Dece conter o método  `ClassFactory()` passando o a classe principal do seu plugin para indicar ao qgis por onde começar a carregar seu plugin.
- main_plugin.py (__obrigtório__): O arquivo que contém a classe principal e o código principal do seu plugin. Este arquivo pode conter qualquer nome, desde que o import no arquivo de init seja feito apropriadamente.
- metadata.txt (__obrigatório__): Contém informações gerais de um plugin, como sua versão, nome e outros metadados.
- resources.qrc: Um arquivo `.xml` que pode ser criado pelo QtDesigner. Contém os caminhos relativos para recursos visuais (como imagens) e outros. Neste tutorial, criaremos este arquivo na mão para carregar apenas o íncone do plugin.
- resources.py: É o compilado do `resources.qrc`
​- icon.png: O arquivo do ícone do nosso plugin, obtido no ite iconfider.com. Créditos ao autor [Aleksandr Reva](https://www.iconfinder.com/icons/1267304/bank_location_map_office_pin_icon).



