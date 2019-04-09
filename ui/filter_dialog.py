# -*- coding: utf-8 -*-
from PyQt4.QtGui import (QDialog, QVBoxLayout,
                         QDialogButtonBox, QLabel,
                         QComboBox)
from PyQt4.QtCore import Qt


class FilterDialog(QDialog):
    def __init__(self, opcoes_list, parent=None):
        super(FilterDialog, self).__init__(parent)
        """ Janela de dialogo criada idependente
        (como uma opção ao uso do qt designer)
        """

        # Cria um layout para a  sua janela de input QDialog
        self.layout = QVBoxLayout(self)

        #Cria um label e adiciona no layout
        self.label = QLabel(u"Escolha o valor de filtro:")
        self.layout.addWidget(self.label)

        # Cria combobox com a lista de opcoes a escolher
        # e adicionar no layout
        self.filtro_box = QComboBox()
        self.filtro_box.addItems(opcoes_list)
        self.layout.addWidget(self.filtro_box)

        # Cria botoes de submeter e adiciona ao layout
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def valor_atual(self):
        """ Retorna qual  valor atual na combo box (valor escolhido) """
        return self.filtro_box.currentText()
