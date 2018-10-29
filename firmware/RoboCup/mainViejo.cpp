/*
 * main.cpp
 *
 *  Created on: 2011. 1. 4.
 *      Author: robotis
 */

/// -v es-la -p 75 -s 190 -a 80

#include <stdio.h>
#include <unistd.h>
#include <limits.h>
#include <string.h>
#include <libgen.h>
#include <signal.h>


#include <cstdlib>
#include <iostream>
#include <errno.h>

#include "mjpg_streamer.h"
#include "LinuxDARwIn.h"

#ifdef MX28_1024
#define MOTION_FILE_PATH    "../../../Data/motion_1024.bin"
#else
#define MOTION_FILE_PATH    "../../../Data/motion_4096.bin"
#endif

#define INI_FILE_PATH       "../../../Data/config.ini"
#define SCRIPT_FILE_PATH    "script.asc"

#define U2D_DEV_NAME0       "/dev/ttyUSB0"
#define U2D_DEV_NAME1       "/dev/ttyUSB1"

using namespace Robot;
using namespace std;

std::string ADDRESS = "192.168.0.102";
#define PORT				20000
#define COMMANDLENGTH       8

LinuxCM730 linux_cm730(U2D_DEV_NAME0);
CM730 cm730(&linux_cm730);

minIni* ini;
//Image* RgbOutput;
ColorFinder* BallFinder;
BallTracker* Tracker;

void ChangeCurrentDir();
void sighandler(int sig);

int Initialize();
void OpenCamera();
void CloseCamera();
void InitLivePreview();
void EndLivePreview();

int WX = 0, WA = 0;

int main(void)
{
    signal(SIGABRT, &sighandler);
    signal(SIGTERM, &sighandler);
    signal(SIGQUIT, &sighandler);
    signal(SIGINT, &sighandler);

    ChangeCurrentDir();	
    Initialize();
	//OpenCamera();
	for(int i=0; i<10; i++)
		LinuxCamera::GetInstance()->CaptureFrame();	
	CloseCamera();
	/////
	LinuxSocket client;
	client.create();
	client.set_non_blocking(true);
	
	// Bucle principal
	int Cont = 0;
	int ContLoses = 0; 
	bool PreviewEnable = false;
	bool FistEnable = false;
	int FistJoint = 0;
	int FistPosition = 0;
	bool WalkingEnable = false;
	bool PageRunningRequest = false;
	usleep(1000*1000);
	//OpenCamera();
	for(int i=0; i<10; i++)
		LinuxCamera::GetInstance()->CaptureFrame();	
	CloseCamera();	

	while(1)
	{
		Cont++;		
		if(client.connect(ADDRESS, PORT))		
		{			
			printf("Conexion establecida con %s. Port %d\n", ADDRESS.c_str(), PORT);	
			bool Connected = true;
			while(Connected)
			{	
				char Command[COMMANDLENGTH];		
				std::cout.setstate(std::ios_base::failbit);									
				int Len = client.recv(Command, COMMANDLENGTH);
				//printf("%d %s\n", Len, Command);
				usleep(1*1000);	
				if(Len > 0)
				{
					// LivePreview					
					if(!strncmp(Command, "LP", 2))					
					{
						InitLivePreview();
						printf("Iniciando LivePreview\n");
						PreviewEnable = true;
					}
					// EndLivePreview
					else if(!strncmp(Command, "EP", 2))					
					{
						if(PreviewEnable)
						{
							EndLivePreview();
							PreviewEnable = false;
							printf("Finalizando LivePreview\n");
						}
					}
					// LEDS
					else if(!strncmp(Command, "LD", 2))
					{
						unsigned char r = Command[5];
						unsigned char g = Command[6];
						unsigned char b = Command[7];
						if(Command[2] == 'E')
						{
							cm730.WriteWord(CM730::P_LED_EYE_L, cm730.MakeColor(r, g, b), NULL);
							printf("Cambiando color de ojos (%d, %d, %d)\n", r, g, b);
						}
						else
						{
							cm730.WriteWord(CM730::P_LED_HEAD_L, cm730.MakeColor(r, g, b), NULL);
							printf("Cambiando color de cara (%d, %d, %d)\n", r, g, b);
						}
					}
					// Posar 
					else if(!strncmp(Command, "PS", 2))
					{
						char pose[2];
						pose[0] = Command[3];
						pose[1] = Command[4];
						pose[2] = Command[5];
						int posePage = atoi(pose);
						Action::GetInstance()->m_Joint.SetEnableBody(true, true);
    					MotionManager::GetInstance()->SetEnable(true);
						Action::GetInstance()->Start(posePage);
						printf("Ejecutando Pose (%c) %d\n", Command[2], posePage);
						if(Command[2] == 'Y')
						{
							PageRunningRequest = true;													
						}
					}
					// Puño
					else if(!strncmp(Command, "FI", 2))
					{
						FistJoint = JointData::ID_R_ELBOW;
						if(Command[2] == 'L')
							FistJoint = JointData::ID_L_ELBOW;
    					MotionManager::GetInstance()->SetEnable(false);
						
						while(cm730.WriteWord(FistJoint, MX28::P_TORQUE_ENABLE, 0, 0) != CM730::SUCCESS);
						while(cm730.ReadWord(FistJoint, MX28::P_PRESENT_POSITION_L, &FistPosition, 0) != CM730::SUCCESS);						
						printf("Ejecutando Puño %c (%d)\n", Command[2], FistPosition);
						FistEnable = true;
					}
					// Orientar Mirada
					else if(!strncmp(Command, "LA", 2))
					{
						char pans[3], tilts[3];
						pans[0] = Command[3];
						pans[1] = Command[4];
						pans[2] = NULL;
						int pan = atoi(pans);
						if(Command[2] == '-')
							pan *= -1;						
						tilts[0] = Command[6];
						tilts[1] = Command[7];
						tilts[2] = NULL;
						int tilt = atoi(tilts);
						if(Command[5] == '-')
							tilt *= -1;																		
						printf("Ejecutando LookAt: (%d, %d) \n", pan, tilt);
						Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
						Head::GetInstance()->MoveByAngle(pan, tilt);						
					}
					// Seguir punto 
					else if(!strncmp(Command, "TA", 2))
					{
						char xs[4], ys[4];
						xs[0] = Command[2];
						xs[1] = Command[3];
						xs[2] = Command[4];
						xs[3] = NULL;
						int x = atoi(xs);
						ys[0] = Command[5];
						ys[1] = Command[6];
						ys[2] = Command[7];
						ys[3] = NULL;
						int y = atoi(ys);
						printf("Ejecutando TrackPoint: (%d, %d) \n", x, y);
						Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
						Tracker->Process(Point2D(x, y));
					}
					// Configuracion de caminata
					else if(!strncmp(Command, "WS", 2))
					{
						char xs[4], as[4];
						xs[0] = Command[2];
						xs[1] = Command[3];
						xs[2] = Command[4];
						xs[3] = NULL;
						WX = atoi(xs);
						as[0] = Command[5];
						as[1] = Command[6];
						as[2] = Command[7];
						as[3] = NULL;
						WA = atoi(as);						
						Walking::GetInstance()->X_MOVE_AMPLITUDE = WX;
						Walking::GetInstance()->A_MOVE_AMPLITUDE = WA;
						printf("Ejecutando WalkingSettings: (X = %d, A = %d) \n", WX, WA);						
					}
					// Caminata por tiempo
					else if(!strncmp(Command, "WT", 2))
					{
						char ts[3];
						ts[0] = Command[6];
						ts[1] = Command[7];
						ts[2] = NULL;
						int t = atoi(ts);

						Action::GetInstance()->m_Joint.SetEnableBody(true, true);
						MotionManager::GetInstance()->SetEnable(true);
						Action::GetInstance()->Start(9);
						while(Action::GetInstance()->IsRunning()) 
							usleep(8*1000);

						Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
                		Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
						printf("Ejecutando WalkingTime: (T = %d) \n", t);						
						Walking::GetInstance()->Start();
						usleep(t*1000*1000);
						Walking::GetInstance()->Stop();
					}
					// Inicio de caminata indefinida
					else if(!strncmp(Command, "WI", 2))
					{
						Action::GetInstance()->m_Joint.SetEnableBody(true, true);
						MotionManager::GetInstance()->SetEnable(true);
						Action::GetInstance()->Start(9);
						while(Action::GetInstance()->IsRunning()) 
							usleep(8*1000);

						Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
                		Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
						Walking::GetInstance()->X_MOVE_AMPLITUDE = WX;
						Walking::GetInstance()->A_MOVE_AMPLITUDE = WA;	
						Walking::GetInstance()->Start();
						printf("Ejecutando WalkingStart\n");
						WalkingEnable = true;
					}
					// Fin Caminata
					else if(!strncmp(Command, "WP", 2))
					{
						Walking::GetInstance()->Stop();
						printf("Ejecutando WalkingStop\n");
						WalkingEnable = false;
					}
					// HeadTracking
					else if(!strncmp(Command, "HT", 2))
					{
						if(Command[2] == 'I')
						{
							//delete LinuxCamera::GetInstance();							
							/*LinuxCamera::GetInstance()->Initialize(0);
    						LinuxCamera::GetInstance()->SetCameraSettings(CameraSettings());
							LinuxCamera::GetInstance()->LoadINISettings(ini);*/
							//Initialize();
							/*BallFinder = new ColorFinder();
							BallFinder->LoadINISettings(ini);
							Tracker = new BallTracker();
							
							Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
							Head::GetInstance()->m_Joint.SetPGain(JointData::ID_HEAD_PAN, 8);
							Head::GetInstance()->m_Joint.SetPGain(JointData::ID_HEAD_TILT, 8);*/
							//Initialize();							
							usleep(5*1000*1000);
							printf("Camara Lista\n");
							while(true)
							{														
								LinuxCamera::GetInstance()->CaptureFrame();	
						        //Tracker->Process(BallFinder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame));
							}
						}
						else
						{
							
						}
					}
				}
				if(FistEnable)
				{
					int value;
					if(cm730.ReadWord(FistJoint, MX28::P_PRESENT_POSITION_L, &value, 0) == CM730::SUCCESS)
					{
						if(abs(value-FistPosition) > 50)
						{
							printf("Me dieron puño (%d)\n", value);
							client.send((void*)("FIOK____"), COMMANDLENGTH);
							MotionManager::GetInstance()->SetEnable(true);
							FistEnable = false;
						}
					}
				}
				if(WalkingEnable)
				{
					if(MotionStatus::FALLEN != STANDUP)
					{
						Walking::GetInstance()->Stop();
						while(Walking::GetInstance()->IsRunning() == 1) 
							usleep(8000);

						Action::GetInstance()->m_Joint.SetEnableBody(true, true);

						if(MotionStatus::FALLEN == FORWARD)
							Action::GetInstance()->Start(10);   // FORWARD GETUP
						else if(MotionStatus::FALLEN == BACKWARD)
							Action::GetInstance()->Start(11);   // BACKWARD GETUP

						while(Action::GetInstance()->IsRunning() == 1) 
							usleep(8000);

						Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
						Walking::GetInstance()->m_Joint.SetEnableBodyWithoutHead(true, true);
						Walking::GetInstance()->X_MOVE_AMPLITUDE = WX;
						Walking::GetInstance()->A_MOVE_AMPLITUDE = WA;						
						Walking::GetInstance()->Start();
					}
				}
				if(PageRunningRequest)
				{
					if(!Action::GetInstance()->IsRunning()) 
					{
						printf("Enviando confirmacion de fin de pose \n");	
						client.send((void*)("Ready___"), COMMANDLENGTH);					
						PageRunningRequest = false;
					}
				}
				if(client.send((void*)("CT______"), COMMANDLENGTH))
					ContLoses = 0;
				else
					ContLoses++;
					
				if(ContLoses >= 10)
				{
					if(PreviewEnable)
					{
						EndLivePreview();
						printf("Finalizando LivePreview\n");
					}
					printf("Cerrando conexion\n");
					return 1;
				}
			}	
		}
		else
		{
			printf("Conexion rechazada [%d], reconectando en 1 seg \n", Cont);
			usleep(1000*1000);
			if(Cont >= 10)
				return 1;
		}
	}
	return 0;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////
void ChangeCurrentDir()
{
    char exepath[1024] = {0};
    if(readlink("/proc/self/exe", exepath, sizeof(exepath)) != -1)
    {
        if(chdir(dirname(exepath)))
            fprintf(stderr, "chdir error!! \n");
    }
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////
void sighandler(int sig)
{
    exit(0);
}

int Initialize()
{
	ini = new minIni(INI_FILE_PATH);
    //RgbOutput = new Image(Camera::WIDTH, Camera::HEIGHT, Image::RGB_PIXEL_SIZE);

	LinuxCamera::GetInstance()->Initialize(0);
    LinuxCamera::GetInstance()->SetCameraSettings(CameraSettings());    // set default
    LinuxCamera::GetInstance()->LoadINISettings(ini);                   // load from ini

	//LinuxCamera::GetInstance()->SetAutoWhiteBalance(true);

    //Streamer = new mjpg_streamer(Camera::WIDTH, Camera::HEIGHT);

    BallFinder = new ColorFinder();
    BallFinder->LoadINISettings(ini);

	Tracker = new BallTracker();
						
    //httpd::ball_finder = ball_finder;*/

    //BallFollower Follower = BallFollower();

    /*ColorFinder* red_finder = new ColorFinder(0, 15, 45, 0, 0.3, 50.0);
    red_finder->LoadINISettings(ini, "RED");
    httpd::red_finder = red_finder;

    ColorFinder* yellow_finder = new ColorFinder(60, 15, 45, 0, 0.3, 50.0);
    yellow_finder->LoadINISettings(ini, "YELLOW");
    httpd::yellow_finder = yellow_finder;

    ColorFinder* blue_finder = new ColorFinder(225, 15, 45, 0, 0.3, 50.0);
    blue_finder->LoadINISettings(ini, "BLUE");
    httpd::blue_finder = blue_finder;*/

    //httpd::ini = ini;
	//if(mode != 'R')
	{
		//////////////////// Framework Initialize ////////////////////////////
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
		{
		    exit(0);
		}
	}
    Action::GetInstance()->m_Joint.SetEnableBody(true, true);
    MotionManager::GetInstance()->SetEnable(true);
	// Control de LEDS
    cm730.WriteByte(CM730::P_LED_PANNEL, 0x01|0x02|0x04, NULL);
	cm730.WriteWord(CM730::P_LED_HEAD_L, cm730.MakeColor(0, 0, 0), NULL);
	cm730.WriteWord(CM730::P_LED_EYE_L, cm730.MakeColor(0, 0, 0), NULL);
	// Mensaje de confirmación de inicializacion y Postura inicial	  -v es-la -p 75 -s 190 -a 80
	LinuxActionScript::PlayMP3("../../../Data/mp3/HolaBanco.mp3");
    
	Action::GetInstance()->Start(15); // 7
    while(Action::GetInstance()->IsRunning()) 
		usleep(8*1000);
	usleep(2*1000*1000);		

	return 1;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////
void OpenCamera()
{
	LinuxCamera::GetInstance()->Initialize(0);
    LinuxCamera::GetInstance()->SetCameraSettings(CameraSettings());    // set default
    LinuxCamera::GetInstance()->LoadINISettings(ini);                   // load from ini
	//LinuxCamera::GetInstance()->SetAutoWhiteBalance(true);
}

void CloseCamera()
{
	LinuxCamera::GetInstance()->~LinuxCamera();
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////
void InitLivePreview()
{
	system("guvcview &");
	usleep(1000*1000);
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////
void EndLivePreview()
{
	std::string cmd("pgrep -f guvcview");
	std::string pattern("\n");
	std::string data;

    FILE * stream;
    const int max_buffer = 256;
    char buffer[max_buffer];
    cmd.append(" 2>&1");

    stream = popen(cmd.c_str(), "r");
    if (stream) 
	{
    	while (!feof(stream))
	    if (fgets(buffer, max_buffer, stream) != NULL) 
			data.append(buffer);
	    pclose(stream);
    }
	int ind = static_cast<int>(data.find_first_of(pattern));
	std::string PID = data.substr(0, ind);
	std::string killcmd = "kill -9 " + PID;
	system(std::string("kill -9 " + PID + " &").c_str());
}


