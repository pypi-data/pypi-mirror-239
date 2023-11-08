from PySide6 import QtWidgets, QtCore
from py_ballisticcalc import Unit

from py_balcalc.signals_manager import appSignalMgr
from py_balcalc.translator import tr
from py_balcalc.ui.custom_widgets import TLabel, UnitSpinBox


class ProfileConditions(QtWidgets.QGroupBox):
    """shows selected profile atmo conditions"""

    def __init__(self, parent=None):
        super(ProfileConditions, self).__init__(parent)
        self.init_ui(self)

    def init_ui(self, conditions):
        conditions.setObjectName("ProfileConditions")
        conditions.setCheckable(True)

        self.gridLayout = QtWidgets.QGridLayout(conditions)
        self.gridLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.c_zero_air_pressure = UnitSpinBox(conditions, Unit.HP(1000), 'unit/pressure')
        self.z_angle = UnitSpinBox(conditions, Unit.DEGREE(0), 'unit/angular')
        self.c_zero_temperature = UnitSpinBox(conditions, Unit.CELSIUS(0), 'unit/temperature')
        self.z_powder_temp = UnitSpinBox(conditions, Unit.CELSIUS(0), 'unit/temperature')
        self.c_zero_air_humidity = QtWidgets.QSpinBox(conditions)

        self.gridLayout.addWidget(self.c_zero_temperature, 0, 1)
        self.gridLayout.addWidget(self.z_powder_temp, 1, 1)
        self.gridLayout.addWidget(self.c_zero_air_humidity, 2, 1)
        self.gridLayout.addWidget(self.c_zero_air_pressure, 3, 1)
        self.gridLayout.addWidget(self.z_angle, 4, 1)

        self.c_zero_air_pressure.setObjectName("c_zero_air_pressure")

        self.z_angle.setObjectName("z_angle")

        self.c_zero_temperature.setObjectName("c_zero_temperature")

        self.c_zero_air_humidity.setObjectName("c_zero_air_humidity")

        self.z_powder_temp.setObjectName("z_powder_temp")

        self.gridLayout.addWidget(TLabel('Temperature:'), 0, 0, 1, 1)
        self.gridLayout.addWidget(TLabel('Powder Temperature:'), 1, 0, 1, 1)
        self.gridLayout.addWidget(TLabel('Humidity:'), 2, 0, 1, 1)
        self.gridLayout.addWidget(TLabel('Pressure:'), 3, 0, 1, 1)
        self.gridLayout.addWidget(TLabel('Angle:'), 4, 0, 1, 1)

        appSignalMgr.translator_updated.connect(self.tr_ui)
        self.tr_ui()

    def tr_ui(self):
        self.setTitle(tr("conditions", "Zeroing conditions"))
        self.c_zero_air_humidity.setSuffix(tr("conditions", " %"))
