# Simple script to filter selections
import maya.cmds as mc


def filter_reset_all():
    mc.selectMode(object=True)
    mc.selectType(allObjects=True)


def filter_only_curves():
    mc.selectMode(object=True)
    mc.selectType(
        handle=False,
        ikHandle=False,
        joint=False,
        polymesh=False,
        nurbsCurve=True,
        cos=True,
        stroke=True,
        nurbsSurface=False,
        subdiv=False,
        plane=False,
        lattice=False,
        cluster=False,
        sculpt=False,
        nonlinear=False,
        particleShape=False,
        emitter=False,
        field=False,
        spring=False,
        rigidBody=False,
        fluid=False,
        hairSystem=False,
        follicle=False,
        nCloth=False,
        nRigid=False,
        dynamicConstraint=False,
        rigidConstraint=False,
        collisionModel=False,
        light=False,
        camera=False,
        texture=False,
        ikEndEffector=False,
        locator=False,
        dimension=False
        )


def filter_curves_and_locators():
    mc.selectMode(object=True)
    mc.selectType(
        handle=False,
        ikHandle=False,
        joint=False,
        polymesh=False,
        nurbsCurve=True,
        cos=True,
        stroke=True,
        nurbsSurface=False,
        subdiv=False,
        plane=False,
        lattice=False,
        cluster=False,
        sculpt=False,
        nonlinear=False,
        particleShape=False,
        emitter=False,
        field=False,
        spring=False,
        rigidBody=False,
        fluid=False,
        hairSystem=False,
        follicle=False,
        nCloth=False,
        nRigid=False,
        dynamicConstraint=False,
        rigidConstraint=False,
        collisionModel=False,
        light=False,
        camera=False,
        texture=False,
        ikEndEffector=False,
        locator=True,
        dimension=False
        )
