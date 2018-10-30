/*
* main.cpp
*
*  Created on: 2018. 10. 16.
*      Author: Fabian Pérez
*/

#include <stdio.h>
#include <unistd.h>
#include <limits.h>
#include <string.h>
#include <libgen.h>
#include <signal.h>
#include <stdlib.h>

#include "mjpg_streamer.h"
#include "LinuxDARwIn.h"

#include "StatusCheck.h"
#include "VisionMode.h"
#include "LinuxNetwork.h"

#ifdef MX28_1024
#define MOTION_FILE_PATH    "../../../Data/motion_1024.bin"
#else
#define MOTION_FILE_PATH    "../../../Data/motion_4096.bin"
#endif

#define INI_FILE_PATH       "../../../Data/config.ini"
#define SCRIPT_FILE_PATH    "script.asc"

#define U2D_DEV_NAME0       "/dev/ttyUSB0"
#define U2D_DEV_NAME1       "/dev/ttyUSB1"

#define ADDRESS         "192.168.0.67"
#define PORT		        20005
#define COMMANDLENGTH   8

using namespace Robot;

LinuxCM730 linux_cm730(U2D_DEV_NAME0);
CM730 cm730(&linux_cm730);

void change_current_dir()
{
  char exepath[1024] = {0};
  if(readlink("/proc/self/exe", exepath, sizeof(exepath)) != -1)
  {
    if(chdir(dirname(exepath)))
    fprintf(stderr, "chdir error!! \n");
  }
}

void Go_Position(int hue, int hue_tol, int min_sat, int min_val, float min_per, float max_per)
{
  Image* rgb_ball = new Image(Camera::WIDTH, Camera::HEIGHT, Image::RGB_PIXEL_SIZE);

  minIni* ini = new minIni(INI_FILE_PATH);

  LinuxCamera::GetInstance()->CreateCamera();
  LinuxCamera::GetInstance()->Initialize(0);
  LinuxCamera::GetInstance()->LoadINISettings(ini);

  ColorFinder* ball_finder = new ColorFinder(hue, hue_tol, min_sat, min_val, min_per, max_per);
  ball_finder->LoadINISettings(ini);
  httpd::ball_finder = ball_finder;

  BallTracker tracker = BallTracker();
  BallFollower follower = BallFollower();
  follower.DEBUG_PRINT = true;

  int n = 0;
  int param[JointData::NUMBER_OF_JOINTS * 5];
  int wGoalPosition, wStartPosition, wDistance;

  for(int id=JointData::ID_R_SHOULDER_PITCH; id<JointData::NUMBER_OF_JOINTS; id++)
  {
    wStartPosition = MotionStatus::m_CurrentJoints.GetValue(id);
    wGoalPosition = Walking::GetInstance()->m_Joint.GetValue(id);
    if( wStartPosition > wGoalPosition )
    wDistance = wStartPosition - wGoalPosition;
    else
    wDistance = wGoalPosition - wStartPosition;

    wDistance >>= 2;
    if( wDistance < 8 )
    wDistance = 8;

    param[n++] = id;
    param[n++] = CM730::GetLowByte(wGoalPosition);
    param[n++] = CM730::GetHighByte(wGoalPosition);
    param[n++] = CM730::GetLowByte(wDistance);
    param[n++] = CM730::GetHighByte(wDistance);
  }
  cm730.SyncWrite(MX28::P_GOAL_POSITION_L, 5, JointData::NUMBER_OF_JOINTS - 1, param);

  Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
  Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);

  bool goal = true;
  while(goal)
  {
    Point2D pos;
    LinuxCamera::GetInstance()->CaptureFrame();

    memcpy(rgb_ball->m_ImageData, LinuxCamera::GetInstance()->fbuffer->m_RGBFrame->m_ImageData, LinuxCamera::GetInstance()->fbuffer->m_RGBFrame->m_ImageSize);

    tracker.Process(ball_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame));
    follower.Process(tracker.ball_position);
    if (follower.KickBall == 1)
    {
      goal = false;
      LinuxCamera::GetInstance()->CloseCamera();
    }
  }
}

/////////////////// MAIN /////////////////////

pid_t pid_camera;

void openMplayer(){
  pid_camera = fork();
  if(pid_camera < 0 ){
    printf("Failed creating child process");
    exit(1);
  }
  else if(pid_camera == 0){
    execlp("/usr/bin/mplayer", "mplayer", "tv://", "driver=v4l2:width=1600:height=900:device=/dev/video0", NULL);
  }
}

void closeMplayer(){
  kill(pid_camera, SIGTERM);
}

void setHeadAngle(unsigned char *command){
  Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
  Head::GetInstance()->MoveByAngle(  command[1] ? ((double)command[2]) : -((double)command[2]) ,
                                      command[3] ? ((double)command[4]) : -((double)command[4]));
}

#define PARADO 1
#define ACAMINAR 9
#define SENTADO 15

void setDarwinPosition(int pos){
  Action::GetInstance()->m_Joint.SetEnableBody(true, true);
  Action::GetInstance()->Start(pos);
  while(Action::GetInstance()->IsRunning()) usleep(8*1000);
}

int main(void)
{
  change_current_dir();

  minIni* ini = new minIni(INI_FILE_PATH);

  //////////////////// Framework Initialize ////////////////////////////
  LinuxCM730 linux_cm730(U2D_DEV_NAME0);
  CM730 cm730(&linux_cm730);
  if(MotionManager::GetInstance()->Initialize(&cm730) == false)
  {
    linux_cm730.SetPortName(U2D_DEV_NAME1);
    if(MotionManager::GetInstance()->Initialize(&cm730) == false)
    {
      printf("Fail to initialize Motion Manager!\n");
      return 0;
    }
  }
  Walking::GetInstance()->LoadINISettings(ini);

  MotionManager::GetInstance()->AddModule((MotionModule*)Action::GetInstance());
  MotionManager::GetInstance()->AddModule((MotionModule*)Head::GetInstance());
  MotionManager::GetInstance()->AddModule((MotionModule*)Walking::GetInstance());

  LinuxMotionTimer *motion_timer = new LinuxMotionTimer(MotionManager::GetInstance());
  motion_timer->Start();
  /////////////////////////////////////////////////////////////////////

  MotionManager::GetInstance()->LoadINISettings(ini);

  int firm_ver = 0;
  if(cm730.ReadByte(JointData::ID_HEAD_PAN, MX28::P_VERSION, &firm_ver, 0)  != CM730::SUCCESS)
  {
    fprintf(stderr, "Can't read firmware version from Dynamixel ID %d!! \n\n", JointData::ID_HEAD_PAN);
    exit(0);
  }

  if(0 < firm_ver && firm_ver < 27)
  {
    #ifdef MX28_1024
    Action::GetInstance()->LoadFile(MOTION_FILE_PATH);
    #else
    fprintf(stderr, "MX-28's firmware is not support 4096 resolution!! \n");
    fprintf(stderr, "Upgrade MX-28's firmware to version 27(0x1B) or higher.\n\n");
    exit(0);
    #endif
  }
  else if(27 <= firm_ver)
  {
    #ifdef MX28_1024
    fprintf(stderr, "MX-28's firmware is not support 1024 resolution!! \n");
    fprintf(stderr, "Remove '#define MX28_1024' from 'MX28.h' file and rebuild.\n\n");
    exit(0);
    #else
    Action::GetInstance()->LoadFile((char*)MOTION_FILE_PATH);
    #endif
  }
  else
  exit(0);

  Action::GetInstance()->m_Joint.SetEnableBody(true, true);
  MotionManager::GetInstance()->SetEnable(true);

  cm730.WriteByte(CM730::P_LED_PANNEL, 0x01|0x02|0x04, NULL);
  cm730.WriteWord(CM730::P_LED_EYE_L, cm730.MakeColor(0, 0, 0), NULL);
  Action::GetInstance()->Start(15);
  while(Action::GetInstance()->IsRunning()) usleep(8*1000);
  cm730.WriteWord(CM730::P_LED_EYE_L, cm730.MakeColor(10, 200, 255), NULL);

  /////////////// MAIN WHILE /////////////////////

  LinuxSocket client;
  client.create();
  client.set_non_blocking(true);

  int reconnectCounter = 0;

  while(1){
    reconnectCounter++;

    if(client.connect(ADDRESS, PORT)){
      setDarwinPosition(PARADO);
      printf("Conexion establecida con %s. Port %d\n", ADDRESS, PORT);
      bool clientConnected = true;
      openMplayer();
      while(clientConnected){
        cm730.WriteWord(CM730::P_LED_EYE_L, cm730.MakeColor(0, 0, 0), NULL);
        usleep(50*1000);
        cm730.WriteWord(CM730::P_LED_EYE_L, cm730.MakeColor(10, 200, 255), NULL);
        usleep(500*1000);
        unsigned char command[COMMANDLENGTH] = "OFIR___";
        int len = client.recv(command, COMMANDLENGTH);
        if(len>0){
          int id;
          printf("%u\n", command[0]);
          id = command[0];
          if(id == 0){
            closeMplayer();
            setDarwinPosition(ACAMINAR);
            Go_Position((int)(command[1])+256*(command[2]), command[3], command[4], command[5], 0.3, 50.0);
            setDarwinPosition(PARADO);
            openMplayer();
          }if(id == 1){
            setHeadAngle(command);
          }if(id == 2){
            Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);

          }if(id == 10){
            Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
            //Walking::GetInstance()->X_MOVE_AMPLITUDE = 0.0;
            //Walking::GetInstance()->A_MOVE_AMPLITUDE = 0.0;
            Walking::GetInstance()->Stop();
            setDarwinPosition(PARADO);
          }if(id == 11){
            setDarwinPosition(ACAMINAR);
            Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
            Walking::GetInstance()->X_MOVE_AMPLITUDE = 1.0;
            Walking::GetInstance()->A_MOVE_AMPLITUDE = 0.0;
            Walking::GetInstance()->Start();
          }if(id == 12){
            setDarwinPosition(ACAMINAR);
            Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
            Walking::GetInstance()->X_MOVE_AMPLITUDE = 0.1;
            Walking::GetInstance()->A_MOVE_AMPLITUDE = 0.0;
            Walking::GetInstance()->Start();
          }

        }
      }
    }else{
      printf("Conexion rechazada [%d], reconectando en 1 seg \n", reconnectCounter);
      usleep(1000*1000);
      if(reconnectCounter >= 10)
      return 1;
    }
  }

  return 0;
}
