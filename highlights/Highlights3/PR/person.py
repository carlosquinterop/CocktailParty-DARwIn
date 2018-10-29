from azure import Azure
import cv2
import os, sys
import queue as qe
from edit_files import Group
from edit_files import PersonFiles

class Person:

    def __init__(self):
        self.ROOT_PATH = os.path.dirname(sys.modules['__main__'].__file__)
        self.azureService = Azure()
        self.codeError = 0
        self.gotAttributes = False
        self.frame = None
        self.framesTrain = None
        self.bb_service = []
        # self.service = None
        self.name = "desconocido"
        self.id_debug = None
        self.faceId = ""
        self.accuracy = None
        self.age = 0#
        self.gender = ""#male-female
        self.smile = 0 #0-1
        self.pose = {} #dict pitch, roll, yaw (double)
        self.emotion = None #anger, contempt, disgust, fear, happiness, neutral, sadness, surprise
        self.beard = 0 #0-1
        self.glasses = ""#eyeglasses - noglasses
        self.eyesOpen = 0
        self.mouthOpen = 0
        self.bald = 0 #número
        self.hairColor = ""#brown, blond, red, gray, other, black
        self.sideburns = 0#0-1
        self.eyeMakeUp = False#true-false
        self.lipMakeUp = False#true-false
        self.headWear = 0#0-1
        self.mask = 0
        self.mustache = 0#0-1

        self.bb_actual = []
        self.image_actual = None
        self.imageBBPair = ([], None)
        self.happiness = 0
        self.sadness = 0
        self.neutral = 0
        self.surprise = 0
        self.anger = 0

        self.table = 0
        self.country = ""
        self.id = ""
        self.id_azure = ""
        self.interaction = 0

        self.lastInteractionTime = 0
        self.G = Group()

        self.bb = []




    def frame2bytes(self, frame):
        retval, encoded_image = cv2.imencode('.png', frame)
        return encoded_image.tobytes()

    def check_img(self, frame):
        if type(frame) != bytes:
            return self.frame2bytes(frame)
        else:
            return frame

    def enrol(self, id, frames):
        person_id, self.codeError = self.azureService.create_person(id)
        success_list = []
        if person_id is not None:
            self.id_azure = person_id
            #print('enrol'+str(len(frames)))
            for frame in frames:
                imgBytes = self.check_img(frame)
                successEnrol, self.codeError = self.azureService.add_face(imgBytes, person_id, frame)
                success_list.append(successEnrol)
            if self.azureService.attributes:
                for key, value in self.azureService.attributes.items():
                    setattr(self, key, value)
                self.G.add(PersonFiles(id, person_id, self.hairColor, self.glasses, self.gender, self.age, self.smile, self.pose, self.emotion,
                    self.beard, self.eyesOpen, self.mouthOpen, self.bald, self.sideburns, self.eyeMakeUp, self.lipMakeUp, self.headWear,
                    self.mask, self.mustache))
            self.azureService.train()
        return success_list.count(True)

    def identify(self, frame):
        self.reset_attributes()
        self.frame = frame
        imgBytes = self.check_img(frame)
        attributes, self.codeError = self.azureService.identify(imgBytes)
        if attributes:
            for key, value in attributes.items():
                setattr(self, key, value)
            self.gotAttributes = True
            return True
        else:
            self.reset_attributes()
            return False

    def identifyPerson(self, frame):
        personsList = self.persons_in_group()
        isIdentified = self.identify(frame)
        if isIdentified:
            for person in personsList:
                if person['personId'] == self.id_azure:
                    self.name = person['name']
                    print('Person Identified: {}'.format(self.name))
                    break
        else:
            print('The person was not identified !!')


    def delete_person_by_name(self,name):
        deleted = False
        personsList, self.codeError = self.azureService.get_all_names()
        for person in personsList:
            if person['name'] == name:
                self.azureService.delete_person(person['personId'])
                deleted = True
                print('Person: {} Deleted !!'.format(name))
                self.G.delete(name)
                break
        if not deleted:
            print('Person: {} Not Found !!'.format(name))

    def persons_in_group(self):
        personsList, self.codeError = self.azureService.get_all_names()
        return personsList

    def reset_attributes(self):
        attrNoEdit = ['azureService', 'debug', 'ROOT_PATH', 'db_handler', 'information']
        for attr in dir(self):
            if not callable(getattr(self, attr)) and not attr.startswith("__") and attr not in attrNoEdit:
                if attr == 'name':
                    setattr(self, attr, "desconocido")
                else:
                    if type(getattr(self, attr)) == int:
                        setattr(self, attr, 0)
                    elif type(getattr(self, attr)) == str:
                        setattr(self, attr, "")
                    elif type(getattr(self, attr)) == bool:
                        setattr(self, attr, False)
                    elif type(getattr(self, attr)) == dict:
                        setattr(self, attr, {})
                    elif type(getattr(self, attr)) == tuple:
                        setattr(self, attr, ([], None))
                    else:
                        setattr(self, attr, None)

class Less_Blurred:
    def __init__(self):
        self.nImages = 5
        self.fm = qe.PriorityQueue(100);
        self.frames = []
    def sort_less_blurred(self, images):
        self.frames = []
        if type(images) == dict:
            for imgID in images:
                self.fm.put((1/cv2.Laplacian(images[imgID], cv2.CV_64F).var(),imgID))
            for i in range(self.nImages):
                dat = self.fm.get()
                nIma = dat[1]
                self.frames.append(images[nIma])
        else:
            print('review images type')
        #print(len(self.frames))
