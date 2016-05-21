# -*- coding: UTF-8 -*-
from __main__ import vtk, qt, ctk, slicer

class Inicio(ctk.ctkWorkflowWidgetStep) :

    def __init__(self, stepid):
        self.initialize(stepid)
        self.setName( 'Ver actividad'  )
        
    def createUserInterface(self):

        font =qt.QFont("Sans Serif", 12, qt.QFont.Bold)
        self.__layout = qt.QFormLayout( self )
    
    def onEntry(self, comingFrom, transitionType):
        super(Inicio, self).onEntry(comingFrom, transitionType)
        self.ctimer = qt.QTimer()
        self.ctimer.singleShot(0, self.killButton)

    def onExit(self, goingTo, transitionType):
        super(Inicio, self).onExit(goingTo, transitionType)
        
    
    def validate(self, desiredBranchId):
        validationSuceeded = True
        super(Inicio, self).validate(validationSuceeded, desiredBranchId)
        
    def killButton(self):
    	print "Holi"

