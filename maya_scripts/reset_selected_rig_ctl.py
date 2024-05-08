# This script will reset transform value of the selected controllers
# Only applies to Translate, Rotate, and Scale attributes!!!
# Select one or more rig controllers and run the script

import maya.cmds as cmds


def get_transform_attributes():
    axes = ('X', 'Y', 'Z')
    transform_attributes = ('translate', 'rotate', 'scale')
    transfrom_attr_list = []
    for i in transform_attributes:
        for axis in axes:
            transfrom_attr_list.append(i + axis)
    return transfrom_attr_list


def default_transform_value(transform_attr):
    default_value = 0
    # Need to set it to 1 for default scale value
    if 'scale' in transform_attr:
        default_value = 1
    return default_value


def set_attr(object_name):
    transfrom_attr_list = get_transform_attributes()
    all_attr_list = cmds.listAttr(object_name, k=True)
    for i in transfrom_attr_list:
        if i in all_attr_list:
            default_value = default_transform_value(i)
            cmds.setAttr(object_name + '.' + i, default_value)
    print('object named ' + object_name + ' has been reset')


def reset_selected():

    selected_objects = cmds.ls(selection=True, tr=True)
    if not selected_objects:
        return cmds.warning(
            'No object selected. Please select objects.')
    for i in selected_objects:
        set_attr(i)


if __name__ == '__main__':
    reset_selected()
