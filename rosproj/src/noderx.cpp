#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>

void chatterCallback(const std_msgs::String::ConstPtr& msg)
{
	int a  = msg->data.length();
	std::cout<<a;

	std::cout<<"The original string:"<<msg->data;
	std::string rev = "";
	for(int i = a-1;i>=0;i--)
	{
	 rev =rev + msg->data[i];
	}
	std::cout<<"\nThe reversed string: "<<rev<<"\n";
}
int main(int argc, char **argv)
{
	ros::init(argc, argv, "noderx");
	ros::NodeHandle n;
	ros::Subscriber sub = n.subscribe("chatter", 1000, chatterCallback);
	ros::spin();
	return 0;
}
