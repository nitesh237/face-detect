from flask import Flask, render_template, request
app = Flask(__name__)
import cv2
import numpy as np 
import os
import sqlite3
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam = cv2.VideoCapture(0); 
rec = cv2.cv.createLBPHFaceRecognizer();
rec.load('Recognizer/trainingData.yml')
def SetFlag():
	flag = {}
	conn = sqlite3.connect('FaceDatabase.db')
	cmd = "SELECT Id FROM Students"
	cursor = conn.execute(cmd)
	for row in cursor:
		flag[str(row[0])] = 0;
	return flag

def getSubid(subject):
	conn = sqlite3.connect('FaceDatabase.db')
	cmd = "SELECT Id FROM Subjects WHERE Name = '" + str(subject) + "'"
	cursor = conn.execute(cmd)
	for row in cursor:
		return row[0]
def getAttendance(id, subject):
	id1 = ""
	conn = sqlite3.connect('FaceDatabase.db')
	cmd = "SELECT Roll FROM Students WHERE Id =" + str(id)
	cursor = conn.execute(cmd)
	for row in cursor:
		id1 = row[0]
	cmd = "SELECT Name FROM Subjects WHERE Id = " + str(subject)
	cursor = conn.execute(cmd)
	for row in cursor:
		cmd = "UPDATE " + str(row[0]) + " SET Attendance = Attendance + 1 WHERE Id =" + str(id1)
	conn.execute(cmd)
	conn.commit()
	conn.close()

def getName(id):
	conn = sqlite3.connect('FaceDatabase.db')
	cmd = "SELECT Name FROM Students WHERE Id =" + str(id)
	cursor = conn.execute(cmd)
	for row in cursor:
		profile = row[0]
	return profile

def check(id, subject):
	conn = sqlite3.connect('FaceDatabase.db')
	cmd = "SELECT Sub_id FROM Studies WHERE Stud_id =" + str(id)
	cursor = conn.execute(cmd)
	for row in cursor:
		if(row[0] == subject):			
			return 1
	return -1

@app.route('/')
def student():
	print('here')
   	return render_template('./student.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
	print('here1')
	if request.method == 'POST':
		print('wohoo!!')
	subject = request.form.getlist('subject')
	print(subject[0])
	sub = getSubid(subject[0])
	print(sub)
		
	font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL,3,1,0,2)
	id = 0;
	path = 'dataset'
	imagePath = [os.path.join(path,f) for f in os.listdir(path)]
	ID = 0;
	flag = SetFlag()
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
			cv2.rectangle(img, (x, y), (x+w,y+h), (0,255,0), 2);
			id, conf = rec.predict(gray[y:y+h,x:x+w])
			chk = check(id, sub)
			print(chk)
			if(check == 1):
				if(flag[str(id)] < 10):
					flag[str(id)] = flag[str(id)] + 1;
					cv2.cv.PutText(cv2.cv.fromarray(img),str(flag[str(id)]),(x,y+h+50),font,0);
				if(flag[str(id)] == 10):
					getAttendance(id, sub, 0)
					cv2.cv.PutText(cv2.cv.fromarray(img),"PRESENT",(x,y+h+50),font,0);
					flag[str(id)] = flag[str(id)] + 1;
				if(flag[str(id)] == 11):
					cv2.cv.PutText(cv2.cv.fromarray(img),"PRESENT",(x,y+h+50),font,0);
				cv2.cv.PutText(cv2.cv.fromarray(img),str(id)+str(getName(id)),(x,y+h),font,0);
			else:
				cv2.cv.PutText(cv2.cv.fromarray(img),"UNKNOWN",(x,y+h),font,0);
		cv2.imshow("stuff", img);
		if(cv2.waitKey(1) == ord('q')):
			break;
	cam.release();
	cv2.destroyAllWindows();
	return 'success'
@app.route('/success')
def success():
   return 'logged in successfully'

if __name__ == '__main__':
   app.run(debug = True)