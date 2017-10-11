import cv2
import numpy as np
import rospy
from krssg_ssl_msgs.msg import BeliefState
from gui_path.msg import point_array
from gui_path.msg import path_point
from gui_path.msg import point_SF

x=point_SF()
print("printing point_sf=", x)
cv2.namedWindow('bots', cv2.WINDOW_NORMAL)
img = np.zeros((400,600,3), np.uint8)
pub = rospy.Publisher('gui_params', point_SF)
vrtx=[(0,0),(0,0)]
s_x=200
s_y=200
f_x=0
f_y=0
points_home=[]
points_opp=[]

def display_bots(points_home, points_opp):
    global img, vrtx
    img = np.zeros((400,600,3), np.uint8)
    for point in points_home:
        cv2.circle(img,(point), 10, (255,0,255), -1)
    for point in points_opp:
        cv2.circle(img,(point), 10, (0,255,255), -1)    
    draw_path(vrtx)        
    cv2.imshow("bots", img)

def draw_path(vrtx):
    # print("in draw_path")
    p1 = vrtx[0]
    for v in vrtx[1:]:
        p2 = v
        cv2.line(img, p1, p2, (255,255,255), 2)
        p1=p2

def set_SF(event=None,x=0,y=0,flags=False,param=None):
    msg=point_SF()
    global s_x, s_y, f_x, f_y
    if(len(points_home)==0):
        print(" home pos is empty. setting s_p = 200,200")
    
    if(event == cv2.EVENT_LBUTTONDOWN):    
        f_x = x
        f_y = y
        s_x = points_home[1][0]
        s_y = points_home[1][1]
    else:
        return

    msg.s_x = s_x
    msg.s_y = s_y
    msg.f_x = f_x
    msg.f_y = f_y
    sl=[]
    for i in points_opp:
        temp = path_point()
        temp.x=i[0]
        temp.y=i[1]
        # print("appendin ",temp)
        msg.obstacles.append(temp)
        # print("now ", sl)
    for i in range(6):
        if(i==1):
            continue
        temp = path_point()    
        temp.x=points_home[i][0]
        temp.y=points_home[i][1]    
        msg.obstacles.append(temp)        
    print("s = ", s_x, s_y)
    print("f = ",f_x,f_y)
    print("points_home = ", points_home)
    print("points_opp = ", points_opp)
    print(msg.obstacles)
    msg.step_size=50
    msg.bias_param=100
    msg.max_iteration=1000
    pub.publish(msg)
    print("published SF msgs on gui_params")

cv2.setMouseCallback('bots', set_SF)

def Callback(msg):
    global points_home
    points_home=[]
    for i in msg.homePos:
        points_home.append((int(i.x)/10+300, int(i.y)/10+200))
    global points_opp    
    points_opp=[]
    for i in msg.awayPos:
        points_opp.append((int(i.x)/10+300, int(i.y)/10+200))   
    display_bots(points_home, points_opp)  
    # set_SF() 

def debug_path(msg):
    global vrtx
    vrtx=[]
    for v in msg.point_array:
        vrtx.append(((int(v.x)),int(v.y)))
    print("received path points, size = ",len(vrtx))    



if __name__ == '__main__':
    rospy.init_node('display', anonymous=True)
    rospy.Subscriber("/belief_state", BeliefState , Callback);
    rospy.Subscriber("path_planner", point_array, debug_path)
    # points = [(5,5),(100,100),(200,200),(301,301)]
    set_SF()
    # display_bots(points)
    cv2.waitKey(0)