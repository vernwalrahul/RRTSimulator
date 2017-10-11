from PyQt4 import QtCore,QtGui
import sys
import rospy
import numpy as np
from interfacePath import Ui_MainWindow
from krssg_ssl_msgs.msg import BeliefState
from ast import literal_eval
from krssg_ssl_msgs.msg import point_2d
from krssg_ssl_msgs.msg import planner_path
from krssg_ssl_msgs.msg import point_SF


points_home=[]
points_opp=[]
vrtx=[(200,200)]
count = 0
pub = rospy.Publisher('gui_params', point_SF)


def debug_path(msg):
    global vrtx
    vrtx=[]
    for v in msg.point_array:
        vrtx.append(((int(v.x)),int(v.y)))
    print("received path points, size = ",len(vrtx))        

              
    # cv2.imshow("bots", img)
    # print(" in display bots here")

def Callback(msg):
    # print(" in callback")
    global points_home
    points_home=[]
    for i in msg.homePos:
        points_home.append((int(i.x)/10+300, int(i.y)/10+200))
    global points_opp    
    points_opp=[]
    for i in msg.awayPos:
        points_opp.append((int(i.x)/10+300, int(i.y)/10+200))


class MainWindow(QtGui.QMainWindow, Ui_MainWindow, QtGui.QWidget):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.scene = QtGui.QGraphicsScene()
        self.image = None
        self.sendData.clicked.connect(self.sendParams)
        #self.updatePath.clicked.connect(self.update_path)
        self.refresh.clicked.connect(self.hide_all)
        self.obstacleRadius = 10
        self.graphicsView.setFixedSize(650,450)
        self.scene.setSceneRect(0, 0, 600, 400)
        self.graphicsView.setScene(self.scene)
        self.hide_all()
        self.pen = QtGui.QPen(QtCore.Qt.green)
        self.mark_s = QtGui.QPen(QtCore.Qt.red)
        self.mark_e = QtGui.QPen(QtCore.Qt.blue)

        self.mark_start = QtGui.QPen(QtCore.Qt.yellow)
        self.mark_goal = QtGui.QPen(QtCore.Qt.green)
        # self.videoFrame=ImageWidget()
        # self.setCentralWidget(self.videoFrame)
        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateImage)
        self.timer.start(30)
        try:
            self.start = literal_eval(str(self.startPointText.text()))
            self.goal = literal_eval(str(self.endPointText.text()))
            self.start[1]-=20
            self.goal[1]-=20
        except Exception as e:
            print("error: ",e)
            self.start=[0,0]
            self.goal=[200,200]    
        # self.capture = cv2.VideoCapture(0)
    def hide_all(self):
        # self.setCentralWidget(self)
        pass

    def sendParams(self):
        stepSize = float(self.stepSizeText.text())
        biasParam = float(self.biasParamText.text())
        maxIterations = float(self.maxIterationsText.text())
        self.start = literal_eval(str(self.startPointText.text()))
        self.goal = literal_eval(str(self.endPointText.text()))
        print("in send params start = ",self.start," goal = ",self.goal)
        # self.start[1]-=20
        # self.goal[1]-=20
        msg=point_SF()
        msg.s_x=self.start[0]
        msg.s_y=self.start[1]
        msg.f_x=self.goal[0]
        msg.f_y=self.goal[1]
        print(" here step_size ",stepSize)
        msg.step_size=stepSize
        msg.bias_param=biasParam
        msg.max_iteration=maxIterations
        pub.publish(msg)
        pass        

    def updateImage(self):
       
        self.display_bots(points_home, points_opp)

    def paintEvent(self,event):
        # print(" in paint event")
        qp=QtGui.QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QtCore.QPoint(0,0),self.image)
        qp.end()  

    def mousePressEvent(self , e):
        global count
        count += 1
        pt=QtCore.QPointF(self.graphicsView.mapToScene(e.pos()))
        print("in mouse event")
        brush= QtGui.QBrush(QtCore.Qt.SolidPattern)

        if(count == 1):
            self.start = (pt.x(),pt.y())
            self.startPointText.setText(str(self.start))
            self.scene.addEllipse(self.start[0],self.start[1],self.obstacleRadius,self.obstacleRadius , self.mark_start, brush)
        else :
            self.goal = (pt.x(),pt.y())
            self.endPointText.setText(str(self.goal))
            self.scene.addEllipse(self.goal[0],self.goal[1],self.obstacleRadius,self.obstacleRadius , self.mark_goal, brush)
            count = 0    

    def display_bots(self, points_home, points_opp):
        global img, vrtx
        self.scene.clear()
        self.graphicsView.setScene(self.scene)
        img = np.zeros((400,600,3), np.uint8)
        brush= QtGui.QBrush(QtCore.Qt.SolidPattern)
        for point in points_home:
            self.scene.addEllipse(point[0], point[1],self.obstacleRadius,self.obstacleRadius , self.mark_e, brush)
        for point in points_opp:
            self.scene.addEllipse(point[0], point[1],self.obstacleRadius,self.obstacleRadius , self.mark_s, brush) 
        self.draw_path(vrtx) 
        self.scene.addEllipse(self.start[0],self.start[1],self.obstacleRadius,self.obstacleRadius , self.mark_start, brush)
        self.scene.addEllipse(self.goal[0],self.goal[1],self.obstacleRadius,self.obstacleRadius , self.mark_goal, brush) 

    def draw_path(self, vrtx):
    # print("in draw_path")
        path = QtGui.QPainterPath()
        # print("in draw_path")
        path.moveTo(vrtx[0][0],vrtx[0][1])
        for i in vrtx[1:]:
            path.lineTo(i[0],i[1])
        
        self.scene.addPath(path)

app=QtGui.QApplication(sys.argv)
w=MainWindow()
def main():
    rospy.init_node('display', anonymous=True)
    rospy.Subscriber("/belief_state", BeliefState , Callback);
    rospy.Subscriber("/path_planner", planner_path, debug_path)

    w.show()
    app.exec_()

if __name__=='__main__':
    main()