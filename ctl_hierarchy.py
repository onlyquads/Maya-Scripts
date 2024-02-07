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


def compare_names(node_list):

    '''Compare returned node list to the selected first item'''

    filtered_items = []

    root_name = '_'.join(node_list[0].split(NAME_SPLIT)[:PREFIX_ELEMENT_COUNT])
    
    root_name = re.sub(r'\d*$', '', root_name)  # Remove any ending digit

    filtered_items = [item for item in node_list if item.startswith(root_name)]

    return filtered_items



def optional_check(node):
    if CTL_NAME is None or CTL_NAME == '':
        return
    node_sn = mc.ls(node, shortNames=True)[0]
    for i in CTL_NAME:
        if i in node_sn:
            return True
    return False



def is_anim_controller(node):
    # print(f'testing node {node}')
    '''get the given node's shape and returns True if nurbsCurve or locator'''
    shape = mc.listRelatives(node, shapes=True, fullPath=True)

    if shape and mc.nodeType(shape[0]) in ['nurbsCurve', 'locator']:
        if optional_check(shape):
            return True
    return False


def get_controller_hierarchy(node):

    controller_list = []

    shapes = mc.listRelatives(node, shapes=True, fullPath=False)
    if not shapes:
        return

    if is_anim_controller(node):
        controller_list.append(node)


    children = mc.listRelatives(node, allDescendents=True, fullPath=False)
    if not children:
        return controller_list
    for child in children:
        if is_anim_controller(child):
            controller_list.append(child)

    # print(controller_list)

    return controller_list


def select_add(node):
    mc.select(add=node)



def get_rig_parth_child_controller():
    child_list = []
    selection_list = mc.ls(selection=True)

    for i in selection_list:
        controller_list = get_controller_hierarchy(i)

        filtered = compare_names(controller_list)
        print(filtered)
        child_list += filtered

    print('FILTERED')
    print(child_list)

    for i in child_list:
        mc.select(i, add=True)


get_rig_parth_child_controller()