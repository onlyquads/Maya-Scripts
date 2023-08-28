import maya.cmds as cmds


def get_position(target_name):
    pos_x = cmds.getAttr(target_name + '.translateX')
    pos_y = cmds.getAttr(target_name + '.translateY')
    pos_z = cmds.getAttr(target_name + '.translateZ')

    rot_x = cmds.getAttr(target_name + '.rotateX')
    rot_y = cmds.getAttr(target_name + '.rotateY')
    rot_z = cmds.getAttr(target_name + '.rotateZ')
    return pos_x, pos_y, pos_z, rot_x, rot_y, rot_z


def align_to_last_selected_object():
    selection = cmds.ls(selection=True)
    pos_x, pos_y, pos_z, rot_x, rot_y, rot_z = get_position(selection[-1])
    selection.remove(selection[-1])
    for i in selection:
        cmds.setAttr(i + '.translateX', pos_x)
        cmds.setAttr(i + '.translateY', pos_y)
        cmds.setAttr(i + '.translateZ', pos_z)
        cmds.setAttr(i + '.rotateX', rot_x)
        cmds.setAttr(i + '.rotateY', rot_y)
        cmds.setAttr(i + '.rotateZ', rot_z)
