# -*- coding: UTF-8 -*-
from __main__ import vtk, qt, ctk, slicer
import os

import simuladorTornillosPedicularesWizard

class simuladorTornillosPediculares:

  def __init__(self, parent):
    parent.title = "Simulador insercion TTP"
    parent.categories = ["Simuladores"]
    parent.dependencies = []
    parent.contributors = ["Camilo Quiceno Quintero ,Nicolas Buitrago Roldan, Jhon Jairo,Juliana Uribe Perez"] # replace with "Firstname Lastname (Org)"
    parent.helpText = """
    Este modulo permite planear y simular la insercion de tornillos transpediculares en la zona lumbar de la columna vertebral 
    """
    parent.acknowledgementText = """
    Grupo de investigacion GIBIC
    """ # replace with organization, grant and thanks.
    self.parent = parent

class simuladorTornillosPedicularesWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):
    #Se establecen los pasos del flujo de trabajo
    self.StepInicio=simuladorTornillosPedicularesWizard.Inicio('Inicio')
    self.StepRegistro=simuladorTornillosPedicularesWizard.IngresoAlumno('IngresoAlumno')
    self.StepHistoriaClinica=simuladorTornillosPedicularesWizard.HistoriaClinica('HistoriaClinica')
    self.StepModuloPlaneacion=simuladorTornillosPedicularesWizard.ModuloPlaneacion('ModuloPlaneacion')
    self.StepMenuProfesor=simuladorTornillosPedicularesWizard.MenuProfesor('MenuProfesor')
    self.StepCalibracion=simuladorTornillosPedicularesWizard.SimulatorTTPCalibration('SimulatorTTPCalibration')

    steps = [] #Se crea tupla que contenga los pasos del flujo de trabajo
    #Se añade a la tupla cada uno de los pasos del flujo de trabajo
    steps.append(self.StepInicio)

    #Se crea el flujo de trabajo
    self.workflow = ctk.ctkWorkflow()
    workflowWidget = ctk.ctkWorkflowStackedWidget()
    workflowWidget.setWorkflow(self.workflow)

    #Se definen las transiciones entre los pasos del flujo de trabajo
    self.workflow.addTransition(self.StepInicio, self.StepRegistro,'1', ctk.ctkWorkflow.Bidirectional )
    self.workflow.addTransition(self.StepInicio, self.StepHistoriaClinica,'2', ctk.ctkWorkflow.Bidirectional )
    self.workflow.addTransition(self.StepInicio, self.StepMenuProfesor,'3', ctk.ctkWorkflow.Bidirectional )
    self.workflow.addTransition(self.StepHistoriaClinica, self.StepModuloPlaneacion)
    self.workflow.addTransition(self.StepModuloPlaneacion,self.StepCalibracion)

    self.workflow.start()
    workflowWidget.visible = True
    self.layout.addWidget( workflowWidget ) 




   