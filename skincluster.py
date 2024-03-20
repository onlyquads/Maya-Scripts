'''
# Description
This is a collection of functions to deal with skincluster in maya

#Usage examples:

- Reset selected objects skinclusters. Useful when bone position has changed
to reset the mesh in bind pose without any deformations:
```python
import maya.cmds as mc
reset_skincluster(mc.ls(sl=True))
```

- Delete skinclusters of selected objects:

```python
import maya.cmds as mc
delete_skincluster_nodes(mc.ls(sl=True))
```
'''

import maya.cmds as mc


def get_skin(node):
    '''Usage: get_skin(mc.ls(sl=True)[0])'''
    skin_dict = {}
    shape = mc.listRelatives(node, s=True, ni=True)[-1]
    list_history = mc.listHistory(shape)
    skin = mc.ls(list_history, type='skinCluster') or []
    if skin:
        skin_dict[skin[0]] = mc.skinCluster(skin[0], query=True, inf=True)
    return skin_dict


def reset_skincluster(nodes):
    '''Usage: reset_skincluster(mc.ls(sl=True))'''
    for node in nodes:
        skincluster = get_skin(node)
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


def delete_skincluster_nodes(nodes):
    skin_cluster_nodes = get_skin(nodes)
    for skincluster in skin_cluster_nodes:
        mc.delete(skincluster)
        print(f'Node : {skincluster} deleted')


def reset_skincluster_no_hack(nodes):
    for node in nodes:
        skin = get_skin(node)
        ids_list = mc.getAttr(skin + '.matrix', mi=True)
        for id in ids_list:
            skin_connections = mc.listConnections(
                skin + '.matrix[' + str(id) + ']', s=True)[0]
            value = mc.getAttr(skin_connections + '.worldInverseMatrix')
            mc.setAttr(
                skin + '.bindPreMatrix[' + str(id) + ']', type='matrix', *value)



