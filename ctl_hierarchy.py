import maya.cmds as mc
import re


# Add an optional name or leave empty
CTL_NAME = [
    '_ctrl',
    ]

# Name split string value:
NAME_SPLIT = '_'

# Prefix element to compare in controller name
PREFIX_ELEMENT_COUNT = 2

ANIM_CTL_TYPE = [
    'nurbsCurve',
    'locator'
    ]


def compare_names(node_list):

    '''Compare returned node list to the first selected item'''

    filtered_items = []

    root_name = '_'.join(node_list[0].split(NAME_SPLIT)[:PREFIX_ELEMENT_COUNT])
    root_name = re.sub(r'\d*$', '', root_name)  # Remove any ending digit

    filtered_items = [item for item in node_list if item.startswith(root_name)]

    return filtered_items


def ctl_string_in_name(node):
    '''if CTL_NAME is set, checks if in node name, if not set, returns True'''
    if CTL_NAME is None or CTL_NAME == '':
        return True
    node_sn = mc.ls(node, shortNames=True)[0]
    for i in CTL_NAME:
        if i in node_sn:
            return True
    return False


def is_anim_controller(node):
    '''get the given node's shape and returns True if nurbsCurve or locator'''

    shape = mc.listRelatives(node, shapes=True, fullPath=True)
    if shape and mc.nodeType(shape[0]) in ANIM_CTL_TYPE:
        return True
    return False


def get_controller_hierarchy_list(node):

    controller_list = []

    if not is_anim_controller(node):
        return
    if not ctl_string_in_name(node):
        return

    controller_list.append(node)

    children = mc.listRelatives(node, allDescendents=True, fullPath=False)
    if not children:
        return controller_list
    for child in children:
        if is_anim_controller(child) and ctl_string_in_name(child):
            controller_list.append(child)

    filtered = compare_names(controller_list)
    return filtered


def get_children_ctl_from_selection():
    children_list = []
    selection_list = mc.ls(selection=True)

    if not selection_list:
        return mc.warning("Please select something")

    for i in selection_list:
        controller_list = get_controller_hierarchy_list(i)
        children_list += controller_list

    children_list = set(children_list)
    mc.warning(f'Found {len(children_list)} items')
    for i in children_list:
        mc.select(i, add=True)


get_children_ctl_from_selection()
