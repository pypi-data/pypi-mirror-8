# encoding: utf-8
'''
@author:     Jose Emilio Romero Lopez

@copyright:  Copyright 2013-2014, Jose Emilio Romero Lopez.

@license:    GPL

@contact:    jemromerol@gmail.com

  This file is part of APASVO.

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from PySide import QtGui, QtCore


class ComboBoxDelegate(QtGui.QStyledItemDelegate):
    """A delegate class displaying a combo box."""

    def __init__(self, parent=None, values=None):
        QtGui.QStyledItemDelegate.__init__(self, parent)
        if values is None:
            values = []
        self._values = values

    def createEditor(self, parent, option, index):
        editor = QtGui.QComboBox(parent)
        editor.addItems(self._values)
        editor.installEventFilter(self)
        return editor

    def setEditorData(self, comboBox, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        try:
            comboBox.setCurrentIndex(self._values.index(value))
        except:
            comboBox.setCurrentIndex(0)

    def setModelData(self, comboBox, model, index):
        value = comboBox.currentText()
        model.setData(index, value)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
