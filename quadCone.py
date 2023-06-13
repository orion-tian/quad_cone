import maya.cmds as cmds
from functools import partial

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
    cmds.floatSliderGrp(HeightSlider,  e=True) #dc = partial(adjustHeight, HeightSlider))

    RadiusSlider = cmds.floatSliderGrp(label='Radius', columnAlign= (1,'right'), 
                                       field=True, min=1, max=20, value=1, step=0.1, dc = 'empty')
    cmds.floatSliderGrp(RadiusSlider,  e=True) # dc = partial(adjustRadius, RadiusSlider))

    SubHSlider = cmds.intSliderGrp(label='Subdivision Height', columnAlign= (1,'right'), 
                                   field=True, min=1, max=20, value=1, step=0.1, dc = 'empty')
    cmds.intSliderGrp(SubHSlider,  e=True) # dc = partial(adjustSubH, SubHSlider))

    CapSlider = cmds.intSliderGrp(label='Subdivision Cap', columnAlign= (1,'right'), 
                                  field=True, min=2, max=20, value=2, step=0.1, dc = 'empty')
    cmds.intSliderGrp(CapSlider,  e=True) #dc = partial(adjustCap, CapSlider))

    SubAxSlider = cmds.intSliderGrp(label='Subdivision Axis', columnAlign= (1,'right'), 
                                    field=True, min=6, max=20, value=6, step=0.1, dc = 'empty')
    cmds.intSliderGrp(SubAxSlider,  e=True) #dc = partial(adjustSubAx, SubAxSlider))

    cmds.separator(h=10, style='none')

    cmds.button(label='Cancel', command=cancelCallback)
    

    cmds.showWindow()

createUI("Quad Cone")

cmds.polyCone()