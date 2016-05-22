# -*- coding: UTF-8 -*-
from __main__ import vtk, qt, ctk, slicer
from os import listdir
from os.path import isfile, join

class ModuloPlaneacion(ctk.ctkWorkflowWidgetStep) :

  def __init__(self, stepid):
    self.initialize(stepid)
    self.setName( '3. Modulo Planeacion Insercion TTP'  )
    self.__parent = super( ModuloPlaneacion, self )
        
  def createUserInterface(self):

		self.__layout = qt.QFormLayout( self )
    
		font=qt.QFont("Sans Serif",10, qt.QFont.Bold)

#Definicion botenes colapsables:
#--------------------------------------------------------------------------------------------------
		self.botonColapsableInstrucciones = ctk.ctkCollapsibleButton()
		self.botonColapsableInstrucciones.text = "Instrucciones de uso"
		self.__layout.addRow(self.botonColapsableInstrucciones)

		self.botonColapsableUbicacionTornillos = ctk.ctkCollapsibleButton()
		self.botonColapsableUbicacionTornillos.text = "Ubicacion de tornillos"
		self.__layout.addRow(self.botonColapsableUbicacionTornillos)

		self.botonColapsableManipulacionTornillos = ctk.ctkCollapsibleButton()
		self.botonColapsableManipulacionTornillos.text = "Manipulacion de tornillos"
		self.__layout.addRow(self.botonColapsableManipulacionTornillos)

#Interfaz grafica de cada boton colapsable
#--------------------------------------------------------------------------------------------------

#Instrucciones de uso:
		self.instruccionesDeUsoLayout=qt.QFormLayout(self.botonColapsableInstrucciones)
		self.instruccionesdeUsoFrame=qt.QFrame()
		self.instruccionesdeUsoFrame.setFrameShadow(1)
		self.instruccionesdeUsoFrame.setGeometry(0,0,7,6)
		self.instruccionesdeUsoFrameLayout=qt.QFormLayout()
		self.labelInstruccionesDeUsoBienvenido = qt.QLabel("Bienvenido al modulo de planeacion")
		self.labelInstruccionesDeUsoBienvenido.setFont(font)
		self.labelInstruccionesDeUsoInstruccion = qt.QLabel("1. Ubique el primer punto de insercion")
		self.labelInstruccionesDeUsoInstruccion.setFont(font)
		self.instruccionesdeUsoFrameLayout.addWidget(self.labelInstruccionesDeUsoBienvenido)
		self.instruccionesdeUsoFrameLayout.addWidget(self.labelInstruccionesDeUsoInstruccion)

		self.instruccionesdeUsoFrame.setLayout(self.instruccionesdeUsoFrameLayout)  
		self.instruccionesDeUsoLayout.addRow(self.instruccionesdeUsoFrame)

#Ubicacion de los tornillos:
		self.ubicacionDeTornillosLayout=qt.QFormLayout(self.botonColapsableUbicacionTornillos)
		self.seleccionTornillo1ComboBox = qt.QComboBox()
		self.pathTornillos="C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Modelos\Tornillos"
		self.onlyfiles = [f for f in listdir(self.pathTornillos) if isfile(join(self.pathTornillos, f))] #Lista los archivos que estan dentro del path
		for tornillo in self.onlyfiles: #Muestra en el comboBox de cursos los archivos que estan presentes en el path
			self.seleccionTornillo1ComboBox.addItem(tornillo)
		self.ubicacionDeTornillosLayout.addRow(self.seleccionTornillo1ComboBox)



  def onEntry(self, comingFrom, transitionType):
    super(ModuloPlaneacion, self).onEntry(comingFrom, transitionType)
    self.ctimer = qt.QTimer()
    self.ctimer.singleShot(0, self.killButton)
    self.cargarScene()


  def onExit(self, goingTo, transitionType):
    super(ModuloPlaneacion, self).onExit(goingTo, transitionType)
        
  def validate(self, desiredBranchId):
    validationSuceeded = True
    super(ModuloPlaneacion, self).validate(validationSuceeded, desiredBranchId)
        
  def killButton(self):
    bl = slicer.util.findChildren(text='ModuloPlaneacion' )
    bl[0].hide()

  def cargarScene(self):
    path1='C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Modelos/stlcolumna.stl' #Se obtiene direccion de la unbicación del tornillo
    path2='C:\Users\Camilo_Q\Documents\GitHub\simuladorTornillosPediculares\simuladorTornillosPedicularesWizard\Modelos\Lumbar 2.5 B31s - 4/4 Lumbar  2.5  B31s.nrrd'
    slicer.util.loadModel(path1)
    slicer.util.loadVolume(path2)

    columna=slicer.util.getNode('stlcolumna') # Se obtiene el nodo del objeto en escena
    columnaModelDisplayNode = columna.GetDisplayNode() 
    columnaModelDisplayNode.SetColor(0.9451,0.8392,0.5686) #Colores parametrizados sobre 255
    columnaModelDisplayNode.SetSliceIntersectionVisibility(1)
    layoutManager = slicer.app.layoutManager() 
    threeDWidget = layoutManager.threeDWidget(0)
    self.threeDView = threeDWidget.threeDView()
    self.threeDView.resetFocalPoint()
#Ubiar la camara en la parte posterior
    cameraNode=slicer.util.getNode('*Camera*') 
    camera=cameraNode.GetCamera() 
    camera.SetPosition(-5.92673, -98.1958, -1116.53)
    camera.SetViewUp(-0.00203823, -0.0605367, 0.998164)
    camera.SetFocalPoint(19, 91, -1105)
    camera.SetViewAngle(30) 
    cameraNode.ResetClippingRange() 
    self.threeDView.setDisabled(True)

