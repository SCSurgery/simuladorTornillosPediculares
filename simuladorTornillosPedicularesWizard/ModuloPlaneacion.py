# -*- coding: UTF-8 -*-
from __main__ import vtk, qt, ctk, slicer

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

  def onEntry(self, comingFrom, transitionType):
    super(ModuloPlaneacion, self).onEntry(comingFrom, transitionType)
    self.ctimer = qt.QTimer()
    self.ctimer.singleShot(0, self.killButton)

  def onExit(self, goingTo, transitionType):
    super(ModuloPlaneacion, self).onExit(goingTo, transitionType)
        
  def validate(self, desiredBranchId):
    validationSuceeded = True
    super(ModuloPlaneacion, self).validate(validationSuceeded, desiredBranchId)
        
  def killButton(self):
    bl = slicer.util.findChildren(text='ModuloPlaneacion' )
    bl[0].hide()

