# -*- coding: UTF-8 -*-
from __main__ import vtk, qt, ctk, slicer

class IngresoAlumno(ctk.ctkWorkflowWidgetStep) :

    def __init__(self, stepid):
        self.initialize(stepid)
        self.setName( '2. Ingreso Alumno'  )
        self.nextButtonText = 'Siguiente'
        self.backButtonText = 'Volver'
        self.__parent = super( IngresoAlumno, self )
        
    def createUserInterface(self):

        font =qt.QFont("Sans Serif", 12, qt.QFont.Bold)
       
        self.__layout = self.__parent.createUserInterface()
        self.__layout = qt.QFormLayout( self )
        loader = qt.QUiLoader()
        path='C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\Interfaz Grafica\Registro.ui'
        qfile = qt.QFile(path)
        qfile.open(qt.QFile.ReadOnly)
        widget = loader.load(qfile)
        self.widget = widget
        self.__layout.addWidget(widget)
        self.widget.setMRMLScene(slicer.mrmlScene)

        self.nombreEditText = self.findWidget(self.widget,'nombreEditText')
        self.contrasenaEditText = self.findWidget(self.widget,'contrasenaEditText')
        self.repetirContrasenaEditText = self.findWidget(self.widget,'repetirContrasenaEditText')
        self.profesorCheckBox = self.findWidget(self.widget,'profesorCheckBox')
        self.estudianteCheckBox = self.findWidget(self.widget,'estudianteCheckBox')
        self.registrarPushButton = self.findWidget(self.widget,'registrarPushButton')
    
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
        b2 = slicer.util.findChildren(text='IngresoAlumno' )
        bl[0].hide()
        b2[0].hide()

    def findWidget(self,widget,objectName):
        if widget.objectName == objectName:
            return widget
        else:
            children = []
            for w in widget.children():
                resulting_widget = self.findWidget(w, objectName)
                if resulting_widget:
                    return resulting_widget
            return None

