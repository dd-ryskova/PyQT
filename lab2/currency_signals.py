from PyQt5.QtCore import QObject, pyqtSignal

class RUBSignals(QObject):
    rubConversionStarted = pyqtSignal()
    rubConversionCompleted = pyqtSignal(dict)
    rubValueChanged = pyqtSignal(str)

class USDSignals(QObject):
    usdConversionStarted = pyqtSignal()
    usdConversionCompleted = pyqtSignal(dict)
    usdValueChanged = pyqtSignal(str)

class EURSignals(QObject):
    eurConversionStarted = pyqtSignal()
    eurConversionCompleted = pyqtSignal(dict)
    eurValueChanged = pyqtSignal(str)