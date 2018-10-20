#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
from person import Person
from person import Less_Blurred
from edit_files import Group

class Characterization:
    def __init__(self):
        self.persons = Person()
        self.blurry = Less_Blurred()  
        
    def get_persons(self):
        personsList = self.persons.persons_in_group()
        for p in personsList:
            print(p)
        return personsList 
    
    def add_person(self, name):
        cap = cv2.VideoCapture(0)
        images = {}
        for i in range(20):
            ret, frame = cap.read()
            frame = cv2.GaussianBlur(frame,(5,5),0)
            images[i] = frame
        cap.release()
        self.blurry.sort_less_blurred(images)
        self.persons.enrol(name,self.blurry.frames)
    
    def delete_person(self, name):
        self.persons.delete_person_by_name(name)
        
    def indentify_person(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        frame = cv2.GaussianBlur(frame,(5,5),0)
        cap.release()
        self.persons.identifyPerson(frame)   
        pi = (self.persons.bb['left'],self.persons.bb['top'])
        pf = (self.persons.bb['left']+self.persons.bb['width'],self.persons.bb['top']+self.persons.bb['height'])
        cv2.rectangle(frame,pi,pf,(0,255,0),3)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,self.persons.name,pi, font, 1,(255,0,0),2,cv2.LINE_AA)
        cv2.imshow('image',frame)
        print("Press Enter to Exit")
        cv2.waitKey(0)
    
    def get_persons_attributes(self):
        G = Group()    
        for p in G.persons:
            print(p)
        return G.persons

#####Pruebas
C = Characterization()
C.indentify_person()
#C.get_persons_attributes()
#C.get_persons()
#C.delete_person('name')
#C.add_person('Julian Rojas')