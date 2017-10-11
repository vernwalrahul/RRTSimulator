import sys
from interfacePath import Ui_MainWindow
from PyQt4 import QtCore, QtGui
import rospy
from gui_path.msg import point_array
from gui_path.msg import path_point
import time
vrtx = []
rgb = []
obslist = []

class MyFirstGuiProgram(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        # path_listener()
        # vrtx = path_listener.get_points()
        #these will be given by pathplanner
        #self.obstacles=[(5,8) , (100,100) , (10 ,50)] 
        #self.pathPoints=[(100,50) , ( -100 ,-200), (-100,120) , (100,100)]
        self.obstacleRadius= 50
        self.obstacles=[(100,100)]
        self.pathPoints=[(0,0),(200,200)]
        print(vrtx,"in guiPath")
        # for obs in obslist:
        #     print("\n\n\n\n in obs_list ")
        #     self.obstacles.append((int(obs[0]), int(obs[1])))

        for v in vrtx:
            self.pathPoints.append((int(v[0]), int(v[1])))

        # for clr in rgb:
        #     self.clrlist.append(int(clr))

        #other information like obstacleRadius, boundry, will be taken from congif file

        QtGui.QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        print("setup done!")
        
        self.scene = QtGui.QGraphicsScene()
        print("graphics_scene done")
        
        self.graphicsView.setScene(self.scene)
        print("set scene done")
        
        self.pen = QtGui.QPen(QtCore.Qt.green)
        print("qpen done")
        
        self.submit.clicked.connect(self.sendParams)

    def refresh_window(self):
        print("in refresh_window")
        for v in vrtx:
            self.pathPoints.append((int(v[0]), int(v[1])))
        self.drawObstacles()
        self.drawPath()  
        w.show()      

    def paintEvent(self, e):
        self.drawObstacles()
        self.drawPath()


    def drawObstacles(self ):
        brush= QtGui.QBrush(QtCore.Qt.SolidPattern)
        for i in self.obstacles:
            self.scene.addEllipse(i[0],i[1],self.obstacleRadius,self.obstacleRadius , self.pen, brush)

    def drawPath(self):
        path = QtGui.QPainterPath()
        path.moveTo(self.pathPoints[0][0],self.pathPoints[0][1])
        for i in self.pathPoints:
            path.lineTo(i[0],i[1])
            self.scene.addPath(path)

    def sendParams(self):
        stepSize = float(self.stepSizeText.text())
        biasParam = float(self.biasParamText.text())
        maxIterations = float(self.maxIterationsText.text())
        print("THESE DATA HAVE TO BE SENT TO PATHPLANNER by path_params ros node stepsize {} , maxiter {} , biasparam {} " .format(stepSize,maxIterations , biasParam))
        isSubmit = True

if __name__ == '__main__':
    # path_listener()
    import sys
    app = QtGui.QApplication(sys.argv)
    print("creating object")
    w = MyFirstGuiProgram()
    print("object created")
    time.sleep(5)

    w.show()
    print("showing done")
    sys.exit(app.exec_())        