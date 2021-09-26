#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>

int main(int argc , char** argv)
{
	ros::init(argc,argv,"nodetx");
	ros::NodeHandle n;
	ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter",1000);
	ros::Rate loop_rate(10);
	
	while(ros::ok())
	{
		std::string input;
		std_msgs::String msg;
		std::cout<<"Enter the sentence\n";
		std::getline(std::cin,input);
		msg.data = input;
		chatter_pub.publish(msg);
		ros::spinOnce();
		loop_rate.sleep();
	}
	return 0;
}
