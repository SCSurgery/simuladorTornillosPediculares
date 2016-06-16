# -*- coding: UTF-8 -*-
from __main__ import vtk, qt, ctk, slicer

class MenuProfesor(ctk.ctkWorkflowWidgetStep) :

    def __init__(self, stepid):
        self.initialize(stepid)
        self.nextButtonText = 'Siguiente'
        self.backButtonText = 'Volver'
        self.setName( u'. Menú profesor'  )
        self.__parent = super( MenuProfesor, self )
        
    def createUserInterface(self):

        font =qt.QFont("Sans Serif", 12, qt.QFont.Bold)
        self.__layout = self.__parent.createUserInterface()
        self.__layout = qt.QFormLayout( self )
        loader = qt.QUiLoader()
        path='C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\Interfaz Grafica\MenuProfesor.ui'
        qfile = qt.QFile(path)
        qfile.open(qt.QFile.ReadOnly)
        widget = loader.load(qfile)
        self.widget = widget
        self.__layout.addWidget(widget)
        self.widget.setMRMLScene(slicer.mrmlScene)
        
    
    def onEntry(self, comingFrom, transitionType):
        super(MenuProfesor, self).onEntry(comingFrom, transitionType)
        self.ctimer = qt.QTimer()
        self.ctimer.singleShot(0, self.killButton)
        slicer.mrmlScene.Clear(0)
        self.cargarScene()

    def onExit(self, goingTo, transitionType):
        super(MenuProfesor, self).onExit(goingTo, transitionType)
    
    def validate(self, desiredBranchId):
        validationSuceeded = True
        super(MenuProfesor, self).validate(validationSuceeded, desiredBranchId)
        
    def killButton(self):
    	bl = slicer.util.findChildren(text='ModuloPlaneacion' )
        b2 = slicer.util.findChildren(text='IngresoAlumno' )
        b3 = slicer.util.findChildren(text='MenuProfesor')
        bl[0].hide()
        b2[0].hide()
        b3[0].hide()

    def cargarScene(self):
        self.layoutManager = slicer.app.layoutManager() 
        self.layoutManager.setLayout(3)
