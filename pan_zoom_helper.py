# Pan Zoom Helper
#
# This script allows user to easily use maya's pan/zoom options.
# You need to set the camera you want to work on
# You can set production camera into the preferences class
# so the script will automatically set it.
#
# INSTALLATION INSTRUCTIONS :
# Copy this script into your maya/scripts folder
# Run these lines in with python:
# "import pan_zoom_helper;"
# "window = pan_zoom_helper.PAN_ZOOM_TOOL();"
# "window.show();"

import os
from PySide2.QtWidgets import QMainWindow, QWidget, QHBoxLayout,QVBoxLayout, QPushButton, QFrame, QDoubleSpinBox, QLineEdit, QLabel, QCheckBox
import maya.cmds as cmds


# FOR MAC OS WE NEED THIS LINE FOR PYTHON 2.7
os.environ['QT_MAC_WANTS_LAYER'] = '1'


class PREFERENCES(object):

    preferences = dict(
        # Set production camera here below
        shotcam='cameraShape1',
        # Change default move step value below
        move_step_value=0.1,
        # Change default zoom step value below
        zoom_step_value=0.1,
    )


class SEPARATOR_LINE(QFrame):
    def __init__(self, parent=None):
        super(SEPARATOR_LINE, self).__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class PAN_ZOOM_TOOL(QMainWindow):

    def __init__(self):

        super(PAN_ZOOM_TOOL, self).__init__()
        self.setWindowTitle('PAN ZOOM TOOL')

        # Load layout
        self.load_ui()

        # Set all buttons disabled by default
        self.enable_zoom_option_buttons(False)
        self.enable_zoom_buttons(False)
        self.enable_move_buttons(False)

        # Check if preference shotcam exists in scene
        self.get_production_camera()

        # Set default step values according to preferences
        self.set_default_move_zoom_step()

    def load_ui(self):

        # Create main layout
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)

        # Create a two row layout for camera name and button
        self.camera_setup_layout = QHBoxLayout(central_widget)

        self.set_camera_button = QPushButton('Set Cam')
        self.set_camera_button.clicked.connect(self.set_camera)

        self.camera_name_text_field = QLineEdit()
        self.camera_name_text_field.setText('set_camera')
        self.camera_name_text_field.setDisabled(True)

        self.camera_setup_layout.addWidget(self.set_camera_button, 1)
        self.camera_setup_layout.addWidget(self.camera_name_text_field)

        # Add to layout
        main_layout.addLayout(self.camera_setup_layout)

        # Add separator
        camera_name_separator = SEPARATOR_LINE(self)
        main_layout.addWidget(camera_name_separator)

        # Create PanZoom Enable/Disable and reset options
        self.layout_pan_zoom_options = QHBoxLayout()

        self.enable_pan_zoom_checkbox = QCheckBox('Pan Zoom')
        self.enable_pan_zoom_checkbox.stateChanged.connect(self.on_pan_zoom_enable)
        self.reset_all_button = QPushButton('Reset')
        self.reset_all_button.clicked.connect(self.reset_all)

        self.layout_pan_zoom_options.addWidget(self.enable_pan_zoom_checkbox)
        self.layout_pan_zoom_options.addWidget(self.reset_all_button)

        # Add to layout
        main_layout.addLayout(self.layout_pan_zoom_options)

        # Add separator
        pan_zoom_options_separator = SEPARATOR_LINE(self)
        main_layout.addWidget(pan_zoom_options_separator)

        # Create the Zoom buttons
        self.layout_zoom_in_out_buttons = QHBoxLayout()

        self.zoom_in_button = QPushButton('Zoom In')
        self.zoom_in_button.clicked.connect(self.zoom_in)

        self.zoom_out_button = QPushButton('Zoom Out')
        self.zoom_out_button.clicked.connect(self.zoom_out)

        self.layout_zoom_in_out_buttons.addWidget(self.zoom_in_button)
        self.layout_zoom_in_out_buttons.addWidget(self.zoom_out_button)

        main_layout.addLayout(self.layout_zoom_in_out_buttons)

        # Create the Reset Zoom button
        self.reset_zoom_button = QPushButton('Reset Zoom')
        self.reset_zoom_button.clicked.connect(self.reset_zoom)

        # Add to layout
        main_layout.addWidget(self.reset_zoom_button)

        # Add separator
        zoom_buttons_separator = SEPARATOR_LINE(self)
        main_layout.addWidget(zoom_buttons_separator)

        # Create the move buttons
        self.layout_left_right_buttons = QHBoxLayout()
        self.move_up_button = QPushButton('Up')
        self.move_up_button.clicked.connect(self.move_up)
        self.move_left_button = QPushButton('Left')
        self.move_left_button.clicked.connect(self.move_left)
        self.move_right_button = QPushButton('Right')
        self.move_right_button.clicked.connect(self.move_right)
        self.move_down_button = QPushButton('Down')
        self.move_down_button.clicked.connect(self.move_down)
        self.reset_move_button = QPushButton('Reset Move')
        self.reset_move_button.clicked.connect(self.reset_move)

        self.layout_left_right_buttons.addWidget(self.move_left_button)
        self.layout_left_right_buttons.addWidget(self.move_right_button)

        # Add to layout
        main_layout.addWidget(self.move_up_button)
        main_layout.addLayout(self.layout_left_right_buttons)
        main_layout.addWidget(self.move_down_button)
        main_layout.addWidget(self.reset_move_button)

        # Add separator
        move_buttons_separator = SEPARATOR_LINE(self)
        main_layout.addWidget(move_buttons_separator)

        # Create user zoom step options
        self.layout_user_zoom_step = QHBoxLayout()

        zoom_step_label = QLabel('Zoom Step Value')
        self.zoom_step_spinbox = QDoubleSpinBox()
        self.zoom_step_spinbox.setMaximum(100)
        self.zoom_step_spinbox.setMinimum(0)

        self.layout_user_zoom_step.addWidget(zoom_step_label, 1)
        self.layout_user_zoom_step.addWidget(self.zoom_step_spinbox)

        # Add to layout
        main_layout.addLayout(self.layout_user_zoom_step)

        # Create user move step options
        self.layout_user_move_step = QHBoxLayout()

        move_step_label = QLabel('Move Step Value')
        self.move_step_spinbox = QDoubleSpinBox()
        self.move_step_spinbox.setMaximum(100)
        self.move_step_spinbox.setMinimum(0)

        self.layout_user_move_step.addWidget(move_step_label, 1)
        self.layout_user_move_step.addWidget(self.move_step_spinbox)

        # Add to layout
        main_layout.addLayout(self.layout_user_move_step)

        # Add separator
        hint_text_separator = SEPARATOR_LINE(self)
        main_layout.addWidget(hint_text_separator)

        # Add user hint text
        user_hint_text = QLabel('<span style= font-size:8pt; text-align:center> <p>Use SHIFT + Click on  move/zoom button</p><p> to divide step value by 2</p>')
        main_layout.addWidget(user_hint_text)

        self.setCentralWidget(central_widget)

    def on_pan_zoom_enable(self, state):

        if state == 2:
            # Checked state (ON)
            shotcam = self.camera_name_text_field.text()
            cmds.setAttr(shotcam+'.panZoomEnabled', 1)
            self.enable_zoom_buttons(True)
            self.enable_move_buttons(True)

        else:
            # Unchecked state (OFF)
            shotcam = self.camera_name_text_field.text()
            cmds.setAttr(shotcam+'.panZoomEnabled', 0)
            self.enable_zoom_buttons(False)
            self.enable_move_buttons(False)

    def enable_zoom_option_buttons(self, bool):

        self.enable_pan_zoom_checkbox.setEnabled(bool)
        self.reset_all_button.setEnabled(bool)
        self.zoom_step_spinbox.setEnabled(bool)
        self.move_step_spinbox.setEnabled(bool)

    def enable_zoom_buttons(self, bool):

        self.zoom_in_button.setEnabled(bool)
        self.zoom_out_button.setEnabled(bool)
        self.reset_zoom_button.setEnabled(bool)

    def enable_move_buttons(self, bool):

        self.move_up_button.setEnabled(bool)
        self.move_down_button.setEnabled(bool)
        self.move_left_button.setEnabled(bool)
        self.move_right_button.setEnabled(bool)
        self.reset_move_button.setEnabled(bool)

    def set_camera(self):

        selected_cam = cmds.ls(selection=True)

        if len(selected_cam) == 0:
            return cmds.warning("Please select a camera.")

        if len(selected_cam) >=2 :
            return cmds.warning("Please select only one camera.")

        if cmds.objectType(selected_cam[0]) == 'transform':
            selected_cam_shape = cmds.listRelatives(selected_cam, s=True)
            if cmds.objectType(selected_cam_shape[0]) == 'camera':
                shotcam = selected_cam_shape[0]
                self.camera_name_text_field.setText(str(shotcam))

                # Turn UI Buttons ON
                self.enable_zoom_option_buttons(True)
                pan_zoom_enabled = self.get_current_pan_zoom_status()
                self.enable_pan_zoom_checkbox.setChecked(pan_zoom_enabled)

                return shotcam
            return cmds.warning("The selected object is not a camera")

        camera = cmds.objectType(selected_cam)
        if camera in ['camera', 'stereoRigCamera']:
            shotcam = selected_cam[0]
            self.camera_name_text_field.setText(shotcam)

            return shotcam
        return cmds.warning("The selected object is not a camera")

    def get_production_camera(self):

        preferences_class = PREFERENCES()
        shotcam = preferences_class.preferences.get('shotcam')

        # If Camera exists in scene, set it as text_field
        if cmds.objExists(shotcam):

            # Set textfield text
            self.camera_name_text_field.setText(shotcam)
            # Enable buttons
            self.enable_zoom_option_buttons(True)

            # Get current shotcam status
            pan_zoom_enabled = self.get_current_pan_zoom_status()
            self.enable_pan_zoom_checkbox.setChecked(pan_zoom_enabled)

        else:
            shotcam = 'Camera Is Not Set!'
            self.camera_name_text_field.setText(shotcam)
            print("No production or prefered camera found in scene.")
            self.enable_zoom_option_buttons(False)

    def get_current_pan_zoom_status(self):
        shotcam = self.camera_name_text_field.text()

        if cmds.objExists(shotcam):
            pan_zoom_enabled = cmds.getAttr(shotcam + '.panZoomEnabled')
            return pan_zoom_enabled

    def set_default_move_zoom_step(self):

        prefs = PREFERENCES()
        default_move_step_value = prefs.preferences.get('move_step_value')
        default_zoom_step_value = prefs.preferences.get('zoom_step_value')

        if default_move_step_value:
            self.move_step_spinbox.setValue(default_move_step_value)

        if default_zoom_step_value:
            self.zoom_step_spinbox.setValue(default_zoom_step_value)

    def zoom_in(self):
        zoom_step_value = self.zoom_step_spinbox.value()
        shotcam = self.camera_name_text_field.text()
        current_value = cmds.getAttr(shotcam + '.zoom')

        # If mod key pressed
        mod = cmds.getModifiers()
        if mod == 1:
            new_value = current_value - (zoom_step_value/2)
            if new_value <= 0:
                return  cmds.warning("The value you try to set is below zero")
            cmds.setAttr(shotcam+'.zoom', new_value)
            return

        new_value = current_value - zoom_step_value
        if new_value <= 0:
            return cmds.warning("The value you try to set is below zero")
        cmds.setAttr(shotcam + '.zoom', new_value)
        return

    def zoom_out(self, *args):
        zoom_step_value = self.zoom_step_spinbox.value()
        shotcam = self.camera_name_text_field.text()
        current_value = cmds.getAttr(shotcam + '.zoom')

        # If mod key pressed
        mod = cmds.getModifiers()
        if mod == 1:
            new_value = current_value + (zoom_step_value / 2)
            if new_value <= 0:
                return cmds.warning("The value you try to set is below zero")
            cmds.setAttr(shotcam + '.zoom', new_value)
            return

        new_value = current_value + zoom_step_value
        if new_value <= 0:
            return cmds.warning("The value you try to set is below zero")
        cmds.setAttr(shotcam + '.zoom', new_value)
        return

    def reset_zoom(self):
        shotcam = self.camera_name_text_field.text()
        cmds.setAttr(shotcam + '.zoom', 1)

    def move_up(self):
        mod = cmds.getModifiers()
        move_step_value = self.move_step_spinbox.value()
        shotcam = self.camera_name_text_field.text()

        current_value = cmds.getAttr(shotcam + '.verticalPan')
        if mod == 1:
            new_value = current_value + (move_step_value / 2)
            cmds.setAttr(shotcam + '.verticalPan', new_value)
            return
        new_value = current_value + move_step_value
        cmds.setAttr(shotcam + '.verticalPan', new_value)
        return

    def move_down(self):
        mod = cmds.getModifiers()
        move_step_value = self.move_step_spinbox.value()
        shotcam = self.camera_name_text_field.text()

        current_value = cmds.getAttr(shotcam + '.verticalPan')
        if mod == 1:
            new_value = current_value - (move_step_value / 2)
            cmds.setAttr(shotcam + '.verticalPan', new_value)
            return
        new_value = current_value - move_step_value
        cmds.setAttr(shotcam + '.verticalPan', new_value)
        return

    def move_left(self):
        mod = cmds.getModifiers()
        move_step_value = self.move_step_spinbox.value()
        shotcam = self.camera_name_text_field.text()

        current_value = cmds.getAttr(shotcam + '.horizontalPan')
        if mod == 1:
            new_value = current_value - (move_step_value / 2)
            cmds.setAttr(shotcam + '.horizontalPan', new_value)
            return
        new_value = current_value - move_step_value
        cmds.setAttr(shotcam + '.horizontalPan', new_value)
        return

    def move_right(self):
        mod = cmds.getModifiers()
        move_step_value = self.move_step_spinbox.value()
        shotcam = self.camera_name_text_field.text()

        current_value = cmds.getAttr(shotcam + '.horizontalPan')
        if mod == 1:
            new_value = current_value + (move_step_value / 2)
            cmds.setAttr(shotcam + '.horizontalPan', new_value)
            return
        new_value = current_value + move_step_value
        cmds.setAttr(shotcam + '.horizontalPan', new_value)
        return

    def reset_move(self):
        shotcam = self.camera_name_text_field.text()
        cmds.setAttr(shotcam + '.verticalPan', 0)
        cmds.setAttr(shotcam + '.horizontalPan', 0)

    def reset_all(self):
        self.reset_zoom()
        self.reset_move()


def show():
    window = PAN_ZOOM_TOOL()
    window.show()
