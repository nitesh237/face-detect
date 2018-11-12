import cv2
import numpy as np 
import os
from PIL import Image
import sqlite3

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam = cv2.VideoCapture(0); 

def fun(id1, name, roll, sem, sex):
	conn = sqlite3.connect("FaceDatabase.db")
	cmd = "SELECT Id FROM Students"
	cursor = conn.execute(cmd)
	flag = 0;
	for row in cursor:
		if(int(id1) == row[0]):
			flag = 1;
			break;
	if(flag == 0):
		cmd = "INSERT INTO Students VALUES (" + str(id1) + ",'" + str(name) + "','" +str(roll)+ "'," +str(sem)+ ",'" +str(sex)+ "')"
 		conn.execute(cmd)
	conn.commit()
	conn.close()

id = raw_input('Enter user id: ');
name = raw_input('Enter name: ');
#roll = raw_input('Enter Roll: ');
#sem = raw_input('Enter Semester: ');
#sex = raw_input('Enter Sex: ');
path = 'dataset'
#fun(id, name, roll, sem, sex)
flag = 0;
imagePath = [os.path.join(path,f) for f in os.listdir(path)]
ID = 0;
for image in imagePath:
 if(os.path.split(image)[-1].split('.')[0] == id):
 	if(os.path.split(image)[-1].split('.')[1] == 'unknown'):
 		num = os.path.split(image)[-1].split('.')[2];
		os.rename(image, "dataset/"+str(int(id)+1)+'.unknown.'+ str(num) +'.jpg');
 		flag = 1;
 	ID = ID+1;
 	print(image)
 	cv2.waitKey(10)

sample = ID;	
c=sample+10;

if(flag == 1):
	c = 10;
	sample = 0;


while(True):
	ret,img = cam.read();
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY);
	faces = faceDetect.detectMultiScale(gray, 1.3, 5);
	
	for(x, y, w, h) in faces:
		cv2.rectangle(img, (x, y), (x+w,y+h), (0,255,0), 2);
	
	cv2.imshow("Check. Press s to start", img);
	if(cv2.waitKey(1) == ord('s')):
		break;


while(True):
	ret,img = cam.read();
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY);
	faces = faceDetect.detectMultiScale(gray, 1.3, 5);
	
	for(x, y, w, h) in faces:
		cv2.imwrite("dataset/"+str(id)+"."+name+"."+str(sample)+".jpg", gray[y:y+h,x:x+w]);
		sample = sample + 1;
		cv2.rectangle(img, (x, y), (x+w,y+h), (0,255,0), 2);
		cv2.waitKey(10);
	cv2.imshow("stuff", img);
	if(sample >= c):
		break;
cam.release();
cv2.destroyAllWindows();