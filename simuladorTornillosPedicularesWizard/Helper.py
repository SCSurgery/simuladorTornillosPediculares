# slicer imports
from __main__ import vtk, slicer

# python includes
import sys
import time

class Helper( object ):
  '''
  classdocs
  '''

  @staticmethod
  def findWidget(widget,objectName):
        if widget.objectName == objectName:
            return widget
        else:
            children = []
            for w in widget.children():
                resulting_widget = findWidget(w, objectName)
                if resulting_widget:
                    return resulting_widget
            return None