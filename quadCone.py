import maya.cmds as cmds
from functools import partial

coneShapeName = 'polyCone1'

def adjAttr(slider, attr, dataType, *args):
    if dataType == 'float':
        val = cmds.floatSliderGrp(slider, q=True, value=True)
    elif dataType == 'int':
        val = cmds.intSliderGrp(slider, q=True, value=True)
    else:
        print('Wrong Data type inputted.')
    
    cmds.setAttr(coneShapeName + '.' + attr, val) 

def createUI(pWindowTitle):
    windowID = "myWindowID"
    
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
        
    cmds.window(windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True)
    cmds.columnLayout(adjustableColumn=True)
                         
    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)
    
    # the UI components
    cmds.separator(h=10, style='none')

    HeightSlider = cmds.floatSliderGrp(label='Height', columnAlign= (1,'right'), 
                                       field=True, min=1, max=20, value=1, step=0.1, dc = 'empty')
    cmds.floatSliderGrp(HeightSlider,  e=True, dc = partial(adjAttr, HeightSlider, 'height', 'float'))

    RadiusSlider = cmds.floatSliderGrp(label='Radius', columnAlign= (1,'right'), 
                                       field=True, min=1, max=20, value=1, step=0.1, dc = 'empty')
    cmds.floatSliderGrp(RadiusSlider,  e=True, dc = partial(adjAttr, RadiusSlider, 'radius', 'float'))

    SubAxSlider = cmds.intSliderGrp(label='Subdivision Axis', columnAlign= (1,'right'), 
                                    field=True, min=3, max=50, value=3, step=1, dc = 'empty')
    cmds.intSliderGrp(SubAxSlider,  e=True, dc = partial(adjAttr, SubAxSlider, 'sa', 'int'))

    SubHSlider = cmds.intSliderGrp(label='Subdivision Height', columnAlign= (1,'right'), 
                                   field=True, min=1, max=50, value=1, step=1, dc = 'empty')
    cmds.intSliderGrp(SubHSlider,  e=True, dc = partial(adjAttr, SubHSlider, 'sh', 'int'))

    CapSlider = cmds.intSliderGrp(label='Subdivision Cap', columnAlign= (1,'right'), 
                                  field=True, min=0, max=20, value=0, step=1, dc = 'empty')
    cmds.intSliderGrp(CapSlider,  e=True, dc = partial(adjAttr, CapSlider, 'sc', 'int'))

    cmds.separator(h=10, style='none')

    cmds.button(label='Cancel', command=cancelCallback)
    
    cmds.showWindow()

createUI("Quad Cone")

coneName = 'pCone1'
# delete existing cones
conesLst = cmds.ls(coneName)
if len(conesLst)>0:
    cmds.delete(conesLst)

# create cone to manipulate
cmds.polyCone(sa=3)
cmds.select(coneName, r=True)