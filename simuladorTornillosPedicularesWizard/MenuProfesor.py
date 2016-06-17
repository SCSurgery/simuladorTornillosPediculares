# -*- coding: UTF-8 -*-
from __main__ import vtk, qt, ctk, slicer
import mysql.connector

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

        self.seleccionDeEstudianteComboBox = self.findWidget(self.widget,'seleccionDeEstudianteComboBox')
        self.cargarPushButton = self.findWidget(self.widget,'cargarPushButton')

        self.cargarPushButton.connect('clicked(bool)',self.onApplyCargar)

        con=mysql.connector.connect(user="root",password="root",host="127.0.0.1",database="basedatos_simulador_ttp")
        cursor=con.cursor()
        estudiantes = []
        cursor.execute("SELECT * FROM estudiantes")
        rows = cursor.fetchall()
        for row in rows:
            estudiantes.append(row)
        for i in range (0,len(estudiantes)):
            self.seleccionDeEstudianteComboBox.addItem(estudiantes[i][1])

    def onEntry(self, comingFrom, transitionType):
        super(MenuProfesor, self).onEntry(comingFrom, transitionType)
        self.ctimer = qt.QTimer()
        self.ctimer.singleShot(0, self.killButton)
        slicer.mrmlScene.Clear(0)
        self.cargarScene()
        self.contadorTornillos1=0
        self.contadorTornillos2=0
        self.tornillo1=None



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

    def findWidget(self,widget,objectName):
        if widget.objectName == objectName:
            return widget
        else:
            children = []
            for w in widget.children():
                resulting_widget = self.findWidget(w, objectName)
                if resulting_widget:
                    return resulting_widget

    def onApplyCargar(self):
        
        self.nombre=self.seleccionDeEstudianteComboBox.currentText
        con=mysql.connector.connect(user="root",password="root",host="127.0.0.1",database="basedatos_simulador_ttp")
        cursor=con.cursor()
        estudiantes = []
        cursor.execute("SELECT * FROM estudiantes")
        rows = cursor.fetchall()
        for row in rows:
            estudiantes.append(row)
        for i in range (0,len(estudiantes)):
            if (self.nombre == estudiantes[i][1]): 
                self.idEstudiante=estudiantes[i][0]
                self.tornillo_1=str(estudiantes[i][3])
                self.tornillo_2=str(estudiantes[i][4])
                self.tranformadaTornillo1=estudiantes[i][5]
                self.tranformadaTornillo2=estudiantes[i][6]
                break

        nombreTornillo1=self.tornillo_1
        nombreTornillo1=nombreTornillo1.split('.')
        nombreTornillo1= nombreTornillo1[0]

        nombreTornillo2=self.tornillo_2
        nombreTornillo2=nombreTornillo2.split('.')
        nombreTornillo2= nombreTornillo2[0]
    
        x=0
        c=[]
        for i in self.tranformadaTornillo1:
            if (i=='[' or i==']'or i==',' or i=='' or i=="'"):
                pass
            else:
                c.append(self.tranformadaTornillo1[x])
            x=x+1
        d=''.join(c)
        d.split(' ')

        self.tranformadaTornillo1 = [float(x) for x in d.split()]
            
        mt1 = vtk.vtkMatrix4x4()

        mt1.SetElement(0,0,float(self.tranformadaTornillo1[0]))
        mt1.SetElement(0,1,float(self.tranformadaTornillo1[1]))
        mt1.SetElement(0,2,float(self.tranformadaTornillo1[2]))
        mt1.SetElement(0,3,float(self.tranformadaTornillo1[3]))
        mt1.SetElement(1,0,float(self.tranformadaTornillo1[4]))
        mt1.SetElement(1,1,float(self.tranformadaTornillo1[5]))
        mt1.SetElement(1,2,float(self.tranformadaTornillo1[6]))
        mt1.SetElement(1,3,float(self.tranformadaTornillo1[7]))
        mt1.SetElement(2,0,float(self.tranformadaTornillo1[8]))
        mt1.SetElement(2,1,float(self.tranformadaTornillo1[9]))
        mt1.SetElement(2,2,float(self.tranformadaTornillo1[10]))
        mt1.SetElement(2,3,float(self.tranformadaTornillo1[11]))

        mt1.SetElement(3,0,0)
        mt1.SetElement(3,1,0)
        mt1.SetElement(3,2,0)
        mt1.SetElement(3,3,1)
    
        x=0
        c=[]
        for i in self.tranformadaTornillo2:
            if (i=='[' or i==']'or i==',' or i=='' or i=="'"):
                pass
            else:
                c.append(self.tranformadaTornillo2[x])
            x=x+1
        d=''.join(c)
        d.split(' ')

        self.tranformadaTornillo2 = [float(x) for x in d.split()]
            
        mt2 = vtk.vtkMatrix4x4()

        mt2.SetElement(0,0,float(self.tranformadaTornillo2[0]))
        mt2.SetElement(0,1,float(self.tranformadaTornillo2[1]))
        mt2.SetElement(0,2,float(self.tranformadaTornillo2[2]))
        mt2.SetElement(0,3,float(self.tranformadaTornillo2[3]))
        mt2.SetElement(1,0,float(self.tranformadaTornillo2[4]))
        mt2.SetElement(1,1,float(self.tranformadaTornillo2[5]))
        mt2.SetElement(1,2,float(self.tranformadaTornillo2[6]))
        mt2.SetElement(1,3,float(self.tranformadaTornillo2[7]))
        mt2.SetElement(2,0,float(self.tranformadaTornillo2[8]))
        mt2.SetElement(2,1,float(self.tranformadaTornillo2[9]))
        mt2.SetElement(2,2,float(self.tranformadaTornillo2[10]))
        mt2.SetElement(2,3,float(self.tranformadaTornillo2[11]))
        mt2.SetElement(3,0,0)
        mt2.SetElement(3,1,0)
        mt2.SetElement(3,2,0)
        mt2.SetElement(3,3,1)

        path1='C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Modelos/stlcolumna.stl' #Se obtiene direccion de la unbicación del tornillo
        path2='C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Modelos\Lumbar 2.5 B31s - 4/4 Lumbar  2.5  B31s.nrrd'
        path3='C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Modelos/nucleos.stl'
        slicer.util.loadModel(path1)
        slicer.util.loadModel(path3)
        slicer.util.loadVolume(path2)

        columna=slicer.util.getNode('stlcolumna') # Se obtiene el nodo del objeto en escena
        nucleo=slicer.util.getNode('nucleos')
        nucleoModelDisplayNode = nucleo.GetDisplayNode()
        nucleoModelDisplayNode.SetColor(0.729411,0.7529411,0.8745098)
        nucleoModelDisplayNode.SetAmbient(0.10)
        nucleoModelDisplayNode.SetDiffuse(0.90)
        nucleoModelDisplayNode.SetSpecular(0.20)
        nucleoModelDisplayNode.SetPower(10)
        nucleoModelDisplayNode.SetSliceIntersectionVisibility(1)

        columnaModelDisplayNode = columna.GetDisplayNode() 

        columnaModelDisplayNode.SetColor(0.9451,0.8392,0.5686) #Colores parametrizados sobre 255
        columnaModelDisplayNode.SetSliceIntersectionVisibility(1)
        columnaModelDisplayNode.SetAmbient(0.33)
        columnaModelDisplayNode.SetDiffuse(0.78)
        columnaModelDisplayNode.SetSpecular(0.13)
        columnaModelDisplayNode.SetPower(15.5)
        self.layoutManager = slicer.app.layoutManager() 
        threeDWidget = self.layoutManager.threeDWidget(0)
        self.threeDView = threeDWidget.threeDView()
        self.threeDView.resetFocalPoint()
        self.layoutManager.setLayout(1)

        self.pathTornillos = 'C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Modelos\Tornillos/'+self.tornillo_1
        slicer.util.loadModel(self.pathTornillos)

        self.pathTornillos = 'C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Modelos\Tornillos/'+self.tornillo_2
        slicer.util.loadModel(self.pathTornillos)

        for i in range(0,20):

            if self.contadorTornillos1==1: self.tornillo1 =slicer.util.getNode(str(nombreTornillo1)+"_"+str(i))
                
            if self.contadorTornillos1==0:
                self.tornillo1 = slicer.util.getNode(str(nombreTornillo1))
                self.contadorTornillos1=1

            if self.tornillo1 != None:
                self.contadorTornillos1=0
                self.tornillo1.SetName("Tornillo_1")
                break

        for i in range(0,20):

            if self.contadorTornillos2==1: self.tornillo2 =slicer.util.getNode(str(nombreTornillo2)+"_"+str(i))
                
            if self.contadorTornillos2==0:
                self.tornillo2 = slicer.util.getNode(str(nombreTornillo2))
                self.contadorTornillos2=1

            if self.tornillo2 != None:
                self.contadorTornillos2=0
                self.tornillo2.SetName("Tornillo_2")
                break
               
               
        # Se relaciona la trnasformada con el objeto tornillo
       
        tornilloModelDisplayNode = self.tornillo1.GetDisplayNode() 
        tornilloModelDisplayNode.SetColor(0.847059,0.847059,0.847059)
        tornilloModelDisplayNode.SetAmbient(0.10)
        tornilloModelDisplayNode.SetDiffuse(0.6)
        tornilloModelDisplayNode.SetSpecular(1)
        tornilloModelDisplayNode.SetPower(40)
        tornilloModelDisplayNode.SetSliceIntersectionVisibility(1)

        self.transformadaTornillo1=slicer.vtkMRMLLinearTransformNode() #Se crea una transformada lineal
        self.transformadaTornillo1.SetName('Transformada Tornillo 1') #Se asigna nombre a la transformada
        slicer.mrmlScene.AddNode(self.transformadaTornillo1) #
        self.tornillo1.SetAndObserveTransformNodeID(self.transformadaTornillo1.GetID())
        self.transformadaTornillo1.SetAndObserveMatrixTransformToParent(mt1)
               
        # Se relaciona la trnasformada con el objeto tornillo
       
        tornilloModelDisplayNode = self.tornillo2.GetDisplayNode() 
        tornilloModelDisplayNode.SetColor(0.847059,0.847059,0.847059)
        tornilloModelDisplayNode.SetAmbient(0.10)
        tornilloModelDisplayNode.SetDiffuse(0.6)
        tornilloModelDisplayNode.SetSpecular(1)
        tornilloModelDisplayNode.SetPower(40)
        tornilloModelDisplayNode.SetSliceIntersectionVisibility(1)

        self.transformadaTornillo2=slicer.vtkMRMLLinearTransformNode() #Se crea una transformada lineal
        self.transformadaTornillo2.SetName('Transformada Tornillo 2') #Se asigna nombre a la transformada
        slicer.mrmlScene.AddNode(self.transformadaTornillo2) #
        self.tornillo2.SetAndObserveTransformNodeID(self.transformadaTornillo2.GetID())
        self.transformadaTornillo2.SetAndObserveMatrixTransformToParent(mt2)