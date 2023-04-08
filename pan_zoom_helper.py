###PanZoomHelper
###This script allows user to easily use maya's pan/zoom options.
###You need to set the camera you want to work on
###You can set production camera into the preferences so the script will automattically set it.

import maya.cmds as cmds
from functools import partial


preferences = dict (

	###Set production camera here
	shotcam = 'cameraShape1',

	move_step_value = 0.1,

	zoom_step_value = 0.1,
	)

def get_production_camera (*args):

	shotcam = preferences.get('shotcam')
	if cmds.objExists(shotcam):
		cmds.textField(selected_shotcam_field, e=True, text = shotcam)
		cmds.rowColumnLayout(pan_zoom_main_toolsUI, e=True, enable = True)
	else:
		shotcam = 'Camera Is Not Set!'
		cmds.textField(selected_shotcam_field, e=True, text = shotcam)
		cmds.warning("No produciton camera found in scene.")


def set_shotcam (*args):
	
	selected_cam = cmds.ls(selection = True)
	
	if len(selected_cam) == 0:
		return cmds.warning ("Please select a camera.")
		
	if len(selected_cam) >=2 :
		return cmds.warning("Please select only one camera.")

	if cmds.objectType(selected_cam[0]) == 'transform':
		selected_cam_shape = cmds.listRelatives(selected_cam, s=True)
		if cmds.objectType(selected_cam_shape[0]) == 'camera':
			shotcam = selected_cam_shape[0]
			cmds.textField(selected_shotcam_field, e=True, text= str(selected_cam_shape[0]))
			cmds.rowColumnLayout(pan_zoom_main_toolsUI, e=True, enable = True)
			return shotcam
		return cmds.warning("The selected object is not a camera")
	if cmds.objectType(selected_cam) == 'camera' or cmds.objectType(selected_cam) == 'stereoRigCamera':
		shotcam = selected_cam[0]
		cmds.textField(selected_shotcam_field, e=True, text= str(selected_cam[0]))
		cmds.rowColumnLayout(pan_zoom_main_toolsUI, e=True, enable = True)
		return shotcam
	
	return cmds.warning("The selected object is not a camera")


def mod_key_pressed (label, *args):
	move_step_value = cmds.floatField (user_move_step_value, q=True, value = True)
	zoom_step_value = cmds.floatField (user_zoom_step_value, q=True, value = True)


def set_pan_zoom_enable(*args):

	shotcam = cmds.textField(selected_shotcam_field, q=True, text= True)
	cmds.setAttr(shotcam+'.panZoomEnabled', 1)
	cmds.rowColumnLayout(pan_zoom_toolsUI,e=True, enable = True)

def set_pan_zoom_disable(*args):

	shotcam = cmds.textField(selected_shotcam_field, q=True, text= True)
	cmds.setAttr(shotcam+'.panZoomEnabled', 0)
	cmds.rowColumnLayout(pan_zoom_toolsUI,e=True, enable = False)


### RESET FUNCTIONS
def reset_zoom(*args):
	
	pan_zoom_tool_state = cmds.checkBox(pan_zoom_tool_state_checkbox, q=True, value = True)
	if pan_zoom_tool_state == False:
		return

	shotcam = cmds.textField(selected_shotcam_field, q=True, text= True)
	cmds.setAttr(shotcam+'.zoom', 1)

def reset_move(*args):
	
	pan_zoom_tool_state = cmds.checkBox(pan_zoom_tool_state_checkbox, q=True, value = True)
	if pan_zoom_tool_state == False:
		return
	shotcam = cmds.textField(selected_shotcam_field, q=True, text= True)
	cmds.setAttr(shotcam+'.horizontalPan', 0)
	cmds.setAttr(shotcam+'.verticalPan', 0)
	return

def reset_pan_zoom_to_default(*args):

	reset_zoom()
	reset_move()


### ZOOM FUNCTION
def zoom (direction, *args):
	pan_zoom_tool_state = cmds.checkBox(pan_zoom_tool_state_checkbox, q=True, value = True)
	if pan_zoom_tool_state == False:
		return
	
	zoom_step_value = cmds.floatField(user_zoom_step_value, q=True, value = True)
	shotcam = cmds.textField(selected_shotcam_field, q=True, text= True)
	current_value = cmds.getAttr(shotcam+'.zoom')

	if direction == 'Zoom In':
		mod = cmds.getModifiers()
		if mod == 1:
			new_value = current_value - (zoom_step_value/2)
			if new_value <= 0:
				return  cmds.warning("The value you try to set is below zero")
			cmds.setAttr(shotcam+'.zoom', new_value)
			return
		new_value = current_value - zoom_step_value
		if new_value <= 0:
			return  cmds.warning("The value you try to set is below zero")
		cmds.setAttr(shotcam+'.zoom', new_value)
		return
	if direction == 'Zoom Out' :
		mod = cmds.getModifiers()
		if mod == 1:
			new_value = current_value + (zoom_step_value/2)
			cmds.setAttr(shotcam+'.zoom', new_value)
			return
		new_value = current_value + zoom_step_value
		cmds.setAttr(shotcam+'.zoom', new_value)
		return


### MOVE FUNCTION
def move (direction, *args):
	
	pan_zoom_tool_state = cmds.checkBox(pan_zoom_tool_state_checkbox, q=True, value= True)
	if pan_zoom_tool_state == False:
		return

	if direction == 'Reset':
		reset_move()
		return

	mod = cmds.getModifiers()
	move_step_value = cmds.floatField(user_move_step_value, q=True, value= True)
	shotcam = cmds.textField(selected_shotcam_field, q=True, text= True)
	if direction == 'Up':
		current_value = cmds.getAttr(shotcam+'.verticalPan')
		if mod == 1:
			new_value = current_value + (move_step_value/2)
			cmds.setAttr(shotcam+'.verticalPan', new_value)
			return
		new_value = current_value + move_step_value
		cmds.setAttr(shotcam+'.verticalPan', new_value)
		return

	if direction == 'Down':
		current_value = cmds.getAttr(shotcam+'.verticalPan')
		if mod == 1:
			new_value = current_value - (move_step_value/2)
			cmds.setAttr(shotcam+'.verticalPan', new_value)
			return
			
		new_value = current_value - move_step_value
		cmds.setAttr(shotcam+'.verticalPan', new_value)
		return

	if direction == 'Right':
		current_value = cmds.getAttr(shotcam+'.horizontalPan')
		if mod == 1 :
			new_value = current_value + (move_step_value/2)
			cmds.setAttr(shotcam+'.horizontalPan', new_value)
			return
		new_value = current_value + move_step_value
		cmds.setAttr(shotcam+'.horizontalPan', new_value)
		return

	if direction == 'Left':
		current_value = cmds.getAttr(shotcam+'.horizontalPan')
		if mod == 1 :
			new_value = current_value - (move_step_value/2)
			cmds.setAttr(shotcam+'.horizontalPan', new_value)
			return
		new_value = current_value - move_step_value
		cmds.setAttr(shotcam+'.horizontalPan', new_value)
		return



def move_buttons():
	cmds.rowColumnLayout(adjustableColumn=True,numberOfColumns = 1, columnWidth = [(1,180)])
	cmds.separator(h=10)
	cmds.button(label='Up', annotation ="Use SHIFT + CLICK to divide the step value by 2.", command = partial(move, 'Up'), height =30)
	cmds.rowColumnLayout(adjustableColumn=True,numberOfColumns=2, columnWidth=[(1,90),(2,90)])
	cmds.button(label='Left', annotation ="Use SHIFT + CLICK to divide the step value by 2.", command = partial(move, 'Left'), height =30)
	cmds.button(label='Right',annotation ="Use SHIFT + CLICK to divide the step value by 2.", command = partial(move, 'Right'), height =30)
	cmds.setParent('..')
	cmds.button(label='Down',annotation ="Use SHIFT + CLICK to divide the step value by 2.", command = partial(move, 'Down'), height =30)
	cmds.button(label='Reset Move',annotation ="Reset only move.", command = partial(move, 'Reset'))
	cmds.separator(h=10)
	cmds.setParent('..')




#CREATE WINDOW
pan_zoom_tool_window = cmds.window( title="Pan Zoom Helper")
window_width=180
cmds.columnLayout( adjustableColumn=True, w= window_width, columnAlign = 'center' )

#WINDOW TITLE
cmds.separator(h=10)
cmds.text('PAN ZOOM HELPER')
cmds.separator(h=10)
cmds.setParent('..')

cmds.rowColumnLayout( adjustableColumn=True,numberOfColumns=2, columnWidth=[(1, 40), (2, 140)])
set_selected_cam_as_shotcam = cmds.button(label='Set', annotation = "Select a camera and click on Set", command = set_shotcam)
selected_shotcam_field = cmds.textField(isObscured = True, editable = False, text = '')

cmds.setParent('..')

###RESET OR ENABLE BUTTONS
cmds.separator(h=10)
pan_zoom_main_toolsUI = cmds.rowColumnLayout(adjustableColumn=True,numberOfColumns=1, enable = False)
cmds.rowColumnLayout(adjustableColumn=True,numberOfColumns=2, columnWidth=[(1, 90), (2, 90)])

pan_zoom_tool_state_checkbox = cmds.checkBox( label='Pan Zoom', annotation ="Enable/Disable Pan Zoom.", align='center',value = False, onCommand = set_pan_zoom_enable, offCommand = set_pan_zoom_disable )
reset_pan_zoom_button = cmds.button(label='Reset',annotation = "Reset Pan and Zoom.", command = reset_pan_zoom_to_default)
cmds.setParent('..')
cmds.setParent('..')

###ZOOM BUTTONS
pan_zoom_toolsUI = cmds.rowColumnLayout(adjustableColumn=True,numberOfColumns=1, columnWidth=[(1, 180)], enable = False)
cmds.separator(h=10)
cmds.rowColumnLayout( adjustableColumn=True,numberOfColumns=3, columnWidth=[(1, 90), (2, 90)])
cmds.button(label="Zoom In", height = 30,annotation ="Use SHIFT + CLICK to divide the step value by 2.", command = partial (zoom,'Zoom In'))
cmds.button(label="Zoom Out", height = 30,annotation ="Use SHIFT + CLICK to divide the step value by 2.", command = partial (zoom,'Zoom Out'))
cmds.setParent('..')
cmds.button(label ="Reset Zoom", annotation = "Reset only zoom", command = reset_zoom)

###MOVE BUTTONS
move_buttons()


cmds.rowColumnLayout(adjustableColumn=True,numberOfColumns = 2, columnWidth=[(1, 90), (2, 90)])

default_zoom_step_value = preferences.get('zoom_step_value')
default_move_step_value = preferences.get('move_step_value')
cmds.text('Zoom Step Value')
user_zoom_step_value = cmds.floatField(value = default_zoom_step_value, annotation = "Set a step value to increment the zoom value with." )
cmds.text('Move Step Value')
user_move_step_value = cmds.floatField(value = default_move_step_value, annotation = "Set a step value to increment the move value with.")
cmds.setParent('..')



#SHOW WINDOW

get_production_camera()
cmds.showWindow( pan_zoom_tool_window )

