#include <iostream>

#include "RRT_implementation.hpp"
#include "ros/ros.h"
#include "krssg_ssl_msgs/BeliefState.h"
#include "krssg_ssl_msgs/planner_path.h"
#include "krssg_ssl_msgs/point_2d.h"
#include "krssg_ssl_msgs/point_SF.h"

using namespace std;
using namespace rrt;
Utils::Point<int> start,finish,origin;
vector<Utils::Point<int> > ObstaclePoints;
RRT<int> test;
long int p=0;
ros::Publisher pub;

bool check(Utils::Point<int> cur)
{
	if(abs(cur.x)<2000 && abs(cur.y)<2000){
		// if (cur.x < 550 && cur.x > 450 && cur.y < 550 & cur.y > 450)
		// {
		// 	return false;
		// }
		return true;
	}
	return false;
}


void send_points()
{
	krssg_ssl_msgs::planner_path points;
	 
	krssg_ssl_msgs::point_2d point;
    vector<Utils::Point<int> > path=test.getPointsOnPath();
	

	// for(int i=0;i<path.size();i++)
	// 	cout<<"("<<path[i].x<<","<<path[i].y<<")";
	  int count = 0;

	
	  cout<<" path.size() = "<<path.size()<<endl;
	  cout<<" start = "<<path[0].x<<","<<path[0].y<<"  Finish = "<<path[path.size()-1].x<<","<<path[path.size()-1].y<<endl;
	  for(int i=0;i<path.size();i++)
	  {
	  	point.x=path[i].x;
	  	point.y=path[i].y;
	  	points.point_array.push_back(point);
	  	// cout<<path[i].x<<","<<path[i].y<<endl;
	  }	  

	 

	  pub.publish(points); cout<<"data published "<<p++<<endl;
}

void callback(const krssg_ssl_msgs::point_SF::ConstPtr& msg)
{
	cout<<" got step_size="<<msg->step_size<<" max_iteration="<<msg->max_iteration<<endl;
	start.x=msg->s_x;
	start.y=msg->s_y;
	finish.x=msg->f_x;
	finish.y=msg->f_y;
	cout<<" start = "<<start.x<<","<<start.y<<" end = "<<finish.x<<","<<finish.y<<endl;
	test.setStepLength(msg->step_size);
	test.setBiasParameter(msg->bias_param);
	test.setMaxIterations(msg->max_iteration);
	test.setEndPoints(start,finish);

	Utils::Point<int> temp;

	temp.x=100;
	temp.y=100;
	ObstaclePoints.push_back(temp);

	test.plan(ObstaclePoints);
	cout<<"Hey!!!!!";
	send_points();
}

int main(int argc, char** argv)
{	
	ros::init(argc, argv, "mkPath_cpp");
	ros::NodeHandle n;
	// ros::NodeHandle n1;

    ros::Subscriber sub = n.subscribe("/gui_params", 1000, callback);
    pub = n.advertise<krssg_ssl_msgs::planner_path>("path_planner", 1000);
      
	

	srand(time(NULL));
	start.x=-10;
	start.y=10;
	finish.x=1000;
	finish.y=730;
	origin.x=0;
	origin.y=0;

	test.setEndPoints(start,finish);
	test.setCheckPointFunction(*(check));
	test.setStepLength(50);
	test.setHalfDimensions(2000.0,2000.0);
	test.setBiasParameter(100);
	test.setOrigin(origin);
	test.setMaxIterations(10000);
	test.plan(ObstaclePoints);
	// test1.setEndPoints(start,finish);
	// test1.setCheckPointFunction(*(check));
	// test1.setStepLength(200);
	// test1.setHalfDimensions(2000.0,2000.0);
	// test1.setBiasParameter(100);
	// test1.setOrigin(origin);
	// test1.setMaxIterations(10000);
	// test2.plan();

	
	 // send_points();
     ros::spin();
	  	// {pub.publish(points); cout<<"data published "<<p++<<endl; ros::spinOnce();usleep(1000*200);}
    
    // ros::Rate loop_rate(10);

	// cout<<"sfd"<<connectA.x<<","<<connectA.y<<" "<<connectB.x<<","<<connectB.y;
}	
