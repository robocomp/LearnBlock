#include <boost/python.hpp>
#include <boost/algorithm/string/predicate.hpp>
#include <opencv2/opencv.hpp>
#include "DifferentialRobot.h"
#include "RGBD.h"
#include "Laser.h"
#include "JointMotor.h"
#include "GenericBase.h"
#include <vector>

#include <Ice/Ice.h>
#include <mutex>
#include <thread>


using namespace boost::python;

using namespace RoboCompGenericBase;
using namespace RoboCompRGBD;
using namespace RoboCompJointMotor;
using namespace RoboCompDifferentialRobot;
using namespace RoboCompLaser;

#define ARRAY_SIZE(array) (sizeof((array))/sizeof((array[0])))

struct params_sonars
{
  std::vector<float> Ldata;
  std::mutex *laser_mutex;
  std::vector<LaserPrx> laser_proxy_vector;
};

struct params_image
{
  cv::Mat *image;
  std::mutex *image_mutex;
  RGBDPrx rgbd_proxy;
};

class ClientCpp
{
  private:

    int adv = 0;
    int rot = 0;
    float max_rot = 0.4;
    cv::Mat image;
    std::mutex *image_mutex;
    Ice::CommunicatorPtr ic;

// Proxies
    DifferentialRobotPrx differentialrobot_proxy;
    RGBDPrx rgbd_proxy;
    params_sonars args_sonars;

    // self.usList = {'front':1000, 'right':1000, 'left':1000, 'back':1000} TODO lasers
    // differentialrobot_proxy;
  public:
    ClientCpp(int argc, char* argv[]);
    ClientCpp(std::vector<std::string> argv_);
    // ClientCpp(const ClientCpp &client);
    void initialize(int argc, char* argv[]);
    std::vector<float> getSonars();
  	cv::Mat getImage();
  	std::vector<float> getPose();
  	void setRobotSpeed(int vAdvance, int vRotation);


};

BOOST_PYTHON_MODULE(Client)
{
    class_<ClientCpp>("ClientCpp", init<std::vector<std::string>>())
        .def("getSonars", &ClientCpp::getSonars)
        .def("getImage", &ClientCpp::getImage)
        .def("getPose", &ClientCpp::getPose)
        .def("setRobotSpeed", &ClientCpp::setRobotSpeed)
    ;
};
