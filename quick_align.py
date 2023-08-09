import maya.cmds as cmds

def get_position(target_name):
    pos_x = cmds.getAttr(target_name+'.translateX')
    pos_y = cmds.getAttr(target_name+'.translateY')
    pos_z = cmds.getAttr(target_name+'.translateZ')

    rot_x = cmds.getAttr(target_name+'.rotateX')
    rot_y = cmds.getAttr(target_name+'.rotateY')
    rot_z = cmds.getAttr(target_name+'.rotateZ')
    print('target position stored')
    return pos_x, pos_y, pos_z, rot_x, rot_y, rot_z

selection = cmds.ls(selection=True)

print selection

pos_x, pos_y, pos_z, rot_x, rot_y, rot_z = get_position(selection[1])

first_object = selection[0]
cmds.setAttr(first_object+'.translateX', pos_x)
cmds.setAttr(first_object+'.translateY', pos_y)
cmds.setAttr(first_object+'.translateZ', pos_z)
cmds.setAttr(first_object+'.rotateX', rot_x)
cmds.setAttr(first_object+'.rotateY', rot_y)
cmds.setAttr(first_object+'.rotateZ', rot_z)
print('Align done')


