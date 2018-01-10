cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

SET(RoboComp_INTERFACES_DIR "/home/learnbot/interfaces/")
include(cmake/learnbot.cmake)

ADD_DEFINITIONS( -std=c++11 )


PROJECT( LearnBot )

LEARNBOT_WRAP_ICE( RGBD Laser DifferentialRobot JointMotor GenericBase )


find_package(Boost COMPONENTS system thread python REQUIRED)
find_package(PythonLibs REQUIRED)
include_directories( ${PYTHON_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS} ${CMAKE_BINARY_DIR} )



MESSAGE(STATUS "${SOURCES}")
add_library(Client SHARED
    learnbot_dsl/LearnBotClient.cpp
    ${SOURCES}
)
