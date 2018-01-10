#include "LearnBotClient.h"


void readImage(params_image * params)
{
  while (true)
  {
    try
    {
      RoboCompRGBD::ColorSeq colorseq;
      RoboCompRGBD::DepthSeq depthseq;
      RoboCompGenericBase::TBaseState bState;
      RoboCompJointMotor::MotorStateMap hState;
      params->rgbd_proxy->getRGB(colorseq, hState, bState);
      params->image_mutex->lock();
      memcpy(params->image->data , &colorseq[0], 320*240*3);
      params->image_mutex->unlock();
    }
    catch(const Ice::Exception &e)
    {
      std::cout << "Error reading form RGBD " << e << std::endl;
    }
  }
};

void readSonars(params_sonars *params)
{
  while (true) {
    int i=0;
    std::vector<LaserPrx> l_prx_vec = params->laser_proxy_vector;
    for (auto lprx:l_prx_vec)
    {
      auto ldata = lprx->getLaserData();
      params->laser_mutex->lock();
      float min=ldata[0].dist;
      for (auto value:ldata)
        if (min<value.dist)
          min = value.dist;
      params->Ldata[i]= min;
      params->laser_mutex->unlock();
      i++;
    }
  }
}
//
// ClientCpp::ClientCpp(const ClientCpp &client)
// {
//   adv = client.adv;
//   rot = client.rot;
//   max_rot = client.max_rot;
//   image = client.image;
//   image_mutex = client.image_mutex;
//   ic = client.ic;
//   differentialrobot_proxy = client.differentialrobot_proxy;
//   rgbd_proxy = client.rgbd_proxy;
//   args_sonars = client.args_sonars;
// }

ClientCpp::ClientCpp(std::vector<std::string> argv_)
{
  char* argv[argv_.size()];
  for (int i=0;i< argv_.size(); i++)
  {
    argv[i] = new char[argv_[i].size()];
    strncpy(argv[i], argv_[i].c_str(), argv_[i].size());
  }
  initialize(argv_.size(), argv);
};

ClientCpp::ClientCpp(int argc, char* argv[])
{
  initialize(argc, argv);
};

void ClientCpp::initialize(int argc, char* argv[])
{
  image_mutex = new std::mutex();
  args_sonars.laser_mutex = new std::mutex();
  if (argc > 1)
  {
    if (!boost::starts_with(argv[1], "--Ice.Config="))
    {
      std::string ll = std::string("--Ice.Config=") + argv[1];
      argv[1] = new char[ll.size()];
      strncpy(argv[1], ll.c_str(), ll.size());
      ic = Ice::initialize(argc, argv);
    }
  }
  else if(argc == 1)
  {
    char* params1[2];
    std::string a1 = argv[0];
    params1[0] = new char[a1.size()];
    strncpy(params1[1], a1.c_str(), a1.size());
    std::string ll = std::string("--Ice.Config=config");
    params1[1] = new char[ll.size()];
    strncpy(params1[1], ll.c_str(), ll.size());
    ic = Ice::initialize(argc, params1);
  }

  std::string proxyString =ic->getProperties()->getProperty("DifferentialRobotProxy");
  differentialrobot_proxy = DifferentialRobotPrx::uncheckedCast( ic->stringToProxy( proxyString ) );
  if(!differentialrobot_proxy) throw std::runtime_error("Invalid proxy DifferentialRobotProxy");


  proxyString = ic->getProperties()->getProperty("RGBDProxy");
  rgbd_proxy = RGBDPrx::uncheckedCast( ic->stringToProxy( proxyString ) );
  if(!rgbd_proxy) throw std::runtime_error("Invalid proxy RGBDProxy");


  image.create(240,320, CV_8UC3);
  params_image args_image;
  args_image.image = &image;
  args_image.image_mutex = image_mutex;
  args_image.rgbd_proxy = rgbd_proxy;
  std::thread t1(readImage, &args_image);
  std::thread t2(readSonars, &args_sonars);
};


std::vector<float> ClientCpp::getSonars()
{
  args_sonars.laser_mutex->lock();
  std::vector<float> ldata;
  for (auto value:args_sonars.Ldata)
    ldata.push_back(value);
  args_sonars.laser_mutex->unlock();
  return ldata;
};


cv::Mat ClientCpp::getImage()
{
  image_mutex->lock();
  return image;
  image_mutex->unlock();
};

std::vector<float> ClientCpp::getPose()
{
  int x, y;
  float alpha;
  differentialrobot_proxy->getBasePose(x,y, alpha);
  std::vector<float> data = {(float)x, (float)y, alpha};
  return data;
};

void ClientCpp::setRobotSpeed(int vAdvance, int vRotation)
{
  if (vAdvance!=0 || vRotation!=0)
  {
      adv = vAdvance;
      rot = vRotation;
  }
  differentialrobot_proxy->setSpeedBase(adv,rot);
};
