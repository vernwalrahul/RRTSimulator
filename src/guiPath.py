import sys
from interfacePath import Ui_MainWindow
from PyQt4 import QtCore, QtGui
import rospy
from ast import literal_eval
from gui_path.msg import point_array
from gui_path.msg import path_point
from gui_path.msg import point_SF
from krssg_ssl_msgs.msg import *
import time

isSubmit = False
stepSize = 0
biasParam = 0
maxIterations = 0
count =0
vrtx = []
rgb = []
obslist = []
awayPos=[]
homePos =[]
pub = rospy.Publisher('gui_params', point_SF)
#import path_listener

rospy.init_node('path_listener', anonymous=True)
class MyFirstGuiProgram(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        
        QtGui.QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        
        self.scene = QtGui.QGraphicsScene()

        self.graphicsView.setFixedSize(600,400)
        self.scene.setSceneRect(0, 0, 600, 400)
        self.graphicsView.setScene(self.scene)
        self.hide_all()
        self.pen = QtGui.QPen(QtCore.Qt.green)
        self.mark_s = QtGui.QPen(QtCore.Qt.red)
        self.mark_e = QtGui.QPen(QtCore.Qt.blue)
        self.sendData.clicked.connect(self.sendParams)
        #self.updatePath.clicked.connect(self.update_path)
        self.refresh.clicked.connect(self.hide_all)
        self.menubar.setStyleSheet("background-color: red")

    def hide_all(self):
        self.stepSizeText.setVisible(False)
        self.stepSize.setVisible(False)
        self.maxIterationsText.setVisible(False)
        self.biasParamText.setVisible(False)
        self.maxIterations.setVisible(False)
        self.biasParam.setVisible(False)
        self.scene.clear()
        self.graphicsView.setScene(self.scene)
        print("in hideall")

    def refresh_window(self):
        # time.sleep(0.005)
        global awayPos
        global homePos
        self.scene.clear()
        self.graphicsView.setScene(self.scene)
         
        brush= QtGui.QBrush(QtCore.Qt.SolidPattern)
        #self.drawPath()
        c_=0
        for i in homePos[1:7]:
            if (i.x/15+300) < 600 and  (i.y/15+200) < 400:
              # print ("position of bot 1",int(i.x),int(i.y))
              self.scene.addEllipse(int(i.x/15+300),int(i.y/15+200),self.obstacleRadius,self.obstacleRadius , self.mark_e, brush)      
              # print(c_," no bot added at ",int(i.x/15+300),int(i.y/15+200))
              c_+=1

    def sendParams(self):
        global stepSize, biasParam, maxIterations
        stepSize = float(self.stepSizeText.text())
        biasParam = float(self.biasParamText.text())
        maxIterations = float(self.maxIterationsText.text())
        self.start = literal_eval(str(self.startPointText.text()))
        self.goal = literal_eval(str(self.endPointText.text()))
        send_point(self.start, self.goal)
        isSubmit = True


    def update_path(self):
        self.refresh_window()
        self.drawPath()

import sys

p=0

def send_point(p1, p2):
    msg=point_SF()
    msg.s_x=p1[0]
    msg.s_y=p1[1]
    msg.f_x=p2[0]
    msg.f_y=p2[1]
    print(" here step_size ",stepSize)
    msg.step_size=stepSize
    msg.bias_param=biasParam
    msg.max_iteration=maxIterations
    pub.publish(msg)


def Callback(msg):
    global awayPos
    global homePos
    # print("in callback")
    awayPos , homePos =[] , []
    awayPos=msg.awayPos 
    homePos=msg.homePos
    # print(homePos[0])
    # w.hide_all()
    w.refresh_window()
    # time.sleep(1);
    #rospy.spin()


app = QtGui.QApplication(sys.argv)
w = MyFirstGuiProgram()
if __name__ == '__main__':
    # rospy.Subscriber("path_planner", point_array, debug_path)
    # rospy.Subscriber("/belief_state", BeliefState , Callback);
    #path_listener()

    w.show()
    app.exec_()
    sys.exit()
