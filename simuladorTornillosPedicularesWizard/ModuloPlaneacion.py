# -*- coding: UTF-8 -*-
from __main__ import vtk, qt, ctk, slicer
from os import listdir
from os.path import isfile, join
import numpy,math
import sys
import mysql.connector

class ModuloPlaneacion(ctk.ctkWorkflowWidgetStep) :

  def __init__(self, stepid):
    self.initialize(stepid)
    self.setName( u'4. Modulo Planeación Insercion TTP'  )
    self.__parent = super( ModuloPlaneacion, self )
    self.nextButtonText = 'Siguiente'
    self.backButtonText = 'Volver'
        
  def createUserInterface(self):

        self.__layout = qt.QFormLayout( self )
        font=qt.QFont("Sans Serif",10, qt.QFont.Bold)

#Definicion botenes colapsables:
#--------------------------------------------------------------------------------------------------
        self.botonColapsableInstrucciones = ctk.ctkCollapsibleButton()
        self.botonColapsableInstrucciones.text = "Instrucciones de uso"
        self.__layout.addRow(self.botonColapsableInstrucciones)

        self.botonColapsableUbicacionTornillos = ctk.ctkCollapsibleButton()
        self.botonColapsableUbicacionTornillos.text = u"Ubicación de tornillos"
        self.__layout.addRow(self.botonColapsableUbicacionTornillos)

        self.botonColapsableManipulacionTornillos = ctk.ctkCollapsibleButton()
        self.botonColapsableManipulacionTornillos.text = u"Manipulación de tornillos"
        self.__layout.addRow(self.botonColapsableManipulacionTornillos)

#Interfaz grafica de cada boton colapsable
#--------------------------------------------------------------------------------------------------
#Instrucciones de uso:
        self.instruccionesDeUsoLayout=qt.QFormLayout(self.botonColapsableInstrucciones)
        self.instruccionesdeUsoFrame=qt.QFrame()
        self.instruccionesdeUsoFrame.setFrameShadow(1)
        self.instruccionesdeUsoFrame.setGeometry(0,0,7,6)
        self.instruccionesdeUsoFrameLayout=qt.QFormLayout()
        self.labelInstruccionesDeUsoBienvenido = qt.QLabel(u"Bienvenido al modulo de planeación")
        self.labelInstruccionesDeUsoBienvenido.setFont(font)
        self.labelInstruccionesDeUsoInstruccion = qt.QLabel(u"1. Ubique el primer punto de inserción")
        self.labelInstruccionesDeUsoInstruccion.setFont(font)
        self.instruccionesdeUsoFrameLayout.addWidget(self.labelInstruccionesDeUsoBienvenido)
        self.instruccionesdeUsoFrameLayout.addWidget(self.labelInstruccionesDeUsoInstruccion)

        self.instruccionesdeUsoFrame.setLayout(self.instruccionesdeUsoFrameLayout)  
        self.instruccionesDeUsoLayout.addRow(self.instruccionesdeUsoFrame)
        self.reiniciarButton = qt.QPushButton("Reiniciar Todo")
        self.reiniciarButton.connect('clicked(bool)',self.onApplyReniciarTodo)

        self.instruccionesdeUsoFrameLayout.addWidget(self.reiniciarButton)

#Ubicacion de los tornillos:
        self.ubicacionDeTornillosLayout=qt.QFormLayout(self.botonColapsableUbicacionTornillos)
        self.ubicacionDeTornillosLayoutContenedorTornillo1=qt.QFrame()
        self.ubicacionDeTornillosLayoutContenedorTornillo2=qt.QFrame()
        self.ubicacionDeTornillosLayoutContenedorTornillo1.setLayout(qt.QHBoxLayout())
        self.ubicacionDeTornillosLayoutContenedorTornillo2.setLayout(qt.QHBoxLayout())

        self.reglaButton = qt.QPushButton("Regla")
        self.reglaButton.toolTip= u"Al presionar este boton ubicara en la vista 3d el punto de inseción"
        self.reglaButton.connect('clicked(bool)',self.onApplyRegla)
        self.ubicacionDeTornillosLayout.addRow(self.reglaButton)

        self.insercion1Button = qt.QPushButton()
        self.insercion1Button.toolTip= u"Al presionar este boton ubicara en la vista 3d el punto de inseción"
        self.insercion1Button.setIcon(qt.QIcon('C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Icons\Fiducials.png'))
        self.insercion1Button.setMaximumWidth(30)
        self.insercion1Button.connect('clicked(bool)',self.onApplyIncercion1)

        self.anadirTornillo1Button = qt.QPushButton("")
        self.anadirTornillo1Button.toolTip= u"Al presionar este boton cargará el tornillo al espacio 3D"
        self.anadirTornillo1Button.setIcon(qt.QIcon('C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Icons\mas.png'))
        self.anadirTornillo1Button.setMaximumWidth(30)
        self.anadirTornillo1Button.connect('clicked(bool)',self.onApplyAnadirTornillo1)

        self.eliminarTornillo1Button = qt.QPushButton("")
        self.eliminarTornillo1Button.toolTip= u"Al presionar este boton eliminará el tornillo al espacio 3D"
        self.eliminarTornillo1Button.setIcon(qt.QIcon('C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Icons\minus.png'))
        self.eliminarTornillo1Button.setMaximumWidth(30)
        self.eliminarTornillo1Button.connect('clicked(bool)',self.onApplyEliminarTornillo1)

        self.seleccionTornillo1ComboBox = qt.QComboBox()
        self.seleccionTornillo1ComboBox.currentIndexChanged.connect(self.seleccionTornillo1ComboBoxMoved)
        #self.seleccionTornillo1ComboBox.addItem("")
        self.pathTornillos="C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Modelos\Tornillos"
        self.onlyfiles = [f for f in listdir(self.pathTornillos) if isfile(join(self.pathTornillos, f))] #Lista los archivos que estan dentro del path
        for tornillo in self.onlyfiles: #Muestra en el comboBox de cursos los archivos que estan presentes en el path
            self.seleccionTornillo1ComboBox.addItem(tornillo)

        self.ubicacionDeTornillosLayoutContenedorTornillo1.layout().addWidget(self.insercion1Button)
        self.ubicacionDeTornillosLayoutContenedorTornillo1.layout().addWidget(self.seleccionTornillo1ComboBox)
        self.ubicacionDeTornillosLayoutContenedorTornillo1.layout().addWidget(self.anadirTornillo1Button)
        self.ubicacionDeTornillosLayoutContenedorTornillo1.layout().addWidget(self.eliminarTornillo1Button)

        self.insercion2Button = qt.QPushButton("")
        self.insercion2Button.toolTip= u"Al presionar este boton ubicará en la vista 3d el punto de insecion"
        self.insercion2Button.setIcon(qt.QIcon('C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Icons\Fiducials.png'))
        self.insercion2Button.setMaximumWidth(30)
        self.insercion2Button.connect('clicked(bool)',self.onApplyIncercion2)

        self.anadirTornillo2Button = qt.QPushButton("")
        self.anadirTornillo2Button.toolTip= u"Al presionar este boton cargará el tornillo al espacio 3D"
        self.anadirTornillo2Button.setIcon(qt.QIcon('C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Icons\mas.png'))
        self.anadirTornillo2Button.setMaximumWidth(30)
        self.anadirTornillo2Button.connect('clicked(bool)',self.onApplyAnadirTornillo2)

        self.eliminarTornillo2Button = qt.QPushButton("")
        self.eliminarTornillo2Button.toolTip= u"Al presionar este boton eliminará el tornillo al espacio 3D"
        self.eliminarTornillo2Button.setIcon(qt.QIcon('C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Icons\minus.png'))
        self.eliminarTornillo2Button.setMaximumWidth(30)
        self.eliminarTornillo2Button.connect('clicked(bool)',self.onApplyEliminarTornillo2)

        self.seleccionTornillo2ComboBox = qt.QComboBox()
        self.seleccionTornillo2ComboBox.currentIndexChanged.connect(self.seleccionTornillo2ComboBoxMoved)
        
        #self.seleccionTornillo2ComboBox.addItem("")
        self.pathTornillos="C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Modelos\Tornillos"
        self.onlyfiles = [f for f in listdir(self.pathTornillos) if isfile(join(self.pathTornillos, f))] #Lista los archivos que estan dentro del path
        for tornillo in self.onlyfiles: #Muestra en el comboBox de cursos los archivos que estan presentes en el path
            self.seleccionTornillo2ComboBox.addItem(tornillo)

        self.ubicacionDeTornillosLayoutContenedorTornillo2.layout().addWidget(self.insercion2Button)
        self.ubicacionDeTornillosLayoutContenedorTornillo2.layout().addWidget(self.seleccionTornillo2ComboBox)
        self.ubicacionDeTornillosLayoutContenedorTornillo2.layout().addWidget(self.anadirTornillo2Button)
        self.ubicacionDeTornillosLayoutContenedorTornillo2.layout().addWidget(self.eliminarTornillo2Button)

        self.ubicacionDeTornillosLayout.addRow(self.ubicacionDeTornillosLayoutContenedorTornillo1)
        self.ubicacionDeTornillosLayout.addRow(self.ubicacionDeTornillosLayoutContenedorTornillo2)

#Manipulacion de los tornillos

        self.manipulacionTornillosLayout=qt.QFormLayout(self.botonColapsableManipulacionTornillos)
        self.manipulacionTornillosLayoutContenedor=qt.QFrame()
        self.manipulacionTornillosLayoutContenedor.setLayout(qt.QHBoxLayout())


        self.comboBoxSeleccionTornillo = qt.QComboBox() #Se crea comboBox para seleccionar tornillo
        self.comboBoxSeleccionTornillo.addItem("Tornillo 1") #Se añade opciones
        self.comboBoxSeleccionTornillo.addItem("Tornillo 2")
        self.comboBoxSeleccionTornillo.currentIndexChanged.connect(self.onMoveComboBox)

        self.barraTranslacionEjeTornillo = qt.QSlider(1) #Se crea un slicer 
        self.barraTranslacionEjeTornillo.setMinimum(0) #Minimo del slider -200
        self.barraTranslacionEjeTornillo.setMaximum(150) #Maximo de slider 200
        self.barraTranslacionEjeTornillo.setPageStep(1) # Al dar clic sobre la barra solo avanza 1 paso
        self.barraTranslacionEjeTornillo.valueChanged.connect(self.onMoveTraslacionEjeTornillo)
        #self.barraTranslacionEjeTornillo.setMaximumWidth(130)
        self.planoTornillo1= qt.QPushButton()
        self.planoTornillo1.setIcon(qt.QIcon('C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Icons\eyeclose.png'))
        self.planoTornillo1.setMaximumWidth(30)
        self.planoTornillo1.connect('clicked(bool)',self.onApplyplanoTornillo1)

        self.manipulacionTornillosLayoutContenedor.layout().addWidget(self.barraTranslacionEjeTornillo)
        self.manipulacionTornillosLayoutContenedor.layout().addWidget(self.planoTornillo1)

        self.manipulacionTornillosLayout.addRow(self.comboBoxSeleccionTornillo)
        self.manipulacionTornillosLayout.addRow(self.manipulacionTornillosLayoutContenedor)
        self.fijarTornillos= qt.QPushButton('Fijar Tornillos')
        self.fijarTornillos.connect('clicked(bool)',self.onApplyFijarTornillos)
        self.manipulacionTornillosLayout.addRow(self.fijarTornillos)

        self.botonGuardar= qt.QPushButton('Guardar')
        self.botonGuardar.connect('clicked(bool)',self.onApplyGuargar)
        self.manipulacionTornillosLayout.addRow(self.botonGuardar)

        self.copiar3D()

  def onEntry(self, comingFrom, transitionType):
    super(ModuloPlaneacion, self).onEntry(comingFrom, transitionType)
    slicer.mrmlScene.Clear(0)

    self.ctimer = qt.QTimer()
    self.ctimer.singleShot(0, self.killButton)
    self.cargarScene()
    self.iniciarFiducials()
    self.clicplanotornillo=0
    self.insercion2Button.setEnabled(False)
    self.anadirTornillo1Button.setEnabled(False)
    self.anadirTornillo2Button.setEnabled(False)
    self.eliminarTornillo1Button.setEnabled(False)
    self.eliminarTornillo2Button.setEnabled(False)
    self.botonColapsableManipulacionTornillos.setEnabled(False)
    self.contadorTornillos1=0
    self.contadorTornillos2=0
    self.valorTrasladoSlidex2=0
    self.valorSlideTornillo1=0
    self.valorSlideTornillo2=0
    self.mostrarplano=0
    self.botonGuardar.setEnabled(False)
    
  def onExit(self, goingTo, transitionType):
    super(ModuloPlaneacion, self).onExit(goingTo, transitionType)
        
  def validate(self, desiredBranchId):
    validationSuceeded = True
    super(ModuloPlaneacion, self).validate(validationSuceeded, desiredBranchId)
        
  def killButton(self):
    bl = slicer.util.findChildren(text='ModuloPlaneacion' )
    b2 = slicer.util.findChildren(text='IngresoAlumno' )
    bl[0].hide()
    b2[0].hide()

  def cargarScene(self):

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
#Ubiar la camara en la parte posterior
    cameraNode=slicer.util.getNode('*Camera*') 
    camera=cameraNode.GetCamera() 
    camera.SetPosition(-5.92673, -98.1958, -1116.53)
    camera.SetViewUp(-0.00203823, -0.0605367, 0.998164)
    camera.SetFocalPoint(19, 91, -1105)
    camera.SetViewAngle(30) 
    cameraNode.ResetClippingRange() 
    slicer.util.resetSliceViews()
    
    self.threeDView.setDisabled(True)
    sliceNode = slicer.util.getNode('vtkMRMLSliceNodeRed')
    sliceNode.SetOrientationToReformat()
    mtslide = vtk.vtkMatrix4x4()
    mtslide.SetElement(0,0,0.550523)
    mtslide.SetElement(0,1,0)
    mtslide.SetElement(0,2,0)
    mtslide.SetElement(0,3,-82.5784)
    mtslide.SetElement(1,0,0)
    mtslide.SetElement(1,1,0.550523)
    mtslide.SetElement(1,2,0)
    mtslide.SetElement(0,3,-79)
    mtslide.SetElement(2,0,0)
    mtslide.SetElement(2,1,0)
    mtslide.SetElement(2,2,1.4002)
    mtslide.SetElement(0,3,0)

    sliceNode.SetSliceToRAS(mtslide)

    self.layoutManager= slicer.app.layoutManager()
    gw = self.layoutManager.sliceWidget('Red')
    gNode = gw.sliceLogic()
    gNode.FitSliceToAll() 


  def iniciarFiducials(self):
        self.referenciasTornillo1=slicer.vtkMRMLMarkupsFiducialNode()
        self.referenciasTornillo1.SetName("Fiducials Tornillo 1")
        self.referenciasTornillo2=slicer.vtkMRMLMarkupsFiducialNode()
        self.referenciasTornillo2.SetName("Fiducials Tornillo 2")
        slicer.mrmlScene.AddNode(self.referenciasTornillo2)
        slicer.mrmlScene.AddNode(self.referenciasTornillo1)

  def onApplyReniciarTodo(self):
        try:
            selflicer.mrmlScene.RemoveNode(self.tornillo1)
        except:
            pass
        a=slicer.util.getNode('Transformada Tornillo 1')
        try:
            slicer.mrmlScene.RemoveNode(a)
        except:
            pass
        a=slicer.util.getNode('Transformada Tornillo 2')
        try:
            slicer.mrmlScene.RemoveNode(a)
        except:
            pass
        try:
            slicer.util.getNode('Fiducials Tornillo 1').RemoveAllMarkups()
        except:
            pass
        try:
            slicer.util.getNode('Fiducials Tornillo 2').RemoveAllMarkups()
        except:
            pass
        self.labelInstruccionesDeUsoInstruccion.setText(u"1. Ubique el primer punto de inserción")
        self.insercion1Button.setEnabled(True)
        self.insercion2Button.setEnabled(False)
        self.anadirTornillo1Button.setEnabled(False)
        self.anadirTornillo2Button.setEnabled(False)
        self.eliminarTornillo1Button.setEnabled(False)
        self.eliminarTornillo2Button.setEnabled(False)
        self.botonColapsableManipulacionTornillos.setEnabled(False)
        self.botonGuardar.setEnabled(False)
        self.tornillo1 = None
        self.tornillo2 = None
        self.valorSlideTornillo1=0
        self.valorSlideTornillo2=0
        sliceNode = slicer.util.getNode('vtkMRMLSliceNodeGreen')
        sliceNode.SetSliceVisible(False)
        referencias1.SetLocked(0)
        referencias2.SetLocked(0)

  def onApplyRegla(self):
        
        selectionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSelectionNodeSingleton")
        selectionNode.SetReferenceActivePlaceNodeClassName("vtkMRMLAnnotationRulerNode")
        interactionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
        placeModePersistence = 0
        interactionNode.SetPlaceModePersistence(placeModePersistence)
        interactionNode.SetCurrentInteractionMode(1)

  def onApplyIncercion1(self):
        aml = slicer.modules.markups.logic()
        F=slicer.util.getNode("Fiducials Tornillo 1")
        aml.SetActiveListID(F)
        placeModePersistence = 0
        slicer.modules.markups.logic().StartPlaceMode(placeModePersistence)
        self.labelInstruccionesDeUsoInstruccion.setText("2. Seleccione el tornillo #1 y carguelo")
        self.threeDView.setDisabled(False)
        self.anadirTornillo1Button.setEnabled(True)
        self.insercion1Button.setEnabled(False)

  def onApplyIncercion2(self):
        aml = slicer.modules.markups.logic()
        F=slicer.util.getNode("Fiducials Tornillo 2")
        aml.SetActiveListID(F)
        placeModePersistence = 0
        slicer.modules.markups.logic().StartPlaceMode(placeModePersistence)
        self.insercion2Button.setEnabled(False)
        self.eliminarTornillo2Button.setEnabled(True)
        self.anadirTornillo2Button.setEnabled(True)
        self.labelInstruccionesDeUsoInstruccion.setText("4. Seleccione el tornillo #2 y carguelo")

  def onApplyplanoTornillo1(self):

        sliceNode = slicer.util.getNode('vtkMRMLSliceNodeGreen')
        if self.clicplanotornillo==0:
            self.planoTornillo1.setIcon(qt.QIcon('C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Icons\eyeopen.png'))
            self.clicplanotornillo=1
            sliceNode.SetOrientationToReformat()
            sliceNode.SetSliceVisible(True)
            self.mostrarplano=1
            
            if self.comboBoxSeleccionTornillo.currentIndex == 0:
                self.SetSliceOrigin(sliceNode,self.targetTornillo1)
                self.SetSliceNormal(sliceNode,self.normalTornillo1)
                
            else:
                self.SetSliceOrigin(sliceNode,self.targetTornillo2)
                self.SetSliceNormal(sliceNode,self.normalTornillo2)

        else:
            self.clicplanotornillo=0
            self.planoTornillo1.setIcon(qt.QIcon('C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Icons\eyeclose.png'))
            sliceNode.SetSliceVisible(False)
            self.mostrarplano=0
            sliceNode.SetOrientationToCoronal()

  def onApplyAnadirTornillo1(self):
 
        self.insercion2Button.setEnabled(True)
        self.anadirTornillo1Button.setEnabled(False)
        self.eliminarTornillo1Button.setEnabled(True)
        self.labelInstruccionesDeUsoInstruccion.setText(u"3. Ubique el segundo punto de inserción")
        self.pathTornillos = 'C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Modelos\Tornillos/'+self.nombreTornillo1+".STL"
        slicer.util.loadModel(self.pathTornillos)
        referencias=slicer.util.getNode('Fiducials Tornillo 1')
        referencias.SetNthMarkupLabel(0,"target 1")
        posicionFiducial1 = [0,0,0]
        referencias.GetNthFiducialPosition(0,posicionFiducial1)

        for i in range(0,20):

            if self.contadorTornillos1==1: self.tornillo1 =slicer.util.getNode(str(self.nombreTornillo1)+"_"+str(i))
                
            if self.contadorTornillos1==0:
                self.tornillo1 =slicer.util.getNode(str(self.nombreTornillo1))
                self.contadorTornillos1=1

            if self.tornillo1 != None:
                self.contadorTornillos1=0
                self.tornillo1.SetName("Tornillo_1")
                break
        # Se relaciona la trnasformada con el objeto tornillo
        self.transformadaTornillo1=slicer.vtkMRMLLinearTransformNode() #Se crea una transformada lineal
        self.transformadaTornillo1.SetName('Transformada Tornillo 1') #Se asigna nombre a la transformada
        slicer.mrmlScene.AddNode(self.transformadaTornillo1) #
        self.tornillo1.SetAndObserveTransformNodeID(self.transformadaTornillo1.GetID())
        tornilloModelDisplayNode = self.tornillo1.GetDisplayNode() 
        tornilloModelDisplayNode.SetColor(0.847059,0.847059,0.847059)
        tornilloModelDisplayNode.SetAmbient(0.10)
        tornilloModelDisplayNode.SetDiffuse(0.6)
        tornilloModelDisplayNode.SetSpecular(1)
        tornilloModelDisplayNode.SetPower(40)
        tornilloModelDisplayNode.SetSliceIntersectionVisibility(1)
        
        self.matriztornillo1 = vtk.vtkMatrix4x4() #Se crea matriz 4x4 para el tornillo 2
        self.transformadaTornillo1.GetMatrixTransformToParent(self.matriztornillo1) # a la matriz de tornillo 2 se toma como padre la matriz de movimiento
        self.matriztornillo1.SetElement(0,3,posicionFiducial1[0]) #Se modifica la matriz del tornillo
        self.matriztornillo1.SetElement(1,3,posicionFiducial1[1])
        self.matriztornillo1.SetElement(2,3,posicionFiducial1[2])
        self.transformadaTornillo1.SetAndObserveMatrixTransformToParent(self.matriztornillo1) # Se añade la matriz del tornillo modificada a la matriz padre de movimientos

        referencias.AddFiducial(posicionFiducial1[0],posicionFiducial1[1]-70,posicionFiducial1[2]) #Se agrega nuevo fiducial en direccion a la longitud del tornillo
        referencias.SetNthMarkupLabel(1,"access 1")
        referencias.AddObserver(referencias.PointModifiedEvent,self.onReferenciasMov)   

  def onApplyAnadirTornillo2(self):

        self.anadirTornillo2Button.setEnabled(False)
        self.botonColapsableManipulacionTornillos.setEnabled(True)
        self.labelInstruccionesDeUsoInstruccion.setText("5. Manipule el tornillo #1 e insertelo")

        self.pathTornillos = 'C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Modelos\Tornillos/'+self.nombreTornillo2+".STL"
        slicer.util.loadModel(self.pathTornillos)

        referencias=slicer.util.getNode('Fiducials Tornillo 2')
        referencias.SetNthMarkupLabel(0,"Target 2")
        posicionFiducial2 = [0,0,0]
        referencias.GetNthFiducialPosition(0,posicionFiducial2)
        referencias.SetLocked(1)

        for i in range(0,20):

            if self.contadorTornillos2==1:
                self.tornillo2 =slicer.util.getNode(str(self.nombreTornillo2)+"_"+str(i))

            if self.contadorTornillos2==0:
                self.tornillo2 =slicer.util.getNode(str(self.nombreTornillo2))
                self.contadorTornillos2=1

            if self.tornillo2 != None:
                self.contadorTornillos2=0
                self.tornillo2.SetName("Tornillo_2")
                break
        self.nombreTornillo2

        self.transformadaTornillo2=slicer.vtkMRMLLinearTransformNode() #Se crea una transformada lineal
        self.transformadaTornillo2.SetName('Transformada Tornillo 2') #Se asigna nombre a la transformada
        slicer.mrmlScene.AddNode(self.transformadaTornillo2) #
        self.tornillo2.SetAndObserveTransformNodeID(self.transformadaTornillo2.GetID()) # Se relaciona la trnasformada con el objeto tornillo
          
        self.matriztornillo2 = vtk.vtkMatrix4x4() #Se crea matriz 4x4 para el tornillo 2
        self.transformadaTornillo2.GetMatrixTransformToParent(self.matriztornillo2) # a la matriz de tornillo 2 se toma como padre la matriz de movimiento
        self.matriztornillo2.SetElement(0,3,posicionFiducial2[0]) #Se modifica la matriz del tornillo
        self.matriztornillo2.SetElement(1,3,posicionFiducial2[1])
        self.matriztornillo2.SetElement(2,3,posicionFiducial2[2])
        self.transformadaTornillo2.SetAndObserveMatrixTransformToParent(self.matriztornillo2) # Se añade la matriz del tornillo modificada a la matriz padre de movimientos

        referencias.AddFiducial(posicionFiducial2[0],posicionFiducial2[1]-70,posicionFiducial2[2]) #Se agrega nuevo fiducial en direccion a la longitud del tornillo
        referencias.SetNthMarkupLabel(1,"access 2")
        referencias.AddObserver(referencias.PointModifiedEvent,self.onReferenciasMov2)
       
        tornillo2ModelDisplayNode = self.tornillo2.GetDisplayNode() 
        tornillo2ModelDisplayNode.SetSliceIntersectionVisibility(1)
        tornillo2ModelDisplayNode.SetColor(0.847059,0.847059,0.847059)
        tornillo2ModelDisplayNode.SetAmbient(0.10)
        tornillo2ModelDisplayNode.SetDiffuse(0.6)
        tornillo2ModelDisplayNode.SetSpecular(1)
        tornillo2ModelDisplayNode.SetPower(40)

  def onApplyEliminarTornillo1(self):

        slicer.mrmlScene.RemoveNode(self.tornillo1)
        a=slicer.util.getNode('Transformada Tornillo 1')
        slicer.mrmlScene.RemoveNode(a)
        slicer.util.getNode('Fiducials Tornillo 1').RemoveAllMarkups()
        self.labelInstruccionesDeUsoInstruccion.setText(u"2. Ubique el primer punto de inserción")
        self.insercion1Button.setEnabled(True)
        self.tornillo1 = None
        self.valorSlideTornillo1=0

  def onApplyEliminarTornillo2(self):

        slicer.mrmlScene.RemoveNode(self.tornillo2)
        a=slicer.util.getNode('Transformada Tornillo 2')
        slicer.mrmlScene.RemoveNode(a)
        slicer.util.getNode('Fiducials Tornillo 2').RemoveAllMarkups()
        self.labelInstruccionesDeUsoInstruccion.setText(u"2. Ubique el segundo punto de inserción")
        self.insercion2Button.setEnabled(True)
        self.tornillo2 = None
        self.valorSlideTornillo2=0

  def onApplyFijarTornillos(self):
        referencias1 = slicer.util.getNode("Fiducials Tornillo 1")
        referencias2 = slicer.util.getNode("Fiducials Tornillo 2")
        referencias1.SetLocked(1)
        referencias2.SetLocked(1)
        self.botonColapsableManipulacionTornillos.setEnabled(True)
        self.botonGuardar.setEnabled(True)
        
  def onApplyGuargar(self):
        vectortornillo1=[]
        vectortornillo2=[]
        Tornillo1=self.seleccionTornillo1ComboBox.currentText
        Tornillo2=self.seleccionTornillo2ComboBox.currentText
        transformadaNode=slicer.util.getNode('Transformada Tornillo 1')
        mt = vtk.vtkMatrix4x4() 
        transformadaNode.GetMatrixTransformToParent(mt)
        vectortornillo1=[mt.GetElement(0,0),mt.GetElement(0,1),mt.GetElement(0,2),mt.GetElement(0,3),mt.GetElement(1,0),mt.GetElement(1,1),mt.GetElement(1,2),mt.GetElement(1,3),mt.GetElement(2,0),mt.GetElement(2,1),mt.GetElement(2,2),mt.GetElement(2,3)] 
        print mt
        transformadaNode=slicer.util.getNode('Transformada Tornillo 2')
        mt = vtk.vtkMatrix4x4() 
        transformadaNode.GetMatrixTransformToParent(mt)
        vectortornillo2=[mt.GetElement(0,0),mt.GetElement(0,1),mt.GetElement(0,2),mt.GetElement(0,3),mt.GetElement(1,0),mt.GetElement(1,1),mt.GetElement(1,2),mt.GetElement(1,3),mt.GetElement(2,0),mt.GetElement(2,1),mt.GetElement(2,2),mt.GetElement(2,3)] 
        con=mysql.connector.connect(user="root",password="root",host="127.0.0.1",database="basedatos_simulador_ttp") #Se conecta a la base de datos
        cursor=con.cursor()
        add_produto = """UPDATE `basedatos_simulador_ttp`.`estudiantes` SET `Tornillo_1`='%s', `Tornillo_2`='%s', `Transformada_Tornillo1`='%s', `Transformada_Tornilo2`='%s' WHERE `idEstudiantes`='%s'"""% (Tornillo1,Tornillo2,str(vectortornillo1),str(vectortornillo2),int(sys.argv[0]))
        cursor.execute(add_produto)
        con.commit()
        con.close()

  def setTransformOrigin(self,target,transformadaNode): #Funcion encargada del desplazamiento

    mt = vtk.vtkMatrix4x4() #Se crea nueva matriz para manipular la matriz de rot-des
    transformada=transformadaNode #Se recupera el nodo de la transformada creada
    transformada.GetMatrixTransformToParent(mt) #Se recuperan los datos actuales de la matriz padre de transformada
    mt.SetElement(0,3,target[0]) #Asigno el origen de la matriz en el fiducial target para mover el tornillo y rotar sobre este punto
    mt.SetElement(1,3,target[1])
    mt.SetElement(2,3,target[2])
    transformada.SetAndObserveMatrixTransformToParent(mt) #Se modifica la matriz rot-des de la transformada con los nuevos valores      

  def onReferenciasMov(self,caller,event): #Se crea metodo que es llamado cuando un fiducial es desplazado por el usuario
   
    sliceNode = slicer.util.getNode('vtkMRMLSliceNodeGreen')
    referencias = slicer.util.getNode("Fiducials Tornillo 1") #Recuperamos el nodo de referencia creado
    self.accessT1=numpy.array(numpy.zeros(3)) #Creamos 3 vectores vacios de 3 elemenos
    self.targetTornillo1=numpy.array(numpy.zeros(3))
    self.normalTornillo1=numpy.array(numpy.zeros(3))
    try:
        referencias.GetNthFiducialPosition(0,self.targetTornillo1) #Se obtienen las nuevas posiciones de los fiducial y se almacenan en dos de los vectores
        referencias.GetNthFiducialPosition(1,self.accessT1)
        self.normalTornillo1=self.accessT1-self.targetTornillo1 # Se restan los dos puntos para obtener la direccion entre ellos
        transformadaNode=slicer.util.getNode('Transformada Tornillo 1')
        self.setTransformOrigin(self.targetTornillo1,transformadaNode) #Funcion encargada del desplazamiento
        self.setTransformNormal(self.normalTornillo1,transformadaNode) #Funcion encargada de la rotacion
        if self.mostrarplano==1:
            self.SetSliceOrigin(sliceNode,self.targetTornillo1)
            self.SetSliceNormal(sliceNode,self.normalTornillo1,transformadaNode)
        
    except():
        pass

  def onReferenciasMov2(self,caller,event): #Se crea metodo que es llamado cuando un fiducial es desplazado por el usuario
    
    sliceNode = slicer.util.getNode('vtkMRMLSliceNodeGreen')
    referencias = slicer.util.getNode("Fiducials Tornillo 2") #Recuperamos el nodo de referencia creado
    self.accessT2=numpy.array(numpy.zeros(3)) #Creamos 3 vectores vacios de 3 elemenos
    self.targetTornillo2=numpy.array(numpy.zeros(3))
    self.normalTornillo2=numpy.array(numpy.zeros(3))
    try:
        referencias.GetNthFiducialPosition(0,self.targetTornillo2) #Se obtienen las nuevas posiciones de los fiducial y se almacenan en dos de los vectores
        referencias.GetNthFiducialPosition(1,self.accessT2)
        self.normalTornillo2=self.accessT2-self.targetTornillo2 # Se restan los dos puntos para obtener la direccion entre ellos
        transformadaNode=slicer.util.getNode('Transformada Tornillo 2')
        self.setTransformOrigin(self.targetTornillo2,transformadaNode) #Funcion encargada del desplazamiento
        self.setTransformNormal(self.normalTornillo2,transformadaNode) #Funcion encargada de la rotacion
        if self.mostrarplano==1:
            self.SetSliceOrigin(sliceNode,self.targetTornillo2)
            self.SetSliceNormal(sliceNode,self.normalTornillo2,transformadaNode)

    except():
        pass 

  def setTransformOrigin(self,target,transformadaNode): #Funcion encargada del desplazamiento

    mt = vtk.vtkMatrix4x4() #Se crea nueva matriz para manipular la matriz de rot-des
    transformada=transformadaNode #Se recupera el nodo de la transformada creada
    transformada.GetMatrixTransformToParent(mt) #Se recuperan los datos actuales de la matriz padre de transformada
    mt.SetElement(0,3,target[0]) #Asigno el origen de la matriz en el fiducial target para mover el tornillo y rotar sobre este punto
    mt.SetElement(1,3,target[1])
    mt.SetElement(2,3,target[2])
    transformada.SetAndObserveMatrixTransformToParent(mt) #Se modifica la matriz rot-des de la transformada con los nuevos valores

  def setTransformNormal(self,normal,transformadaNode): #Funcion encargada de la rotacion

    vtk.vtkMath().Normalize(normal) #Se normaliza la direccion del vector entre los dos fiducial
    mt = vtk.vtkMatrix4x4()   #Se crea nueva matriz para manipular la matriz de rot-des
    transformada=transformadaNode  #Se recupera el nodo de la transformada creada
    transformada.GetMatrixTransformToParent(mt) #Se recuperan los datos actuales de la matriz padre de transformada
    cross=numpy.array(numpy.zeros(3)) #Se crea nuevo vector que contrandra el resultado de un producto cruz de 3 elementos
    #
    transform=vtk.vtkTransform() # Se crea nueva transformada 
    #
    nodeNormal=[-mt.GetElement(0,1),-mt.GetElement(1,1),-mt.GetElement(2,1)] #Recuperamos el eje z del tornillo
    self.nodePosicion=[mt.GetElement(0,3),mt.GetElement(1,3),mt.GetElement(2,3)] #Recuperamos la posicion del tornillo
    #
    mt.SetElement(0,3,0) #Asigno el origen de la matriz en el fiducial target para mover el tornillo y rotar sobre este punto
    mt.SetElement(1,3,0) 
    mt.SetElement(2,3,0)
    #
    vtk.vtkMath().Cross(nodeNormal,normal,cross) #Producto cruz entre el eje z y el vector dicector de los dos fiducial para calcular el vector perpendicular
    dot = vtk.vtkMath().Dot(nodeNormal,normal) #Prodducto punto entre el eje z y el vector dicector de los dos fiducial para calcular el angulo
    dot = -1.0 if (dot < -1) else (1.0 if(dot>1.0) else dot) #Operador ternario, limita a que el angulo este entre -1 y 1 ya quese aplica un coseno inverso
    #
    rotacion = vtk.vtkMath().DegreesFromRadians(math.acos(dot)) #Se calcula el angulo entre nodeNormal y normal
    #Aplicar transformada
    transform.PostMultiply() #Rota y translada en el orden correcto,"pre-multiply (or left multiply) A by B" means BA, while "post-multiply (or right multiply) A by C" means AC,Sets the internal state of the transform to PostMultiply. All subsequent operations will occur after those already represented in the current transformation. In homogeneous matrix notation, M = A*M where M is the current transformation matrix and A is the applied matrix. The default is PreMultiply.
    transform.SetMatrix(mt) #Se añade la nueva matriz que esta en el origin de coordenadas
    transform.RotateWXYZ(rotacion,cross) #Create a rotation matrix and concatenate it with the current transformation according to PreMultiply or PostMultiply semantics. The angle is in degrees, and (x,y,z) specifies the axis that the rotation will be performed around.
    transform.GetMatrix(mt) #Se recupera la matriz rotada
    #
    mt.SetElement(0,3,self.nodePosicion[0]) #A la nueva matriz rotada le cambio nuevamente el origen a donde estaba
    mt.SetElement(1,3,self.nodePosicion[1])
    mt.SetElement(2,3,self.nodePosicion[2])
    transformada.SetAndObserveMatrixTransformToParent(mt) # Actulizo la matriz con los cambios realizados

  def seleccionTornillo1ComboBoxMoved(self):
    self.contadorTornillos1=0
    self.nombreTornillo1=str(self.seleccionTornillo1ComboBox.currentText).split('.')
    self.nombreTornillo1=str(self.nombreTornillo1[0])
    print self.nombreTornillo1  

  def seleccionTornillo2ComboBoxMoved(self):
    self.contadorTornillos2=0
    self.nombreTornillo2=str(self.seleccionTornillo2ComboBox.currentText).split('.')
    self.nombreTornillo2=str(self.nombreTornillo2[0])

  def onMoveComboBox(self):

    if self.comboBoxSeleccionTornillo.currentIndex == 0:
        referencias1 = slicer.util.getNode("Fiducials Tornillo 1")
        referencias2 = slicer.util.getNode("Fiducials Tornillo 2")
        self.barraTranslacionEjeTornillo.setValue(self.valorSlideTornillo1)
        referencias1.SetLocked(0)
        referencias2.SetLocked(1)
        self.labelInstruccionesDeUsoInstruccion.setText("5. Manipule el tornillo #1 e insertelo")
    else: 
        referencias2 = slicer.util.getNode("Fiducials Tornillo 2")
        referencias1 = slicer.util.getNode("Fiducials Tornillo 1")
        self.barraTranslacionEjeTornillo.setValue(self.valorSlideTornillo2)
        referencias2.SetLocked(0)
        referencias1.SetLocked(1)
        self.labelInstruccionesDeUsoInstruccion.setText("5. Manipule el tornillo #2 e insertelo")

  def onMoveTraslacionEjeTornillo(self):
    valorTrasladoSlidex =self.barraTranslacionEjeTornillo.value
    access=numpy.array(numpy.zeros(3)) #Creamos 3 vectores vacios de 3 elemenos
    target=numpy.array(numpy.zeros(3))
    normal=numpy.array(numpy.zeros(3))
    movimientoNormal=numpy.array(numpy.zeros(3))
    try:

        if self.comboBoxSeleccionTornillo.currentIndex == 0:
            referencias = slicer.util.getNode("Fiducials Tornillo 1")
            referencias.GetNthFiducialPosition(0,target) #Se obtienen las nuevas posiciones de los fiducial y se almacenan en dos de los vectores
            referencias.GetNthFiducialPosition(1,access)
            normal=access-target # Se restan los dos puntos para obtener la direccion entre ellos
            transformadaNode=slicer.util.getNode('Transformada Tornillo 1')
            self.valorSlideTornillo1=self.barraTranslacionEjeTornillo.value
        else:
            referencias = slicer.util.getNode("Fiducials Tornillo 2")
            referencias.GetNthFiducialPosition(0,target) #Se obtienen las nuevas posiciones de los fiducial y se almacenan en dos de los vectores
            referencias.GetNthFiducialPosition(1,access)
            normal=access-target # Se restan los dos puntos para obtener la direccion entre ellos
            transformadaNode=slicer.util.getNode('Transformada Tornillo 2')
            self.valorSlideTornillo2=self.barraTranslacionEjeTornillo.value

        vtk.vtkMath().Normalize(normal) #Se normaliza la direccion del vector entre los dos fiducial
        mt = vtk.vtkMatrix4x4()   #Se crea nueva matriz para manipular la matriz de rot-des
        transformada=transformadaNode  #Se recupera el nodo de la transformada creada
        transformada.GetMatrixTransformToParent(mt)
        if valorTrasladoSlidex>self.valorTrasladoSlidex2:
            movimientoNormal[0]=target[0]-normal[0]*1
            movimientoNormal[1]=target[1]-normal[1]*1
            movimientoNormal[2]=target[2]-normal[2]*1
        else: 
            movimientoNormal[0]=target[0]+normal[0]*2
            movimientoNormal[1]=target[1]+normal[1]*2
            movimientoNormal[2]=target[2]+normal[2]*2
        mt.SetElement(0,3,movimientoNormal[0]) #Asigno el origen de la matriz en el fiducial target para mover el tornillo y rotar sobre este punto
        mt.SetElement(1,3,movimientoNormal[1])
        mt.SetElement(2,3,movimientoNormal[2])
        transformada.SetAndObserveMatrixTransformToParent(mt)
        if self.comboBoxSeleccionTornillo.currentIndex == 0: referencias.SetNthFiducialPosition(0,movimientoNormal[0],movimientoNormal[1],movimientoNormal[2])
        else: referencias.SetNthFiducialPosition(0,movimientoNormal[0],movimientoNormal[1],movimientoNormal[2])
        self.valorTrasladoSlidex2=valorTrasladoSlidex
                
    except():
        pass

  def SetSliceOrigin(self, sliceNode, origen):

      if (sliceNode == None):
        return

      bounds = self.GetVolumeBounds(sliceNode)
      origen[0] = numpy.max((bounds[0],numpy.min((origen[0],bounds[1]))))
      origen[1] = numpy.max((bounds[2],numpy.min((origen[1],bounds[3]))))
      origen[2] = numpy.max((bounds[4],numpy.min((origen[2],bounds[5]))))

      #Asigna la nueva posicion
      sliceNode.GetSliceToRAS().SetElement(0,3,origen[0])
      sliceNode.GetSliceToRAS().SetElement(1,3,origen[1])
      sliceNode.GetSliceToRAS().SetElement(2,3,origen[2])
      sliceNode.UpdateMatrices()

  def SetSliceNormal(self, sliceNode, normal,transformadaNode):

      if (sliceNode == None):
        return
      mtslide = vtk.vtkMatrix4x4()
      transformada=transformadaNode
      transformada.GetMatrixTransformToParent(mtslide)
      mtslide.SetElement(1,3,self.nodePosicion[0])
      mtslide.SetElement(1,3,self.nodePosicion[1])
      mtslide.SetElement(2,3,self.nodePosicion[2])
      sliceNode.SetSliceToRAS(mtslide)

  def GetVolumeBounds(self, sliceNode):
        """Calcula y retorna el bounding box del volumen"""
        sliceCompositeNode = slicer.vtkMRMLSliceLogic().GetSliceCompositeNode(sliceNode)
        
        if ((sliceNode == None) or (sliceCompositeNode == None)):
            return
        volumeNodeID = 0
        if(not volumeNodeID):
            volumeNodeID = sliceCompositeNode.GetBackgroundVolumeID() if sliceCompositeNode else 0 #operador ternario: valor_si_cierto if condición else valor_si_falso 
        if(not volumeNodeID):
            volumeNodeID = sliceCompositeNode.GetForegroundVolumeID() if sliceCompositeNode else 0
        if(not volumeNodeID):
            volumeNodeID = sliceCompositeNode.GetLabelVolumeID() if sliceCompositeNode else 0
        
        volumeNode = slicer.util.getNode(volumeNodeID)
        
        if (volumeNode):
            dimensions = numpy.array(numpy.zeros(3))
            center = numpy.array(numpy.zeros(3))
            bounds = numpy.array(numpy.zeros(6))
            
            slicer.vtkMRMLSliceLogic().GetVolumeRASBox(volumeNode,dimensions,center)
            bounds[0] = center[0] - dimensions[0] / 2;
            bounds[1] = center[0] + dimensions[0] / 2;
            bounds[2] = center[1] - dimensions[1] / 2;
            bounds[3] = center[1] + dimensions[1] / 2;
            bounds[4] = center[2] - dimensions[2] / 2;
            bounds[5] = center[2] + dimensions[2] / 2;
            
            return bounds
  
  def copiar3D(self):
        qDesktopW = qt.QDesktopWidget()
        t = slicer.qMRMLThreeDView()
        t.setWindowTitle('3D')

        if qDesktopW.screenCount == 2:
            qRect2 = qDesktopW.screenGeometry(1)
            t.setGeometry(qRect2)
            t.show()
            t.setMRMLScene(slicer.mrmlScene)
            t.forceRender()
            n = slicer.util.getNode('*View*')
            t.setMRMLViewNode(n)
        elif qDesktopW.screenCount == 1:
            t.close()
            print "Se desconectó la segunda pantalla"

        #Copiar la vista 3D con opciones de configuracion
        o = slicer.qMRMLThreeDWidget()
        o.setWindowTitle('3D')
        
        o.setMRMLScene(slicer.mrmlScene)
        o.forceRender()
        n = slicer.util.getNode('*View*')
        o.setMRMLViewNode(n)
