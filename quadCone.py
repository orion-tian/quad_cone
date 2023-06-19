import maya.cmds as cmds
from functools import partial

coneName = 'quad_cone'
coneShapeName = 'polyCone1'

def adjAttr(slider, attr, dataType, *args):
    if dataType == 'float':
        val = cmds.floatSliderGrp(slider, q=True, value=True)
    elif dataType == 'int':
        val = cmds.intSliderGrp(slider, q=True, value=True)
    else:
        print('Wrong Data type inputted.')
    
    cmds.setAttr(coneShapeName + '.' + attr, val) 

def movePoint(floatField, axis, dir, saSlider, shSlider, scSlider, *args):
    # disable subdivision controls
    cmds.intSliderGrp(saSlider, edit=True, enable=False)
    cmds.intSliderGrp(shSlider, edit=True, enable=False)
    cmds.intSliderGrp(scSlider, edit=True, enable=False)

    # get value of field
    val = cmds.floatField(floatField, q=True, value=True)
    if dir == 'neg':
        val = val*-1
    
    # make dictionary of vertices grouped by height
    sel_vtx = cmds.ls(coneName + '.vtx[:]', fl=True)
    vtx_by_h = {}
    for vtx in sel_vtx:
        y_coord = cmds.xform(vtx, q=True, ws=True, t=True)[1]
        if y_coord in vtx_by_h.keys():
            vtx_by_h[y_coord].append(vtx)
        else:
            vtx_by_h[y_coord] = [vtx]

    # adjust vertices
    num_layers = float(len(vtx_by_h)) - 1.0
    i = 0
    for k in vtx_by_h.keys():
        for v in vtx_by_h[k]:
            if i!=0:
                posi = cmds.xform(v, q=True, ws=True, t=True)
                if axis == 'x': 
                    cmds.move(posi[0] + val * i/num_layers, posi[1], posi[2], v, ws=True)
                elif axis == 'z':
                    cmds.move(posi[0], posi[1], posi[2] + val * i/num_layers, v, ws=True)
                else:
                    print("Argument wrong")
        i += 1

def resetCallback(pwindID, *pArgs):
        # remake UI
        if cmds.window(pwindID, exists=True):
            cmds.deleteUI(pwindID)
        createUI("Quad Cone")

        # remake cone
        conesLst = cmds.ls(coneName)
        if len(conesLst)>0:
            cmds.delete(conesLst)
        
        cmds.polyCone(name = coneName, sa=3)
        cmds.select(coneName, r=True)

def createUI(pWindowTitle):
    windowID = "myWindowID"
    
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
        
    cmds.window(windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True)
    cmds.columnLayout(adjustableColumn=True)
    
    # subdivision controls
    cmds.separator(h=10, style='none')

    subAxSlider = cmds.intSliderGrp(label='Subdivision Axis', columnAlign= (1,'right'), 
                                    field=True, min=3, max=50, value=3, step=1, dc = 'empty')
    cmds.intSliderGrp(subAxSlider,  e=True, dc = partial(adjAttr, subAxSlider, 'sa', 'int'))

    subHSlider = cmds.intSliderGrp(label='Subdivision Height', columnAlign= (1,'right'), 
                                   field=True, min=1, max=50, value=1, step=1, dc = 'empty')
    cmds.intSliderGrp(subHSlider,  e=True, dc = partial(adjAttr, subHSlider, 'sh', 'int'))

    subCapSlider = cmds.intSliderGrp(label='Subdivision Cap', columnAlign= (1,'right'), 
                                  field=True, min=0, max=20, value=0, step=1, dc = 'empty')
    cmds.intSliderGrp(subCapSlider,  e=True, dc = partial(adjAttr, subCapSlider, 'sc', 'int'))

    cmds.separator(h=10, style='out')

    # height and radius controls
    heightSlider = cmds.floatSliderGrp(label='Height', columnAlign= (1,'right'), 
                                       field=True, min=0.1, max=20, value=2, step=0.1, dc = 'empty')
    cmds.floatSliderGrp(heightSlider,  e=True, dc = partial(adjAttr, heightSlider, 'height', 'float'))

    radiusSlider = cmds.floatSliderGrp(label='Radius', columnAlign= (1,'right'), 
                                       field=True, min=0.1, max=20, value=1, step=0.1, dc = 'empty')
    cmds.floatSliderGrp(radiusSlider,  e=True, dc = partial(adjAttr, radiusSlider, 'radius', 'float'))

    cmds.separator(h=10, style='none')

    # apex controls
    cmds.text("Adjust position of apex")
    
    cmds.separator(h=10, style='none')

    cmds.rowColumnLayout(numberOfColumns=6, 
                         columnWidth=[(1,145),(2, 75), (3, 10), (4,65),(5,5),(6,65)],
                         columnOffset=[(1,"right", 3)])
    
    cmds.text(label="X-axis: ")
    xAxisFloat = cmds.floatField(min = 0.1, max = 5, value = 1, step = 0.1)
    cmds.separator(h=10, style='none')
    cmds.button(label='<-', command=partial(movePoint, xAxisFloat, 'x', 'neg', 
                                            subAxSlider, subHSlider, subCapSlider))
    cmds.separator(h=10, style='none')
    cmds.button(label='->', command=partial(movePoint, xAxisFloat, 'x', 'pos', 
                                            subAxSlider, subHSlider, subCapSlider))
    cmds.text(label="Z-axis: ")
    zAxisFloat = cmds.floatField(min = 0.1, max = 5, value = 1, step = 0.1)
    cmds.separator(h=10, style='none')
    cmds.button(label='<-', command=partial(movePoint, zAxisFloat, 'z', 'neg', 
                                            subAxSlider, subHSlider, subCapSlider))
    cmds.separator(h=10, style='none')
    cmds.button(label='->', command=partial(movePoint, zAxisFloat, 'z', 'pos',
                                            subAxSlider, subHSlider, subCapSlider))
    
    #reset button
    cmds.setParent('..')
    cmds.separator(h=10, style='none')
    cmds.button(label='Reset', command=partial(resetCallback, windowID))
    
    cmds.showWindow()

createUI("Quad Cone")

# delete existing cones
conesLst = cmds.ls(coneName)
if len(conesLst)>0:
    cmds.delete(conesLst)

# create cone to manipulate
cmds.polyCone(name = coneName, sa=3)
cmds.select(coneName, r=True)