# -*- coding: UTF-8 -*-
from __main__ import vtk, qt, ctk, slicer
import mysql.connector

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
        self.nombreEditText.textChanged.connect(self.textchanged1)
        self.contrasenaEditText.textChanged.connect(self.textchanged2)
        self.repetirContrasenaEditText.textChanged.connect(self.textchanged3)
        self.registrarPushButton.connect('clicked(bool)',self.onApplyRegistrar)
    
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


    def onApplyRegistrar(self):
        if (self.name != None)and(self.contra!=None):
            if (self.contra == self.contrar):
                con=mysql.connector.connect(user="root",password="root",host="127.0.0.1",database="basedatos_simulador_ttp")
                cursor=con.cursor()
                if(self.estudianteCheckBox.isChecked()):
                    ingreso=0;
                    estudiantes = []
                    cursor.execute("SELECT * FROM estudiantes")
                    rows = cursor.fetchall()
                    for row in rows:
                        estudiantes.append(row)
                    for i in range (0,len(estudiantes)):
                        if (self.name == estudiantes[i][1]): 
                            qt.QMessageBox.warning(slicer.util.mainWindow(),'Error Login', u'Ese nombre de usuario ya se encuentra registrado')   
                            break
                        else:
                            ingreso=1
                    if ingreso==1:
                        if (con!=None):
                            estudianteid=int(len(estudiantes)+1)
                            Nombre=str(self.name)
                            Contrasena=str(self.contra)
                            add_produto = """INSERT INTO estudiantes(idEstudiantes,
                                            Nombre_Estudiante,Contasena_Estudiante)
                                            VALUES ('%s','%s','%s')"""% (estudianteid,Nombre,Contrasena)

                            cursor.execute(add_produto)
                            con.commit()
                            con.close()
                            qt.QMessageBox.warning(slicer.util.mainWindow(),'Error Login', u'Registro exitoso')
                        else:
                            qt.QMessageBox.warning(slicer.util.mainWindow(),'Error Login', u'Conexión fallida con la base de datos')
                elif(self.profesorCheckBox.isChecked()):
                    ingreso=0;
                    profesores = []
                    cursor.execute("SELECT * FROM profesores")
                    rows = cursor.fetchall()
                    for row in rows:
                        profesores.append(row)
                    for i in range (0,len(profesores)):
                        if (self.name == profesores[i][1]): 
                            qt.QMessageBox.warning(slicer.util.mainWindow(),'Error Login', u'Ese nombre de usuario ya se encuentra registrado')   
                            break
                        else:
                            ingreso=1
                    if ingreso==1:
                        if (con!=None):
                            profesorid=int(len(profesores)+1)
                            Nombre=str(self.name)
                            Contrasena=str(self.contra)
                            add_produto = """INSERT INTO profesores(idProfesores,
                                            Nombre_Profesor,Contrasena_Profesor)
                                            VALUES ('%s','%s','%s')"""% (profesorid,Nombre,Contrasena)

                            cursor.execute(add_produto)
                            con.commit()
                            con.close()
                            qt.QMessageBox.warning(slicer.util.mainWindow(),'Error Login', u'Registro exitoso')
                        else:
                            qt.QMessageBox.warning(slicer.util.mainWindow(),'Error Login', u'Conexión fallida con la base de datos')
            else:
                qt.QMessageBox.warning(slicer.util.mainWindow(),'Error Login', u'Sus contraseñas no son iguales')
        else:
            qt.QMessageBox.warning(slicer.util.mainWindow(),'Error Login', u'Espacios vacios')

    def textchanged1(self,text):
        self.name = str(text)
        
    def textchanged2(self,text):
        self.contra = str(text)

    def textchanged3(self,text):
        self.contrar = str(text)
