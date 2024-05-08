import maya.cmds as mc


def get_current_eval():
    return mc.evaluationManager(query=True, mode=True)[0]


def switch_to_parallel():
    mc.evaluationManager(mode='parallel')
    mc.warning('Evaluation Mode set to Parallel')


def switch_to_dg():
    mc.evaluationManager(mode='off')
    mc.warning('Evaluation Mode set to DG')


def switch_to_serial():
    mc.evaluationManager(mode='serial')
    mc.warning('Evaluation Mode set to Serial')


def switch_evaluation_mode():
    current_eval = get_current_eval()
    if current_eval == 'off':
        switch_to_parallel()
        return
    switch_to_dg()
