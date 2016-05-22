# -*- coding: UTF-8 -*-
from __main__ import vtk, qt, ctk, slicer

class IngresoAlumno(ctk.ctkWorkflowWidgetStep) :

    def __init__(self, stepid):
        self.initialize(stepid)
        self.setName( '2. Ingreso Alumno'  )
        
    def createUserInterface(self):

        font =qt.QFont("Sans Serif", 12, qt.QFont.Bold)
        self.__layout = qt.QFormLayout( self )
    
    def onEntry(self, comingFrom, transitionType):
        super(IngresoAlumno, self).onEntry(comingFrom, transitionType)
        self.ctimer = qt.QTimer()
        self.ctimer.singleShot(0, self.killButton)

    def onExit(self, goingTo, transitionType):
        super(IngresoAlumno, self).onExit(goingTo, transitionType)
        
    
    def validate(self, desiredBranchId):
        validationSuceeded = True
        super(IngresoAlumno, self).validate(validationSuceeded, desiredBranchId)
        

    def killButton(self):
    	bl = slicer.util.findChildren(text='ModuloPlaneacion' )
    	bl[0].hide()

