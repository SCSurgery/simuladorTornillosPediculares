# -*- coding: UTF-8 -*-
from __main__ import qt, ctk, slicer
import mysql.connector
import sys
import os


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

        moduleName = 'simuladorTornillosPediculares'
        scriptedModulesPath = eval('slicer.modules.%s.path' % moduleName.lower())# devuelve la ruta del .py
        scriptedModulesPath = os.path.dirname(scriptedModulesPath)# lleva a la carpeta del modulo
   
        path = os.path.join(scriptedModulesPath,'Interfaz Grafica', '%s.ui' %self.stepid)
        loader = qt.QUiLoader()
        #path1='C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\Interfaz Grafica\Inicio.ui'
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

        self.nombreEditText.textChanged.connect(self.textchanged1)
        self.contrasenaEditText.textChanged.connect(self.textchanged2)

    def onEntry(self, comingFrom, transitionType):

        moduloName = 'simuladorTornillosPediculares'

        slicer.mrmlScene.Clear(0)
        super(Inicio, self).onEntry(comingFrom, transitionType)
        self.ctimer = qt.QTimer()
        self.ctimer.singleShot(0, self.killButton)

    def onExit(self, goingTo, transitionType):
        super(Inicio, self).onExit(goingTo, transitionType)
         
    def validate(self, desiredBranchId):
        con=mysql.connector.connect(user="root",password="root",host="127.0.0.1",database="basedatos_simulador_ttp")
        cursor=con.cursor()
        sys.argv=["indice","Nombre","Contrasena"]
        if self.profesorCheckBox.isChecked():
            desiredBranchId = '2'
            ingreso=0;
            profesores = []
            cursor.execute("SELECT * FROM profesores")
            rows = cursor.fetchall()
            for row in rows:
                profesores.append(row)
            for i in range (0,len(profesores)):
                if (self.name == profesores[i][1] and self.contra == str(profesores[i][2])):
                    desiredBranchId = '3'
                    super(Inicio, self).validate(True, desiredBranchId)
                    ingreso=1
            if ingreso==0:
                qt.QMessageBox.warning(slicer.util.mainWindow(),'Error Login', u'Usuario y/o contraseña invalidos')
                super(Inicio, self).validate(False, desiredBranchId)
        elif self.estudianteCheckBox.isChecked():
            ingreso=0;
            estudiantes = []
            cursor.execute("SELECT * FROM estudiantes")
            rows = cursor.fetchall()
            for row in rows:
                estudiantes.append(row)
            for i in range (0,len(estudiantes)):
                if (self.name == estudiantes[i][1] and self.contra == str(estudiantes[i][2])):
                    desiredBranchId = '2'
                    super(Inicio, self).validate(True, desiredBranchId)
                    ingreso=1
                    sys.argv[0]=str(estudiantes[i][0])
                    sys.argv[1]=self.name
                    sys.argv[2]=str(estudiantes[i][2])
                    print sys.argv[0]
            if ingreso==0:
                qt.QMessageBox.warning(slicer.util.mainWindow(),'Error Login', u'Usuario y/o contraseña invalidos')
                super(Inicio, self).validate(False, desiredBranchId)
        elif self.eresNuevoCheckBox.isChecked():
            desiredBranchId = '1'
            super(Inicio, self).validate(True, desiredBranchId)

    def killButton(self):
    	
        b2 = slicer.util.findChildren(text='IngresoAlumno' )
        b3 = slicer.util.findChildren(text='MenuProfesor')
        b4 = slicer.util.findChildren(text='SimulatorTTPCalibration')
        
        b2[0].hide()
        b3[0].hide()
        b4[0].hide()

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

    def textchanged1(self,text):
        self.name = str(text)
        
    def textchanged2(self,text):
        self.contra = str(text)
