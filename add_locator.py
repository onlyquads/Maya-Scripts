# Create locators aligned to each selected object or to center of world if no selection.

import maya.cmds as mc

LOCATOR_SCALE = 5


def set_locator_scale(locator):
	
    mc.setAttr(locator+'.localScaleX', LOCATOR_SCALE)
    mc.setAttr(locator+'.localScaleY', LOCATOR_SCALE)
    mc.setAttr(locator+'.localScaleZ', LOCATOR_SCALE)


def create_aligned_locator():

	selection = mc.ls(selection = True)
	if selection:
		for node in selection :
			matrix = mc.xform(node, query=True, worldSpace=True, matrix=True)
			locator = mc.spaceLocator()
			mc.xform(locator, matrix=matrix)
			set_locator_scale(locator=locator)
	else:
		locator = mc.spaceLocator()
		set_locator_scale(locator=locator)



