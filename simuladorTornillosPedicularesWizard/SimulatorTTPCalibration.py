# -*- coding: UTF-8 -*-
from __main__ import vtk, qt, ctk, slicer

class SimulatorTTPCalibration(ctk.ctkWorkflowWidgetStep) :

    def __init__(self, stepid):
        self.initialize(stepid)
        self.nextButtonText = 'Siguiente'
        self.backButtonText = 'Volver'
        self.setName( u'. Calibración'  )
        
    def createUserInterface(self):

        font =qt.QFont("Sans Serif", 12, qt.QFont.Bold)
        self.__layout = qt.QFormLayout( self )

        self.labelInstruccionesDeUsoBienvenido = qt.QLabel("Historia Clinica: \n\nEl paciente presenta ...")
        self.labelInstruccionesDeUsoBienvenido.setFont(font)
        self.__layout.addRow(self.labelInstruccionesDeUsoBienvenido)
        
    def onEntry(self, comingFrom, transitionType):
        super(SimulatorTTPCalibration, self).onEntry(comingFrom, transitionType)
        self.ctimer = qt.QTimer()
        self.ctimer.singleShot(0, self.killButton)
        slicer.mrmlScene.Clear(0)
        self.cargarScene()

    def onExit(self, goingTo, transitionType):
        super(SimulatorTTPCalibration, self).onExit(goingTo, transitionType)
    
    def validate(self, desiredBranchId):
        validationSuceeded = True
        super(SimulatorTTPCalibration, self).validate(validationSuceeded, desiredBranchId)
        
    def killButton(self):
    	
        b2 = slicer.util.findChildren(text='IngresoAlumno' )
        b3 = slicer.util.findChildren(text='MenuProfesor')
        b4 = slicer.util.findChildren(text='SimulatorTTPCalibration')
        
        b2[0].hide()
        b3[0].hide()
        b4[0].hide()

    def cargarScene(self):
        print "."
        
