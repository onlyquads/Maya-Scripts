'''
Collection of functions to work with skinclusters

'''

import maya.cmds as mc


def get_skin(msh):
    '''Usage: get_skin(mc.ls(sl=True)[0])'''
    skin_dict = {}
    shape = mc.listRelatives(msh, s=True, ni=True)[-1]
    list_history = mc.listHistory(shape)
    skin = mc.ls(list_history, type='skinCluster') or []
    if skin:
        skin_dict[skin[0]] = mc.skinCluster(skin[0], query=True, inf=True)
    return skin_dict


def reset_skincluster(mesh_list):
    '''Usage: reset_skincluster(mc.ls(sl=True))'''
    for msh in mesh_list:
        skincluster = get_skin(msh)
        joint_indices = mc.getAttr(skincluster+'.matrix', mi=True)
        for id in joint_indices:
            connected_joints = mc.listConnections(
                skincluster+'.matrix['+str(id)+']', s=True) or []
            if connected_joints:
                sk = connected_joints[0]
                has_hack_skin = mc.listConnections(
                    skincluster+'.bindPreMatrix['+str(id)+']', s=True) or []
                if not has_hack_skin:
                    val = mc.getAttr(sk + '.worldInverseMatrix')
                    mc.setAttr(
                        skincluster+'.bindPreMatrix['+str(id)+']',
                        type='matrix',
                        *val)
