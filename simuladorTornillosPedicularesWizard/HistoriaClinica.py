# -*- coding: UTF-8 -*-
from __main__ import vtk, qt, ctk, slicer

class HistoriaClinica(ctk.ctkWorkflowWidgetStep) :

    def __init__(self, stepid):
        self.initialize(stepid)
        self.nextButtonText = 'Siguiente'
        self.backButtonText = 'Volver'
        self.setName( '3. Historia clinica del caso'  )
        
    def createUserInterface(self):

        font =qt.QFont("Sans Serif", 12, qt.QFont.Bold)
        self.__layout = qt.QFormLayout( self )

        self.labelInstruccionesDeUsoBienvenido = qt.QLabel("Historia Clinica: \n\nEl paciente presenta ...")
        self.labelInstruccionesDeUsoBienvenido.setFont(font)
        self.__layout.addRow(self.labelInstruccionesDeUsoBienvenido)
        
    
    def onEntry(self, comingFrom, transitionType):
        super(HistoriaClinica, self).onEntry(comingFrom, transitionType)
        self.ctimer = qt.QTimer()
        self.ctimer.singleShot(0, self.killButton)
        slicer.mrmlScene.Clear(0)
        self.cargarScene()

    def onExit(self, goingTo, transitionType):
        super(HistoriaClinica, self).onExit(goingTo, transitionType)
    
    def validate(self, desiredBranchId):
        validationSuceeded = True
        super(HistoriaClinica, self).validate(validationSuceeded, desiredBranchId)
        
    def killButton(self):
    	bl = slicer.util.findChildren(text='ModuloPlaneacion' )
        b2 = slicer.util.findChildren(text='IngresoAlumno' )
        bl[0].hide()
        b2[0].hide()

    def cargarScene(self):
        path2='C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Modelos\Lumbar 2.5 B31s - 4/4 Lumbar  2.5  B31s.nrrd'
        slicer.util.loadVolume(path2)
        self.layoutManager = slicer.app.layoutManager() 
        self.layoutManager.setLayout(27)
