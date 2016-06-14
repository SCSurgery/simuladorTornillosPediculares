# -*- coding: UTF-8 -*-
from __main__ import vtk, qt, ctk, slicer


class Inicio(ctk.ctkWorkflowWidgetStep) :

    def __init__(self, stepid):
        self.initialize(stepid)
        self.setName( u'1. Inicio simulador inserción TTP'  )
        self.nextButtonText = 'Siguiente'
        self.backButtonText = 'Volver'
        self.__parent = super( Inicio, self )
        
    def createUserInterface(self):

        font =qt.QFont("Sans Serif", 12, qt.QFont.Bold)
        self.__layout = self.__parent.createUserInterface()
        self.__layout = qt.QFormLayout( self )
        loader = qt.QUiLoader()
        path='C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\Interfaz Grafica\Inicio.ui'
        qfile = qt.QFile(path)
        qfile.open(qt.QFile.ReadOnly)
        widget = loader.load(qfile)
        self.widget = widget
        self.__layout.addWidget(widget)
        self.widget.setMRMLScene(slicer.mrmlScene)
        
        self.nombreEditText = self.findWidget(self.widget,'nombreEditText')
        self.contrasenaEditText = self.findWidget(self.widget,'contrasenaEditText')
        self.profesorCheckBox = self.findWidget(self.widget,'profesorCheckBox')
        self.estudianteCheckBox = self.findWidget(self.widget,'estudianteCheckBox')
        self.eresNuevoCheckBox = self.findWidget(self.widget,'eresNuevoCheckBox')

    def onEntry(self, comingFrom, transitionType):
        super(Inicio, self).onEntry(comingFrom, transitionType)
        self.ctimer = qt.QTimer()
        self.ctimer.singleShot(0, self.killButton)

    def onExit(self, goingTo, transitionType):
        super(Inicio, self).onExit(goingTo, transitionType)
        
    
    def validate(self, desiredBranchId):
        
        if self.profesorCheckBox.isChecked():
            desiredBranchId = '2'
            super(Inicio, self).validate(True, desiredBranchId)
        elif self.estudianteCheckBox.isChecked():
            desiredBranchId = '2'
            super(Inicio, self).validate(True, desiredBranchId)
        elif self.eresNuevoCheckBox.isChecked():
            desiredBranchId = '1'
            super(Inicio, self).validate(True, desiredBranchId)
        
        
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

    
