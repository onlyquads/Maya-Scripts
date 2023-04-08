###This script is a workaround for maya  artists working with Team Viewer. 
###As Team Viewer doesn’t send key pressed infos other than modifiers keys, 
###users cannot use some maya paint shortcuts. 
###Using this script users can increase/decrease paint brush values or soft selection radius value. 

import maya.cmds as cmds
import maya.mel as mel
from functools import partial

tv_paint_tools_version = 1.2

###EDIT VALUES HERE TO CHANGE DEFAULT STEP VALUE AND BUTTONS VALUES.
###YOU CAN ADD MORE BUTTONS TOO
PRESET_VALUES = dict(
	brush_step_default_value = 0.05,
	brush_buttons_values=[
		(0.005),
		(0.01),
		(0.04)
		],
	softsel_step_default_value = 0.1,
	softsel_buttons_values =[
		(0.01),
		(0.1),
		(1)
		]	
	)


#PAINT BRUSH FUNCTIONS

def increase_brush_radius(*args):
	current_context = cmds.currentCtx()
	if "art" not in current_context:
		return cmds.warning("Not in Paint Context")

	step_value = cmds.floatField(user_specified_step, q=True, v=True)
	current_radius = cmds.artAttrCtx(current_context, query=True, radius=True)
	new_radius = current_radius + step_value
	cmds.artAttrCtx(current_context, e=True, radius=new_radius)
	print("Brush Radius set to " + str(new_radius))


def decrease_brush_radius(*args):
	current_context = cmds.currentCtx()
	if "art" not in current_context:
		return cmds.warning("Not in Paint Context")	

	step_value = cmds.floatField(user_specified_step, q=True, v=True)
	current_radius = cmds.artAttrCtx(current_context, query=True, radius=True)
	new_radius = current_radius - step_value
	cmds.artAttrCtx(current_context, e=True, radius=new_radius)
	print("Brush Radius set to " + str(new_radius))


def set_brush_radius_from_button(label, *args):
	brush_radius = label
	current_context = cmds.currentCtx()

	if "art" not in current_context:
		return cmds.warning("Not in Paint Context")
	
	mods = cmds.getModifiers()
	if mods ==1:
		return cmds.floatField(user_specified_step, e= True,v=brush_radius)

	cmds.artAttrCtx(current_context, e=True, radius=brush_radius)
	print("Brush Radius set to " + str(brush_radius))

#SOFT SELECTION FUNCTIONS

def increase_softsel_radius(*args):
	
	current_context = cmds.currentCtx()
	if "art" in current_context:
		return cmds.warning("Not in a transform context.")
	
	step_value = cmds.floatField(user_specified_softsel_step, q=True, v=True)
	current_radius = cmds.softSelect(query=True, softSelectDistance=True)
	new_radius = current_radius + step_value
	cmds.softSelect(e=True, softSelectDistance=new_radius)
	print("Soft Selection Radius set to "+ str(new_radius))

def decrease_softsel_radius(*args):
	current_context = cmds.currentCtx()
	if "art" in current_context:
		return cmds.warning("Not in a transform context.")
	
	step_value = cmds.floatField(user_specified_softsel_step, q=True, v=True)
	current_radius = cmds.softSelect(query=True, softSelectDistance=True)
	new_radius = current_radius - step_value
	cmds.softSelect(e=True, softSelectDistance=new_radius)
	print("Soft Selection Radius set to "+ str(new_radius))

def set_softsel_radius_from_button (label, *args):
	current_context = cmds.currentCtx()
	if "art" in current_context:
		return cmds.warning("Not in a transform context.")
	softsel_radius = label
	mods = cmds.getModifiers()
	if mods ==1:
		return cmds.floatField(user_specified_softsel_step, e= True,v=softsel_radius)
	cmds.softSelect(e=True, softSelectDistance=softsel_radius)
	print("Soft Selection Radius set to "+ str(softsel_radius))

def set_softsel_fallof_mode (label, *args):
	current_context = cmds.currentCtx()
	if "art" in current_context:
		return cmds.warning("Not in a transform context.")
	mode_value= '("' +label+'");'
	cmd = 'setSoftSelectFalloffMode' + mode_value
	mel.eval(cmd)
	print("Soft Selection set to "+ label)


#REPLACE SMOOTH AND FLOOD

def flood_user_value (*args) :
	current_context = cmds.currentCtx()
	if "art" not in current_context:
		return cmds.warning("Not in Skin Paint Context")
	current_value = cmds.artAttrCtx(current_context, q=True, value = True)
	mods = cmds.getModifiers()
	if mods ==1:
		flood_value = 0
		cmds.artAttrCtx(current_context, e=True, value=flood_value)
		cmds.artAttrCtx(current_context, e=True, clear = True)
		cmds.artAttrCtx(current_context, e=True, value=current_value)
		return
	flood_value = 1
	cmds.artAttrCtx(current_context, e=True, value=flood_value)
	cmds.artAttrCtx(current_context, e=True, clear = True)
	cmds.artAttrCtx(current_context, e=True, value=current_value)
	print("Paint Flood with value : " + str(flood_value))

def set_operation_replace(*args):
	current_context = cmds.currentCtx()
	if "art" not in current_context:
		return cmds.warning("Not in Skin Paint Context")
	mel.eval('artAttrPaintOperation artAttrCtx  Replace;')
	print("Operation set to Smooth")	
		

def set_operation_smooth(*args):
	current_context = cmds.currentCtx()
	if "art" not in current_context:
		return cmds.warning("Not in Skin Paint Context")
	mel.eval('artAttrPaintOperation artAttrCtx Smooth;')
	print("Operation set to Smooth")



#TRANSFORM CONSTRAINTS FUNCTIONS

def set_edge_constraint (label, *args):
	current_context = cmds.currentCtx()
	if "art" in current_context:
		return cmds.warning("Not in a transform context.")
	mode_value= label
	print mode_value
	cmd = 'manipMoveSetXformConstraint ' + mode_value
	mel.eval(cmd)
	print("Transform_constraint set to "+ label)

#EXTRAS FUNCTIONS

def open_graph_editor(*args):
	mel.eval('GraphEditor;')


def open_tween_machine (*args):
    mel.eval('tweenMachine')

#UI FUNCTIONS

def populate_brush_radius_buttons ():
	button_values = PRESET_VALUES.get('brush_buttons_values')
	for i in button_values :
		annotation_text = 'Set Brush Radius to ' + str(i) + ' Use SHIFT+CLICK to set as step value'
		cmds.button(label = i, annotation = annotation_text, command = partial (set_brush_radius_from_button, i))


def populate_sofsel_radius_buttons ():
	button_values = PRESET_VALUES.get('softsel_buttons_values')
	for i in button_values :
		annotation_text = 'Set Soft Selection Radius to ' + str(i) + '. Use SHIFT+CLICK to set as step value'
		cmds.button(label = i, annotation = annotation_text, command = partial (set_softsel_radius_from_button, i))




#Create window
window = cmds.window( title="TV Paint Helper")
window_width=180
cmds.columnLayout( adjustableColumn=True, w= window_width )

#PAINT BRUSH TITLE
cmds.separator(h=10)
cmds.text("Paint Brush Radius")
cmds.separator(h=10)

#PAINT BRUSH BUTTONS
cmds.rowColumnLayout(adjustableColumn=True, numberOfColumns=3, columnWidth=[(1, 60), (2, 60), (3, 60)] )
cmds.button(label='+',annotation='Increase Brush Radius', command= increase_brush_radius,width=60 )
step_default_value = PRESET_VALUES.get('brush_step_default_value')
user_specified_step = cmds.floatField(editable = True, width=60, v=step_default_value,annotation = "Set Step Value")
cmds.button(label='-',annotation='decrease Brush Radius', command= decrease_brush_radius, width=60 )
populate_brush_radius_buttons()
cmds.setParent('..')

#REPLACE SMOOTH AND FLOOD BUTTONS
cmds.rowColumnLayout(adjustableColumn=True, numberOfColumns=2, columnWidth=[(1, 90), (2, 90)] )
cmds.button(label='Replace', command = set_operation_replace)
cmds.button(label='Smooth', command= set_operation_smooth)
cmds.setParent('..')
cmds.button(label='Flood', command= flood_user_value, annotation = 'Flood Smooth or Replace with value 1.  Use SHIFT+CLICK to Flood replace with value 0')

#SOFT SELECTION RADIUS TITLE
cmds.rowColumnLayout(adjustableColumn=True, numberOfColumns=1, w=window_width )
cmds.separator(h=10)
cmds.text("Soft Selection Radius")
cmds.separator(h=10)

#SOFT SELECTION RADIUS BUTTONS
cmds.rowColumnLayout(adjustableColumn=True, numberOfColumns=3, columnWidth=[(1, 60), (2, 60), (3, 60)] )

cmds.button(label='+',annotation='Increase Soft Selection Radius', command= increase_softsel_radius,width=60 )
step_default_value = PRESET_VALUES.get('softsel_step_default_value')
user_specified_softsel_step = cmds.floatField(editable = True, width=60, v=step_default_value, annotation = "Set Step Value")
cmds.button(label='-',annotation='decrease Soft Selection Radius', command= decrease_softsel_radius, width=60 )
populate_sofsel_radius_buttons()

#SOFT SELECTION FALLOFF MODE BUTTONS
cmds.text(label='Falloff: ', width =60)
cmds.button(label='Volume', command= partial (set_softsel_fallof_mode, 'Volume'), width=60)
cmds.button(label='Surface', command= partial (set_softsel_fallof_mode, 'Surface'), width=60)

#TRANSFORM CONSTRAINT MODE BUTTONS
cmds.text(label='Constraint: ', width =60)
cmds.button(label='Off', command= partial (set_edge_constraint, 'none'), width=60)
cmds.button(label='EdgeLoop', command= partial (set_edge_constraint, 'edge'), width=60)
cmds.setParent( '..' )

#EXTRAS TEXT AND BUTTONS
cmds.separator(h=10)
cmds.text("Extras")
cmds.separator(h=10)

cmds.button(label='Graph Editor', command= open_graph_editor)
cmds.button(label='Tween Machine', command= open_tween_machine)

#Show the window that we created (window)
cmds.showWindow( window )
