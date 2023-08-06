# -*- coding: utf-8 -*-
#
# AWL simulator - GUI CPU configuration widget
#
# Copyright 2012-2014 Michael Buesch <m@bues.ch>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from __future__ import division, absolute_import, print_function, unicode_literals
from awlsim.common.compat import *

from awlsim.gui.util import *


class ClockMemSpinBox(QSpinBox):
	def __init__(self, parent=None):
		QSpinBox.__init__(self, parent)

		self.setMinimum(-1)
		self.setMaximum(0xFFFF)
		self.setValue(-1)
		self.setPrefix("MB ")

	def textFromValue(self, value):
		if value < 0:
			return "<disabled>"
		return QSpinBox.textFromValue(self, value)

	def valueFromText(self, text):
		if text == "<disabled>":
			return -1
		return QSpinBox.valueFromText(self, text)

class CpuConfigDialog(QDialog):
	def __init__(self, parent, simClient):
		QDialog.__init__(self, parent)
		self.simClient = simClient
		self.setWindowTitle("CPU configuration")

		self.setLayout(QGridLayout(self))

		label = QLabel("Number of accumulator registers", self)
		self.layout().addWidget(label, 0, 0)
		self.accuCombo = QComboBox(self)
		self.accuCombo.addItem("2 accus", 2)
		self.accuCombo.addItem("4 accus", 4)
		self.layout().addWidget(self.accuCombo, 0, 1)

		label = QLabel("Clock memory byte", self)
		self.layout().addWidget(label, 1, 0)
		self.clockMemSpin = ClockMemSpinBox(self)
		self.layout().addWidget(self.clockMemSpin, 1, 1)

		label = QLabel("Mnemonics", self)
		self.layout().addWidget(label, 2, 0)
		self.mnemonicsCombo = QComboBox(self)
		self.mnemonicsCombo.addItem("Automatic", S7CPUSpecs.MNEMONICS_AUTO)
		self.mnemonicsCombo.addItem("English", S7CPUSpecs.MNEMONICS_EN)
		self.mnemonicsCombo.addItem("German", S7CPUSpecs.MNEMONICS_DE)
		self.layout().addWidget(self.mnemonicsCombo, 2, 1)

		self.obTempCheckBox = QCheckBox("Enable writing of OB TEMP "
			"entry-variables", self)
		self.layout().addWidget(self.obTempCheckBox, 3, 0, 1, 2)

		self.extInsnsCheckBox = QCheckBox("Enable extended "
			"non-standard instructions", self)
		self.layout().addWidget(self.extInsnsCheckBox, 4, 0, 1, 2)

		self.closeButton = QPushButton("Close", self)
		self.layout().addWidget(self.closeButton, 5, 1)

		self.closeButton.released.connect(self.accept)

	def loadFromProject(self, project):
		specs = project.getCpuSpecs()

		index = self.accuCombo.findData(specs.nrAccus)
		assert(index >= 0)
		self.accuCombo.setCurrentIndex(index)

		self.clockMemSpin.setValue(specs.clockMemByte)

		index = self.mnemonicsCombo.findData(specs.getConfiguredMnemonics())
		assert(index >= 0)
		self.mnemonicsCombo.setCurrentIndex(index)

		self.obTempCheckBox.setCheckState(
			Qt.Checked if project.getObTempPresetsEn() else\
			Qt.Unchecked
		)

		self.extInsnsCheckBox.setCheckState(
			Qt.Checked if project.getExtInsnsEn() else\
			Qt.Unchecked
		)

	def saveToProject(self, project):
		mnemonics = self.mnemonicsCombo.itemData(self.mnemonicsCombo.currentIndex())
		nrAccus = self.accuCombo.itemData(self.accuCombo.currentIndex())
		clockMemByte = self.clockMemSpin.value()
		obTempEnabled = self.obTempCheckBox.checkState() == Qt.Checked
		extInsnsEnabled = self.extInsnsCheckBox.checkState() == Qt.Checked

		specs = project.getCpuSpecs()
		specs.setConfiguredMnemonics(mnemonics)
		specs.setNrAccus(nrAccus)
		specs.setClockMemByte(clockMemByte)
		project.setObTempPresetsEn(obTempEnabled)
		project.setExtInsnsEn(extInsnsEnabled)
