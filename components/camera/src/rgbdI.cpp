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
#include "rgbdI.h"

RGBDI::RGBDI(GenericWorker *_worker, QObject *parent) : QObject(parent)
{
	worker = _worker;
	mutex = worker->mutex;       // Shared worker mutex
}


RGBDI::~RGBDI()
{
}

Registration RGBDI::getRegistration(const Ice::Current&)
{
	return worker->getRegistration();
}

void RGBDI::getImage( ColorSeq  &color,  DepthSeq  &depth,  PointSeq  &points,  RoboCompJointMotor::MotorStateMap  &hState,  RoboCompDifferentialRobot::TBaseState  &bState, const Ice::Current&)
{
	worker->getImage(color, depth, points, hState, bState);
}

void RGBDI::getXYZ( PointSeq  &points,  RoboCompJointMotor::MotorStateMap  &hState,  RoboCompDifferentialRobot::TBaseState  &bState, const Ice::Current&)
{
	worker->getXYZ(points, hState, bState);
}

void RGBDI::getRGB( ColorSeq  &color,  RoboCompJointMotor::MotorStateMap  &hState,  RoboCompDifferentialRobot::TBaseState  &bState, const Ice::Current&)
{
	worker->getRGB(color, hState, bState);
}

TRGBDParams RGBDI::getRGBDParams(const Ice::Current&)
{
	return worker->getRGBDParams();
}

void RGBDI::getDepth( DepthSeq  &depth,  RoboCompJointMotor::MotorStateMap  &hState,  RoboCompDifferentialRobot::TBaseState  &bState, const Ice::Current&)
{
	worker->getDepth(depth, hState, bState);
}

void RGBDI::setRegistration( Registration  value, const Ice::Current&)
{
	worker->setRegistration(value);
}

void RGBDI::getData( imgType  &rgbMatrix,  depthType  &distanceMatrix,  RoboCompJointMotor::MotorStateMap  &hState,  RoboCompDifferentialRobot::TBaseState  &bState, const Ice::Current&)
{
	worker->getData(rgbMatrix, distanceMatrix, hState, bState);
}

void RGBDI::getDepthInIR( depthType  &distanceMatrix,  RoboCompJointMotor::MotorStateMap  &hState,  RoboCompDifferentialRobot::TBaseState  &bState, const Ice::Current&)
{
	worker->getDepthInIR(distanceMatrix, hState, bState);
}






