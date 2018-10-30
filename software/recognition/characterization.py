#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
from person import Person
from person import Less_Blurred
from edit_files import Group
import time

class Characterization:
    def __init__(self):
        self.persons = Person()
        self.blurry = Less_Blurred()

    def get_persons(self):
        G = Group()
        personsList = G.persons
        return personsList
        # personsList = self.persons.persons_in_group()
        # # for p in personsList:
        # #     print(p)
        # return personsList

    def add_person(self, name, capture):
        G = Group()
        personsList = G.persons
        add = False
        for i in range(len(personsList)):
            if(G.persons[i].name == name):
                print('Person already added')
                add = True
                break
        if not add:
            #cap = cv2.VideoCapture(0)
            cap = capture
            images = {}
            print('Tomando fotos')
            for i in range(5):
                ret, frame = cap.read()
            for i in range(20):
                #print('FOTO: '+str(i))
                ret, frame = cap.read()
                frame = frame[115:600, 320:960]
                frame = cv2.flip(frame,0)
                frame = cv2.flip(frame,1)
                # cv2.imshow('image',frame)
                # print("Press Enter to Exit")
                # cv2.waitKey(0)
                time.sleep(0.3)
                frame = cv2.GaussianBlur(frame,(5,5),0)
                images[i] = frame
            #cap.release()
            self.blurry.sort_less_blurred(images)
            self.persons.enrol(name,self.blurry.frames)
            return 1
        return 0

    def delete_person(self, name):
        self.persons.delete_person_by_name(name)

    def identify_person(self, capture):
        aux = True
        while (aux):
            #cap = cv2.VideoCapture(0)
            cap = capture
            ret, frame = cap.read()
            frame = cv2.flip(frame,0)
            frame = cv2.flip(frame,1)
            frame = cv2.GaussianBlur(frame,(5,5),0)
            #cap.release()
            self.persons.identifyPerson(frame)
            if (self.persons.bb != None):
                aux = False
        return self.persons.name
        # pi = (self.persons.bb['left'],self.persons.bb['top'])
        # pf = (self.persons.bb['left']+self.persons.bb['width'],self.persons.bb['top']+self.persons.bb['height'])
        # cv2.rectangle(frame,pi,pf,(0,255,0),3)
        # font = cv2.FONT_HERSHEY_SIMPLEX
        # cv2.putText(frame,self.persons.name,pi, font, 1,(255,0,0),2,cv2.LINE_AA)
        #cv2.imshow('image',frame)
        #print("Press Enter to Exit")
        #cv2.waitKey(0)


    def get_persons_attributes(self):
        G = Group()
        for p in G.persons:
            print(p)
        return G.persons

    def get_person_attribute(self, name):
        G = Group()
        personsList = G.persons
        id = -1
        for i in range(len(personsList)):
            if(G.persons[i].name == name):
                id = i
                break
        if (id==-1):
            print('Person not recognized')
            return {}
        else:
            attributes = {'age':G.persons[id].age, 'gender':G.persons[id].gender, 'smile':G.persons[id].smile, 'glasses':G.persons[id].glasses, \
                        'bald':G.persons[id].bald, 'hairColor':G.persons[id].hairColor, 'eyeMakeUp':G.persons[id].eyeMakeUp, 'lipMakeUp':G.persons[id].lipMakeUp, \
                        'headWear':G.persons[id].headWear, 'mustache':G.persons[id].mustache, 'beard':G.persons[id].beard}
            return attributes

    def delete_all_person(self):
        G = Group()
        personsList = G.persons
        for i in range(len(personsList)):
            self.delete_person(G.persons[i].name)
        ids = self.persons.azureService.get_all_names()
        for person in ids[0]:
            self.persons.azureService.delete_person(person['personId'])





#####Pruebas
#C = Characterization()
#C.identify_person()
#C.get_persons_attributes()
#C.get_persons()
#C.delete_person('name')
#C.add_person('Fabian_P')
