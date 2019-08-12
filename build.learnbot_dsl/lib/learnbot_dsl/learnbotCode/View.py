from __future__ import print_function, absolute_import
from learnbot_dsl.learnbotCode.VisualBlock import *


class MyView(QtWidgets.QGraphicsView):

    def __init__(self, scene, parent, arg=None):
        self.zoom = None
        QtWidgets.QGraphicsView.__init__(self, scene, parent)

    def setZoom(self, zoom):
        self.zoom = zoom

    def wheelEvent(self, event):
        if self.zoom:
            # Zoom Factor
            zoomInFactor = 1.25
            zoomOutFactor = 1 / zoomInFactor

            # Set Anchors
            self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
            self.setResizeAnchor(QtWidgets.QGraphicsView.NoAnchor)

            # Save the scene pos
            oldPos = self.mapToScene(event.pos())

            # Zoom
            if event.delta() > 0:
                zoomFactor = zoomInFactor
            else:
                zoomFactor = zoomOutFactor
            self.scale(zoomFactor, zoomFactor)

            # Get the new position
            newPos = self.mapToScene(event.pos())

            # Move scene to old position
            delta = newPos - oldPos
            self.translate(delta.x(), delta.y())
