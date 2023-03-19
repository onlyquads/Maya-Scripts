###This script creates a window with shortcut buttons for quick access while painting skincluster influences in maya

import maya.cmds as cmds
import maya.mel as mel
from functools import partial

skin_paint_version = 1.0

SKIN_PAINT_PRESET_VALUES = dict(

	default_step_value = 1,
	skin_paint_values=[
		(0),
		(0.25),
		(0.50),
		(0.75),
		(1),
		(0.1),
		(0.2),
		(0.8),
		(0.9)
		]
)



def get_current_paint_value ():

	current_context = cmds.currentCtx()

	if "artAttrSkinContext" in current_context :
		current_paint_value = cmds.artAttrCtx(current_context, q=True, value = True)
		#cmds.text(current_paint_value_text, e=True, v=current_paint_value)
		return current_paint_value
	
	else:
		current_paint_value = "N/A"
		return current_paint_value


def set_paint_value (label, *args):

	
	current_context = cmds.currentCtx()
	if "artAttr" not in current_context:
		return cmds.warning("Not in Skin Paint Context")
	#Check if user press SHIFT key
	mods = cmds.getModifiers()
	paint_value = label
	if mods ==1:
		return cmds.floatField(user_specified_step, e= True,v=paint_value)

	cmds.artAttrCtx(current_context, e=True, value=paint_value)
	print("Paint Value set to " + str(paint_value))

		


def increase_paint_value (*args):
	current_context = cmds.currentCtx()
	if "artAttr" not in current_context:
		return cmds.warning("Not in Skin Paint Context")
	step_value = cmds.floatField(user_specified_step, q=True, v=True)
	current_paint_value = cmds.artAttrCtx(current_context, query=True, value=True)
	new_paint_value = current_paint_value + step_value
	cmds.artAttrCtx(current_context, e=True, radius=new_paint_value)
	print("Paint Value set to " + str(new_paint_value))

def decrease_paint_value (*args):
	current_context = cmds.currentCtx()
	if "artAttr" not in current_context:
		return cmds.warning("Not in Skin Paint Context")
	step_value = cmds.floatField(user_specified_step, q=True, v=True)
	current_paint_value = cmds.artAttrCtx(current_context, query=True, value=True)
	new_paint_value = current_paint_value - step_value
	cmds.artAttrCtx(current_context, e=True, value=new_paint_value)
	print("Paint Value set to " + str(new_paint_value))
	
		

def flood_user_value (*args) :

	current_context = cmds.currentCtx()
	if "artAttr" not in current_context:
		return cmds.warning("Not in Skin Paint Context")
	mods = cmds.getModifiers()
	if mods ==1:
		current_value = cmds.artAttrCtx(current_context, q=True, value=True)
		step_value = 0
		cmds.artAttrCtx(current_context, e=True, value=step_value)
		cmds.artAttrCtx(current_context, e=True, clear = True)
		cmds.artAttrCtx(current_context, e=True, value=current_value)
		print("Paint Flood with value : " + str(step_value))
		return
	current_value = cmds.artAttrCtx(current_context, q=True, value=True)
	step_value = 1
	cmds.artAttrCtx(current_context, e=True, value=step_value)
	cmds.artAttrCtx(current_context, e=True, clear = True)
	cmds.artAttrCtx(current_context, e=True, value=current_value)
	print("Paint Flood with value : " + str(step_value))

		



def set_operation_replace(*args):
	current_context = cmds.currentCtx()
	if "artAttr" not in current_context:
		return cmds.warning("Not in Skin Paint Context")
	mel.eval('artAttrPaintOperation artAttrSkinPaintCtx Replace;')
	print("Operation set to Smooth")
		

def set_operation_smooth(*args):

	current_context = cmds.currentCtx()
	if "artAttr" not in current_context:
		return cmds.warning("Not in Skin Paint Context")
	mel.eval('artAttrPaintOperation artAttrSkinPaintCtx Smooth;')
	print("Operation set to Smooth")
		



def populate_skin_paint_buttons():
	values_list = SKIN_PAINT_PRESET_VALUES.get('skin_paint_values')

	for i in values_list:
		annotation_text = 'Set Paint Value to '+str(i)+'. Use SHIFT+CLICK to set as Step value'
		cmds.button(label=i,annotation = annotation_text, command = partial (set_paint_value, i))


#Create window
window = cmds.window( title="Skin Paint Helper")
window_width=180
cmds.columnLayout( adjustableColumn=True, w= window_width )

#PAINT TOOL TITLE
cmds.separator(h=10)
cmds.text("Skin Paint Helper")
cmds.separator(h=10)


'''
cmds.rowColumnLayout( numberOfColumns = 2)
cmds.text("Current Value :")
current_paint_value_text = cmds.text(get_current_paint_value())
cmds.setParent('..')
'''


#PAINT VALUE BUTTONS

cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1,90),(2,90)])
cmds.button(label='Replace', annotation ='Set Operation to Replace', command=set_operation_replace)
cmds.button(label='Smooth', annotation ='Set Operation to Smooth', command=set_operation_smooth)
cmds.setParent('..')

cmds.rowColumnLayout( numberOfColumns=5, columnWidth=[(1, 36), (2, 36), (3, 36),(4,36),(5,36) ] )

populate_skin_paint_buttons()

cmds.setParent('..')


cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 60), (2, 60), (3, 60)] )
cmds.button(label='+',annotation='Increase paint Value', command= increase_paint_value,width=60 )
default_step_value = SKIN_PAINT_PRESET_VALUES.get('default_step_value')
user_specified_step = cmds.floatField(editable = True, width=60, v=default_step_value ,annotation = "Set Step Value")
cmds.button(label='-',annotation='decrease paint Value', command= decrease_paint_value, width=60 )
cmds.setParent('..')
cmds.button(label='Flood', annotation='Flood paint Value', command = flood_user_value)


cmds.showWindow( window )
