import os
import cv2
import numpy as np 
from PIL import Image

recognizer = cv2.createLBPHFaceRecognizer();
path = 'dataset';

def getImageID(path):
 	imagePath = [os.path.join(path,f) for f in os.listdir(path)]
 	faces = []
 	IDs = []
 	for image in imagePath[1:]:
 		face = Image.open(image).convert('L');
 		faceNp = np.array(face,'uint8');
 		ID = int(os.path.split(image)[-1].split('.')[0]);
 		print(ID)
 		faces.append(faceNp)
 		IDs.append(ID)
 		cv2.imshow("trainer", faceNp)
 		cv2.waitKey(10)
 	return np.array(IDs),faces

IDs, faces = getImageID(path)
recognizer.train(faces,IDs)

recognizer.save('Recognizer/trainingData.yml')
cv2.destroyAllWindows();




