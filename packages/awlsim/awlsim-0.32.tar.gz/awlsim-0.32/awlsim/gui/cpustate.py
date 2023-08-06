# -*- coding: utf-8 -*-
#
# AWL simulator - GUI CPU state widgets
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

from awlsim.gui.valuelineedit import *
from awlsim.gui.util import *


class StateWindow(QWidget):
	# Window-close signal
	closed = Signal(QWidget)
	# Config-change (address, type, etc...) signal
	configChanged = Signal(QWidget)

	def __init__(self, client, parent=None):
		QWidget.__init__(self, parent)
		self.setLayout(QGridLayout(self))
		pixmap = QPixmap(16, 16)
		pixmap.fill(QColor(0, 0, 192))
		self.setWindowIcon(QIcon(pixmap))
		self.client = client

	def update(self):
		size, hint = self.size(), self.minimumSizeHint()
		if size.width() < hint.width() or\
		   size.height() < hint.height():
			self.resize(hint)

	# Get a list of MemoryArea instances for the memory
	# areas covered by this window.
	def getMemoryAreas(self):
		return []

	# Try to write memory to this window.
	# The window might reject the request, if this memory
	# doesn't belong to it.
	def setMemory(self, memArea):
		return False

	def setMemories(self, memAreas):
		for memArea in memAreas:
			self.setMemory(memArea)

	def closeEvent(self, ev):
		self.closed.emit(self)
		ev.accept()
		self.deleteLater()

class State_CPU(StateWindow):
	def __init__(self, client, parent=None):
		StateWindow.__init__(self, client, parent)
		self.setWindowTitle("CPU Details")

		self.label = QLabel(self)
		font = self.label.font()
		font.setFamily("Mono")
		font.setFixedPitch(True)
		font.setKerning(False)
		self.label.setFont(font)
		self.layout().addWidget(self.label, 0, 0)

		self.label.setText("No CPU status available, yet.")

	def setDumpText(self, text):
		self.label.setText(text)
		self.update()

class AbstractDisplayWidget(QWidget):
	EnumGen.start
	ADDRSPACE_E		= EnumGen.item
	ADDRSPACE_A		= EnumGen.item
	ADDRSPACE_M		= EnumGen.item
	ADDRSPACE_DB		= EnumGen.item
	EnumGen.end

	addrspace2name = {
		ADDRSPACE_E	: ("I", "Inputs"),
		ADDRSPACE_A	: ("Q", "Outputs"),
		ADDRSPACE_M	: ("M", "Flags"),
		ADDRSPACE_DB	: ("DB", "Data block"),
	}

	addrspace2memarea = {
		ADDRSPACE_E	: MemoryArea.TYPE_E,
		ADDRSPACE_A	: MemoryArea.TYPE_A,
		ADDRSPACE_M	: MemoryArea.TYPE_M,
		ADDRSPACE_DB	: MemoryArea.TYPE_DB,
	}

	changed = Signal()

	def __init__(self, client, addrSpace, addr, width, db, parent=None):
		QWidget.__init__(self, parent)
		self.setLayout(QGridLayout(self))

		self.client = client
		self.addrSpace = addrSpace
		self.addr = addr
		self.width = width
		self.db = db

	def get(self):
		pass

	# Set a byte in this display widget.
	# offset -> The relative byte offset
	# value -> The byte value
	def setByte(self, offset, value):
		pass

	def _showValueValidity(self, valid):
		if valid:
			pal = self.palette()
			pal.setColor(QPalette.Text, Qt.black)
			self.setPalette(pal)
		else:
			pal = self.palette()
			pal.setColor(QPalette.Text, Qt.red)
			self.setPalette(pal)

class BitDisplayWidget(AbstractDisplayWidget):
	def __init__(self, client, addrSpace, addr, width, db,
		     parent=None,
		     displayPushButtons=True):
		AbstractDisplayWidget.__init__(self, client, addrSpace,
					       addr, width, db, parent)

		self.cbs = {}
		self.pbs = {}
		self.prevButtonStates = {}
		y = 0
		for i in range(self.width - 1, -1, -1):
			cb = QCheckBox(str(i), self)
			self.layout().addWidget(cb, y + 0, (self.width - i - 1) % 8)
			self.cbs[i] = cb
			cb.stateChanged.connect(self.changed)
			if displayPushButtons:
				pb = QPushButton("", self)
				self.layout().addWidget(pb, y + 1, (self.width - i - 1) % 8)
				self.pbs[i] = pb
				self.prevButtonStates[i] = False
				pb.pressed.connect(self.__buttonUpdate)
				pb.released.connect(self.__buttonUpdate)
			if i and i % 8 == 0:
				y += 2

		self.update()

	def __buttonUpdate(self):
		for bitNr, pb in self.pbs.items():
			pressed = bool(pb.isDown())
			if pressed == self.prevButtonStates[bitNr]:
				continue
			self.prevButtonStates[bitNr] = pressed

			if self.cbs[bitNr].checkState() == Qt.Checked:
				self.cbs[bitNr].setCheckState(Qt.Unchecked)
			else:
				self.cbs[bitNr].setCheckState(Qt.Checked)

	def get(self):
		value = 0
		for bitNr, cb in self.cbs.items():
			if cb.checkState() == Qt.Checked:
				value |= (1 << bitNr)
		return value

	def setByte(self, offset, value):
		bitBase = ((self.width // 8) - 1 - offset) * 8
		for bitNr in range(bitBase, bitBase + 8):
			if value & 1:
				self.cbs[bitNr].setCheckState(Qt.Checked)
			else:
				self.cbs[bitNr].setCheckState(Qt.Unchecked)
			value >>= 1

class NumberDisplayWidget(AbstractDisplayWidget):
	def __init__(self, client, base, addrSpace, addr, width, db, parent=None):
		AbstractDisplayWidget.__init__(self, client, addrSpace,
					       addr, width, db, parent)

		self.base = base
		self.__currentValue = -1

		self.line = ValueLineEdit(self.__validateInput, self)
		self.layout().addWidget(self.line)

		self.line.valueChanged.connect(self.changed)

		self.update()

	def __convertValue(self, textValue):
		try:
			if self.base == 2:
				textValue = textValue.replace('_', '').replace(' ', '')
			value = int(textValue, self.base)
			if self.base == 10:
				if value > (1 << (self.width - 1)) - 1 or\
				   value < -(1 << (self.width - 1)):
					raise ValueError
			else:
				if value > (1 << self.width) - 1:
					raise ValueError
		except ValueError as e:
			return None
		return value

	def __validateInput(self, inputString, pos):
		if self.__convertValue(inputString) is None:
			return QValidator.Intermediate
		return QValidator.Acceptable

	def get(self):
		value = self.__convertValue(self.line.text())
		if value is None:
			return 0
		return value

	def setByte(self, offset, value):
		mask = ~(0xFF << (self.width - 8 - (offset * 8))) & 0xFFFFFFFF
		value = (value << (self.width - 8 - (offset * 8))) & 0xFFFFFFFF
		value = (self.__currentValue & mask) | value
		if self.__currentValue != value:
			self.__currentValue = value
			self.__displayValue()

	def __displayValue(self):
		value = self.__currentValue
		if self.base == 2:
			string = intToDualString(value, self.width)
		elif self.base == 10:
			if self.width == 8:
				string = "%d" % byteToSignedPyInt(value)
			elif self.width == 16:
				string = "%d" % wordToSignedPyInt(value)
			elif self.width == 32:
				string = "%d" % dwordToSignedPyInt(value)
			else:
				assert(0)
		elif self.base == 16:
			if self.width == 8:
				string = "%02X" % (value & 0xFF)
			elif self.width == 16:
				string = "%04X" % (value & 0xFFFF)
			elif self.width == 32:
				string = "%08X" % (value & 0xFFFFFFFF)
			else:
				assert(0)
		else:
			assert(0)
		self.line.setText(string)

class HexDisplayWidget(NumberDisplayWidget):
	def __init__(self, client, addrSpace, addr, width, db, parent=None):
		NumberDisplayWidget.__init__(self, client, 16, addrSpace,
					     addr, width, db, parent)

class DecDisplayWidget(NumberDisplayWidget):
	def __init__(self, client, addrSpace, addr, width, db, parent=None):
		NumberDisplayWidget.__init__(self, client, 10, addrSpace,
					     addr, width, db, parent)

class BinDisplayWidget(NumberDisplayWidget):
	def __init__(self, client, addrSpace, addr, width, db, parent=None):
		NumberDisplayWidget.__init__(self, client, 2, addrSpace,
					     addr, width, db, parent)

class RealDisplayWidget(AbstractDisplayWidget):
	def __init__(self, client, addrSpace, addr, width, db, parent=None):
		AbstractDisplayWidget.__init__(self, client, addrSpace,
					       addr, width, db, parent)

		self.__currentValue = -1

		self.line = ValueLineEdit(self.__validateInput, self)
		self.layout().addWidget(self.line)

		self.line.valueChanged.connect(self.changed)

		self.update()

	def __convertValue(self, textValue):
		try:
			value = pyFloatToDWord(float(textValue))
		except ValueError as e:
			return None
		return value

	def __validateInput(self, inputString, pos):
		if self.__convertValue(inputString) is None:
			return QValidator.Intermediate
		return QValidator.Acceptable

	def get(self):
		value = self.__convertValue(self.line.text())
		if value is None:
			return 0
		return value

	def setByte(self, offset, value):
		mask = ~(0xFF << (self.width - 8 - (offset * 8))) & 0xFFFFFFFF
		value = (value << (self.width - 8 - (offset * 8))) & 0xFFFFFFFF
		value = (self.__currentValue & mask) | value
		if self.__currentValue != value:
			self.__currentValue = value
			self.__displayValue()

	def __displayValue(self):
		value = self.__currentValue
		if self.width == 32:
			string = str(dwordToPyFloat(value))
		else:
			string = "Not DWORD"
		self.line.setText(string)

class State_Mem(StateWindow):
	def __init__(self, client, addrSpace, parent=None):
		StateWindow.__init__(self, client, parent)

		self.addrSpace = addrSpace

		x = 0

		if addrSpace == AbstractDisplayWidget.ADDRSPACE_DB:
			self.dbSpin = QSpinBox(self)
			self.dbSpin.setPrefix("DB ")
			self.dbSpin.setMinimum(0)
			self.dbSpin.setMaximum(0xFFFF)
			self.layout().addWidget(self.dbSpin, 0, x)
			x += 1

		self.addrSpin = QSpinBox(self)
		self.addrSpin.setMinimum(0)
		self.addrSpin.setMaximum(0xFFFF)
		self.layout().addWidget(self.addrSpin, 0, x)
		x += 1

		self.widthCombo = QComboBox(self)
		self.widthCombo.addItem("Byte", 8)
		self.widthCombo.addItem("Word", 16)
		self.widthCombo.addItem("DWord", 32)
		self.layout().addWidget(self.widthCombo, 0, x)
		x += 1

		self.fmtCombo = QComboBox(self)
		self.fmtCombo.addItem("Checkboxes", "cb")
		self.fmtCombo.addItem("Dual", "bin")
		self.fmtCombo.addItem("Decimal", "dec")
		self.fmtCombo.addItem("Hexadecimal", "hex")
		self.fmtCombo.addItem("Real", "real")
		self.layout().addWidget(self.fmtCombo, 0, x)
		x += 1

		self.contentLayout = QGridLayout()
		self.contentLayout.setContentsMargins(QMargins())
		self.layout().addLayout(self.contentLayout, 1, 0, 1, x)

		self.contentWidget = None

		if addrSpace == AbstractDisplayWidget.ADDRSPACE_DB:
			self.dbSpin.valueChanged.connect(self.rebuild)
		self.addrSpin.valueChanged.connect(self.rebuild)
		self.widthCombo.currentIndexChanged.connect(self.rebuild)
		self.fmtCombo.currentIndexChanged.connect(self.rebuild)

		self.__changeBlocked = 0
		self.rebuild()

	def rebuild(self):
		if self.contentWidget:
			self.contentLayout.removeWidget(self.contentWidget)
			self.contentWidget.deleteLater()
		self.contentWidget = None

		addr = self.addrSpin.value()
		index = self.fmtCombo.currentIndex()
		fmt = self.fmtCombo.itemData(index)
		index = self.widthCombo.currentIndex()
		width = self.widthCombo.itemData(index)
		if self.addrSpace == AbstractDisplayWidget.ADDRSPACE_DB:
			db = self.dbSpin.value()
		else:
			db = None

		if fmt == "real":
			# If REAL is selected with byte or word width,
			# change to dword width.
			if width != 32:
				index = self.widthCombo.findData(32)
				# This will re-trigger the "rebuild" slot.
				self.widthCombo.setCurrentIndex(index)
				return

		name, longName = AbstractDisplayWidget.addrspace2name[self.addrSpace]
		width2suffix = {
			8	: "B",
			16	: "W",
			32	: "D",
		}
		name += width2suffix[width]
		self.addrSpin.setPrefix(name + "  ")
		self.setWindowTitle(longName)

		if fmt == "cb":
			self.contentWidget = BitDisplayWidget(self.client,
							      self.addrSpace,
							      addr, width, db, self,
							      displayPushButtons=True)
			self.contentLayout.addWidget(self.contentWidget)
		elif fmt == "hex":
			self.contentWidget = HexDisplayWidget(self.client,
							      self.addrSpace,
							      addr, width, db, self)
			self.contentLayout.addWidget(self.contentWidget)
		elif fmt == "dec":
			self.contentWidget = DecDisplayWidget(self.client,
							      self.addrSpace,
							      addr, width, db, self)
			self.contentLayout.addWidget(self.contentWidget)
		elif fmt == "bin":
			self.contentWidget = BinDisplayWidget(self.client,
							      self.addrSpace,
							      addr, width, db, self)
			self.contentLayout.addWidget(self.contentWidget)
		elif fmt == "real":
			self.contentWidget = RealDisplayWidget(self.client,
							       self.addrSpace,
							       addr, width, db, self)
			self.contentLayout.addWidget(self.contentWidget)
		else:
			assert(0)
		self.contentWidget.changed.connect(self.__changed)
		self.contentWidget.setEnabled(True)
		self.update()
		QTimer.singleShot(0, self.__finalizeRebuild)

		self.configChanged.emit(self)

	def __finalizeRebuild(self):
		self.resize(self.sizeHint())

	def __changed(self):
		if self.__changeBlocked or not self.contentWidget:
			return
		value = self.contentWidget.get()
		width = self.widthCombo.itemData(self.widthCombo.currentIndex())

		memArea = self.__makeMemoryArea()
		memArea.data = bytearray(width // 8)
		WordPacker.toBytes(memArea.data, width, 0, value)

		self.client.writeMemory((memArea,))

	def __makeMemoryArea(self):
		dbIndex = 0
		if self.addrSpace == AbstractDisplayWidget.ADDRSPACE_DB:
			dbIndex = self.dbSpin.value()
		addr = self.addrSpin.value()
		nrBits = self.widthCombo.itemData(self.widthCombo.currentIndex())

		return MemoryArea(memType = AbstractDisplayWidget.addrspace2memarea[self.addrSpace],
				  flags = 0,
				  index = dbIndex,
				  start = addr,
				  length = nrBits // 8)

	def getMemoryAreas(self):
		return ( self.__makeMemoryArea(), )

	def setMemory(self, memArea):
		if not self.contentWidget:
			return False
		thisArea = self.__makeMemoryArea()
		if not thisArea.overlapsWith(memArea):
			return False
		thisStart, thisEnd = thisArea.start, thisArea.start + thisArea.length - 1

		if memArea.flags & (memArea.FLG_ERR_READ | memArea.FLG_ERR_WRITE):
			self.contentWidget.setEnabled(False)
			return False

		self.__changeBlocked += 1
		addr = memArea.start
		for value in memArea.data:
			if addr > thisEnd:
				break
			if addr >= thisStart:
				self.contentWidget.setByte(addr - thisStart,
							   value)
			addr += 1
		self.__changeBlocked -= 1
		self.update()
		return True

class State_LCD(StateWindow):
	def __init__(self, client, parent=None):
		StateWindow.__init__(self, client, parent)
		self.setWindowTitle("LCD")

		self.displayedValue = 0

		self.addrSpin = QSpinBox(self)
		self.addrSpin.setPrefix("Q ")
		self.addrSpin.setMinimum(0)
		self.addrSpin.setMaximum(0xFFFF)
		self.layout().addWidget(self.addrSpin, 0, 0)

		self.widthCombo = QComboBox(self)
		self.widthCombo.addItem("Byte", 8)
		self.widthCombo.addItem("Word", 16)
		self.widthCombo.addItem("DWord", 32)
		self.layout().addWidget(self.widthCombo, 0, 1)

		self.endianCombo = QComboBox(self)
		self.endianCombo.addItem("Big-endian", "be")
		self.endianCombo.addItem("Little-endian", "le")
		self.layout().addWidget(self.endianCombo, 1, 0)

		self.fmtCombo = QComboBox(self)
		self.fmtCombo.addItem("BCD", "bcd")
		self.fmtCombo.addItem("Signed BCD", "signed-bcd")
		self.fmtCombo.addItem("Binary", "bin")
		self.fmtCombo.addItem("Signed binary", "signed-bin")
		self.layout().addWidget(self.fmtCombo, 1, 1)

		self.lcd = QLCDNumber(self)
		self.lcd.setMinimumHeight(50)
		self.layout().addWidget(self.lcd, 2, 0, 1, 2)

		self.addrSpin.valueChanged.connect(self.rebuild)
		self.widthCombo.currentIndexChanged.connect(self.rebuild)
		self.endianCombo.currentIndexChanged.connect(self.rebuild)
		self.fmtCombo.currentIndexChanged.connect(self.rebuild)

		self.__changeBlocked = 0
		self.rebuild()

	def getDataWidth(self):
		index = self.widthCombo.currentIndex()
		return self.widthCombo.itemData(index)

	def getFormat(self):
		index = self.fmtCombo.currentIndex()
		return self.fmtCombo.itemData(index)

	def getEndian(self):
		index = self.endianCombo.currentIndex()
		return self.endianCombo.itemData(index)

	def rebuild(self):
		self.update()
		self.configChanged.emit(self)

	def __makeMemoryArea(self):
		nrBits = self.widthCombo.itemData(self.widthCombo.currentIndex())
		addr = self.addrSpin.value()

		return MemoryArea(memType = MemoryArea.TYPE_A,
				  flags = 0,
				  index = 0,
				  start = addr,
				  length = nrBits // 8)

	def getMemoryAreas(self):
		return ( self.__makeMemoryArea(), )

	def setMemory(self, memArea):
		thisArea = self.__makeMemoryArea()
		if not thisArea.overlapsWith(memArea):
			return False
		thisStart, thisEnd = thisArea.start, thisArea.start + thisArea.length - 1

		if memArea.flags & (memArea.FLG_ERR_READ | memArea.FLG_ERR_WRITE):
			#TODO
			return False

		self.__changeBlocked += 1
		addr = memArea.start
		for value in memArea.data:
			if addr > thisEnd:
				break
			if addr >= thisStart:
				self.__setByte(addr - thisStart,
					       value)
			addr += 1
		self.__changeBlocked -= 1
		self.update()
		return True

	def __setByte(self, offset, value):
		width = self.getDataWidth()
		mask = ~(0xFF << (width - 8 - (offset * 8))) & 0xFFFFFFFF
		value = (value << (width - 8 - (offset * 8))) & 0xFFFFFFFF
		value = (self.displayedValue & mask) | value
		if self.displayedValue != value:
			self.displayedValue = value
			self.__displayValue()

	def __displayValue(self):
		addr = self.addrSpin.value()
		width = self.getDataWidth()
		fmt = self.getFormat()
		endian = self.getEndian()
		value = self.displayedValue

		if endian == "le":
			if width == 16:
				value = swapEndianWord(value)
			elif width == 32:
				value = swapEndianDWord(value)

		if fmt == "bcd":
			if width == 8:
				value = "%02X" % (value & 0xFF)
			elif width == 16:
				value = "%04X" % (value & 0xFFFF)
			elif width == 32:
				value = "%08X" % (value & 0xFFFFFFFF)
			else:
				assert(0)
		elif fmt == "signed-bcd":
			if width == 8:
				sign = '-' if (value & 0xF0) else ''
				value = "%s%01X" % (sign, value & 0x0F)
			elif width == 16:
				sign = '-' if (value & 0xF000) else ''
				value = "%s%03X" % (sign, value & 0x0FFF)
			elif width == 32:
				sign = '-' if (value & 0xF0000000) else ''
				value = "%s%07X" % (sign, value & 0x0FFFFFFF)
			else:
				assert(0)
		elif fmt == "bin":
			if width == 8:
				value = "%d" % (value & 0xFF)
			elif width == 16:
				value = "%d" % (value & 0xFFFF)
			elif width == 32:
				value = "%d" % (value & 0xFFFFFFFF)
			else:
				assert(0)
		elif fmt == "signed-bin":
			if width == 8:
				value = "%d" % byteToSignedPyInt(value)
			elif width == 16:
				value = "%d" % wordToSignedPyInt(value)
			elif width == 32:
				value = "%d" % dwordToSignedPyInt(value)
			else:
				assert(0)
		else:
			assert(0)
		self.__changeBlocked += 1
		self.lcd.setDigitCount(len(value))
		self.lcd.display(value)
		self.__changeBlocked -= 1

class _State_TimerCounter(StateWindow):
	def __init__(self, client, memAreaType, parent=None):
		StateWindow.__init__(self, client, parent)
		self.memAreaType = memAreaType

		self.indexSpin = QSpinBox(self)
		self.indexSpin.setMinimum(0)
		self.indexSpin.setMaximum(0xFFFF)
		self.layout().addWidget(self.indexSpin, 0, 0)

		self.formatCombo = QComboBox(self)
		self.layout().addWidget(self.formatCombo, 0, 1)

		hbox = QHBoxLayout()
		self.valueEdit = ValueLineEdit(self.__validateInput, self)
		hbox.addWidget(self.valueEdit)
		self.statusLabel = QLabel(self)
		hbox.addWidget(self.statusLabel)
		self.resetButton = QPushButton("R", self)
		hbox.addWidget(self.resetButton)
		self.layout().addLayout(hbox, 1, 0, 1, 2)

		self.displayedStatus = 0

		self.indexSpin.valueChanged.connect(self.rebuild)
		self.formatCombo.currentIndexChanged.connect(self.rebuild)
		self.valueEdit.valueChanged.connect(self.__newValueEntered)
		self.resetButton.released.connect(self.reset)

		self.__changeBlocked = 0
		self.setMinimumWidth(310)
		self.rebuild()

	def reset(self):
		self.__sendValue(0)

	def __updateStatus(self):
		self.statusLabel.setText("Q=%d" % self.displayedStatus)

	def rebuild(self):
		self.valueEdit.clear()
		self.displayedStatus = 0
		self.__updateStatus()
		self.update()
		self.configChanged.emit(self)

	def __makeMemoryArea(self):
		index = self.indexSpin.value()
		return MemoryArea(memType = self.memAreaType,
				  flags = 0,
				  index = index,
				  start = 0,
				  length = 32)

	def getMemoryAreas(self):
		return ( self.__makeMemoryArea(), )

	def setMemory(self, memArea):
		if memArea.memType != self.memAreaType or\
		   memArea.index != self.indexSpin.value():
			return False

		if memArea.flags & (memArea.FLG_ERR_READ | memArea.FLG_ERR_WRITE):
			self.valueEdit.setEnabled(False)
			return False
		self.valueEdit.setEnabled(True)

		try:
			value = WordPacker.fromBytes(memArea.data, 32)
			status = (value >> 31) & 1
			value &= 0xFFFF
		except AwlSimError as e:
			return False
		text = self.valueToText(value)
		if text == self.valueEdit.text() and\
		   status == self.displayedStatus:
			return True

		self.displayedStatus = status
		self.__updateStatus()

		self.__changeBlocked += 1
		self.valueEdit.setText(text)
		self.__changeBlocked -= 1

		self.update()
		return True

	def textToValue(self, text):
		raise NotImplementedError

	def valueToText(self, value):
		raise NotImplementedError

	def __validateInput(self, inputString, pos):
		if self.textToValue(inputString) is None:
			return QValidator.Intermediate
		return QValidator.Acceptable

	def __newValueEntered(self, newText):
		if self.__changeBlocked:
			return

		value = self.textToValue(newText)
		if value is not None:
			self.__sendValue(value)

	def __sendValue(self, value):
		memArea = self.__makeMemoryArea()
		memArea.data = bytearray(4)
		WordPacker.toBytes(memArea.data, 32, 0, value)
		self.client.writeMemory((memArea,))

class State_Timer(_State_TimerCounter):
	def __init__(self, client, parent=None):
		_State_TimerCounter.__init__(self, client,
					     MemoryArea.TYPE_T,
					     parent)
		self.setWindowTitle("Timer")

		self.indexSpin.setPrefix("T ")

		self.formatCombo.addItem("Dual", "bin")
		self.formatCombo.addItem("Hexadecimal", "hex")
		self.formatCombo.addItem("S5Time", "s5t")

		self.update()

	def textToValue(self, text):
		fmt = self.formatCombo.itemData(self.formatCombo.currentIndex())
		if fmt == "s5t":
			try:
				val = AwlDataType.tryParseImmediate_S5T(text)
				if val is None:
					return None
			except AwlSimError as e:
				return None
		elif fmt == "bin":
			try:
				val = AwlDataType.tryParseImmediate_Bin(text)
				if val is None:
					return None
				if val > 0xFFFF:
					return None
			except AwlSimError as e:
				return None
		elif fmt == "hex":
			try:
				val = AwlDataType.tryParseImmediate_HexWord(text)
				if val is None:
					return None
			except AwlSimError as e:
				return None
		else:
			assert(0)
		if (val & 0xF000) > 0x3000 or\
		   (val & 0x0F00) > 0x0900 or\
		   (val & 0x00F0) > 0x0090 or\
		   (val & 0x000F) > 0x0009:
			return None
		return val

	def valueToText(self, value):
		value &= 0xFFFF
		fmt = self.formatCombo.itemData(self.formatCombo.currentIndex())
		if fmt == "s5t":
			try:
				seconds = Timer.s5t_to_seconds(value)
				return "S5T#" + AwlDataType.formatTime(seconds, True)
			except AwlSimError as e:
				return ""
		elif fmt == "bin":
			text = "2#" + intToDualString(value, 16)
		elif fmt == "hex":
			text = "W#16#%04X" % value
		else:
			assert(0)
		return text

class State_Counter(_State_TimerCounter):
	def __init__(self, client, parent=None):
		_State_TimerCounter.__init__(self, client,
					     MemoryArea.TYPE_Z,
					     parent)
		self.setWindowTitle("Counter")

		self.indexSpin.setPrefix("C ")

		self.formatCombo.addItem("BCD (counter)", "bcd")
		self.formatCombo.addItem("Dual", "bin")

		self.update()

	def textToValue(self, text):
		fmt = self.formatCombo.itemData(self.formatCombo.currentIndex())
		if fmt == "bin":
			try:
				val = AwlDataType.tryParseImmediate_Bin(text)
				if val is None:
					return None
				if val > 0xFFFF:
					return None
			except AwlSimError as e:
				return None
		elif fmt == "bcd":
			try:
				val = AwlDataType.tryParseImmediate_BCD_word(text)
				if val is None:
					return None
			except AwlSimError as e:
				return None
		else:
			assert(0)
		if val > 0x999 or\
		   (val & 0x0F00) > 0x0900 or\
		   (val & 0x00F0) > 0x0090 or\
		   (val & 0x000F) > 0x0009:
			return None
		return val

	def valueToText(self, value):
		value &= 0xFFFF
		fmt = self.formatCombo.itemData(self.formatCombo.currentIndex())
		if fmt == "bin":
			text = "2#" + intToDualString(value, 16)
		elif fmt == "bcd":
			text = "C#%X" % value
		else:
			assert(0)
		return text

class StateWorkspace(QWorkspace):
	def __init__(self, parent=None):
		QWorkspace.__init__(self, parent)
