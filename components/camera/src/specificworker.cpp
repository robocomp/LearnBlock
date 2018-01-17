/*
 *    Copyright (C) 2018 by YOUR NAME HERE
 *
 *    This file is part of RoboComp
 *
 *    RoboComp is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    RoboComp is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License
 *    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
 */
#include "specificworker.h"

/**
* \brief Default constructor
*/
SpecificWorker::SpecificWorker(MapPrx& mprx) : GenericWorker(mprx)
{
	writer = new uchar[240*320*3];
	reader = new uchar[240*320*3];
	cam = VideoCapture(0);
	double fps = cam.get(CV_CAP_PROP_FPS);
	qDebug()<<fps<<"fps";
	cam.set(38, 1);
	if (!cam.isOpened()) { //check if video device has been initialised
		cout << "cannot open camera";
	}
}

/**
* \brief Default destructor
*/
SpecificWorker::~SpecificWorker()
{

}

bool SpecificWorker::setParams(RoboCompCommonBehavior::ParameterList params)
{




	timer.start(0);


	return true;
}

void SpecificWorker::compute()
{
	cam >> cameraFrame;
	resize(cameraFrame,dst, Size(320,240));
	copy(dst.data,dst.data+240*320*3,writer);
	QMutexLocker locker(mutex);
	swap(writer, reader);
}


Registration SpecificWorker::getRegistration()
{

}

void SpecificWorker::getImage(ColorSeq &color, DepthSeq &depth, PointSeq &points, RoboCompJointMotor::MotorStateMap &hState, RoboCompDifferentialRobot::TBaseState &bState)
{

}

void SpecificWorker::getXYZ(PointSeq &points, RoboCompJointMotor::MotorStateMap &hState, RoboCompDifferentialRobot::TBaseState &bState)
{

}

void SpecificWorker::getRGB(ColorSeq &color, RoboCompJointMotor::MotorStateMap &hState, RoboCompDifferentialRobot::TBaseState &bState)
{

}

TRGBDParams SpecificWorker::getRGBDParams()
{

}

void SpecificWorker::getDepth(DepthSeq &depth, RoboCompJointMotor::MotorStateMap &hState, RoboCompDifferentialRobot::TBaseState &bState)
{

}

void SpecificWorker::setRegistration(const Registration &value)
{

}

void SpecificWorker::getData(imgType &rgbMatrix, depthType &distanceMatrix, RoboCompJointMotor::MotorStateMap &hState, RoboCompDifferentialRobot::TBaseState &bState)
{
	QMutexLocker locker(mutex);
	rgbMatrix = RoboCompRGBD::imgType(reader,reader+320*240*3);
}

void SpecificWorker::getDepthInIR(depthType &distanceMatrix, RoboCompJointMotor::MotorStateMap &hState, RoboCompDifferentialRobot::TBaseState &bState)
{

}






