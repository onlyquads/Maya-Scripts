# This script creates a window with shortcut buttons for quick access while
# painting skincluster influences in maya
import sys
from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QWidget
from functools import partial
import maya.cmds as cmds
import maya.mel as mel

TOOL_NAME = 'Skin Paint Helper'

# You can edit the default step value here
DEFAULT_STEP_VALUE = 1

# You can edit, remove, add values of buttons here.
SKIN_PAINT_VALUES = [
    0, 0.25, 0.50, 0.75, 1, 0.1, 0.2, 0.8, 0.9
]


def maya_main_window():
    """Return Maya's main window"""
    for obj in QtWidgets.QApplication.topLevelWidgets():
        if obj.objectName() == 'MayaWindow':
            return obj
    raise RuntimeError('Could not find MayaWindow instance')


class SkinPaintHelper(QWidget):
    def __init__(self, parent=None):
        if not parent:
                parent = maya_main_window()
        super(SkinPaintHelper, self).__init__(parent, QtCore.Qt.Tool)

        self.setWindowTitle(TOOL_NAME)

        self.initUI()

    def initUI(self):
        # self.setFixedSize(180, 250)

        layout = QtWidgets.QVBoxLayout()

        # PAINT TOOL TITLE
        layout.addWidget(QtWidgets.QLabel('Skin Paint Helper'))

        # PAINT VALUE BUTTONS
        button_layout1 = QtWidgets.QGridLayout()
        replace_btn = QtWidgets.QPushButton('Replace')
        replace_btn.setToolTip('Set Operation to Replace')
        replace_btn.clicked.connect(self.set_operation_replace)
        button_layout1.addWidget(replace_btn, 0, 0)

        smooth_btn = QtWidgets.QPushButton('Smooth')
        smooth_btn.setToolTip('Set Operation to Smooth')
        smooth_btn.clicked.connect(self.set_operation_smooth)
        button_layout1.addWidget(smooth_btn, 0, 1)

        layout.addLayout(button_layout1)

        button_layout2 = QtWidgets.QGridLayout()
        row, col = 0, 0
        for i in SKIN_PAINT_VALUES:
            btn = QtWidgets.QPushButton(str(i))
            btn.setToolTip(f'Set Paint Value to {i}. Use SHIFT+CLICK to set as Step value')
            btn.clicked.connect(partial(self.set_paint_value, i))
            button_layout2.addWidget(btn, row, col)
            col += 1
            if col > 4:
                col = 0
                row += 1

        layout.addLayout(button_layout2)

        button_layout3 = QtWidgets.QHBoxLayout()
        increase_btn = QtWidgets.QPushButton('+')
        increase_btn.setToolTip('Increase paint Value')
        increase_btn.clicked.connect(self.increase_paint_value)
        button_layout3.addWidget(increase_btn)

        self.step_value_field = QtWidgets.QDoubleSpinBox()
        self.step_value_field.setValue(DEFAULT_STEP_VALUE)
        self.step_value_field.setToolTip('Set Step Value')
        button_layout3.addWidget(self.step_value_field)

        decrease_btn = QtWidgets.QPushButton('-')
        decrease_btn.setToolTip('Decrease paint Value')
        decrease_btn.clicked.connect(self.decrease_paint_value)
        button_layout3.addWidget(decrease_btn)

        layout.addLayout(button_layout3)

        flood_btn = QtWidgets.QPushButton('Flood')
        flood_btn.setToolTip('Flood paint Value')
        flood_btn.clicked.connect(self.flood_user_value)
        layout.addWidget(flood_btn)

        self.setLayout(layout)

    def get_current_paint_value(self):
        current_context = cmds.currentCtx()

        if 'artAttrSkinContext' in current_context:
            current_paint_value = cmds.artAttrCtx(
                current_context, q=True, value=True)
            return current_paint_value
        else:
            current_paint_value = 'N/A'
            return current_paint_value

    def set_paint_value(self, value, *args):
        current_context = cmds.currentCtx()
        if 'artAttr' not in current_context:
            return cmds.warning('Not in Skin Paint Context')

        mods = cmds.getModifiers()
        if mods == 1:
            self.step_value_field.setValue(value)
            return

        cmds.artAttrCtx(current_context, e=True, value=value)
        print('Paint Value set to ' + str(value))

    def increase_paint_value(self):
        current_context = cmds.currentCtx()
        if 'artAttr' not in current_context:
            return cmds.warning('Not in Skin Paint Context')
        step_value = self.step_value_field.value()
        current_paint_value = cmds.artAttrCtx(
            current_context, query=True, value=True)
        print('Current paint value = ' + str(current_paint_value))
        new_paint_value = current_paint_value + step_value
        cmds.artAttrCtx(current_context, e=True, value=new_ppaint_value)
        print('Paint Value set to ' + str(new_paint_value))

    def decrease_paint_value(self):
        current_context = cmds.currentCtx()
        if 'artAttr' not in current_context:
            return cmds.warning('Not in Skin Paint Context')
        step_value = self.step_value_field.value()
        current_paint_value = cmds.artAttrCtx(
            current_context, query=True, value=True)
        print('Current paint value = ' + str(current_paint_value))
        new_paint_value = current_paint_value - step_value
        cmds.artAttrCtx(current_context, e=True, value=new_paint_value)
        print('Paint Value set to ' + str(new_paint_value))

    def flood_user_value(self):
        current_context = cmds.currentCtx()
        if 'artAttr' not in current_context:
            return cmds.warning('Not in Skin Paint Context')
        mods = cmds.getModifiers()
        if mods == 1:
            current_value = cmds.artAttrCtx(current_context, q=True, value=True)
            step_value = 0
            cmds.artAttrCtx(current_context, e=True, value=step_value)
            cmds.artAttrCtx(current_context, e=True, clear=True)
            cmds.artAttrCtx(current_context, e=True, value=current_value)
            print('Paint Flood with value : ' + str(step_value))
            return
        current_value = cmds.artAttrCtx(current_context, q=True, value=True)
        step_value = 1
        cmds.artAttrCtx(current_context, e=True, value=step_value)
        cmds.artAttrCtx(current_context, e=True, clear=True)
        cmds.artAttrCtx(current_context, e=True, value=current_value)
        print('Paint Flood with value : ' + str(step_value))

    def set_operation_replace(self):
        current_context = cmds.currentCtx()
        if 'artAttr' not in current_context:
            return cmds.warning('Not in Skin Paint Context')
        if 'skin' in current_context:
            mel.eval('artAttrPaintOperation artAttrSkinPaintCtx Replace;')
            return
        if 'art' in current_context:
            mel.eval('artAttrPaintOperation artAttrCtx Replace')
            return
        print('Operation set to Replace')

    def set_operation_smooth(self):
        current_context = cmds.currentCtx()
        if 'artAttr' not in current_context:
            return cmds.warning('Not in Skin Paint Context')
        if 'skin' in current_context:
            mel.eval('artAttrPaintOperation artAttrSkinPaintCtx Smooth;')
            return
        if 'art' in current_context:
            mel.eval('artAttrPaintOperation artAttrCtx Smooth')
            return
        print('Operation set to Smooth')

def show_ui():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    window = SkinPaintHelper()
    window.show()

    app.exec_()


