import cv2
import face_recognition

def resize_image(img):
	scale = 500/img.shape[0]

	width = int(img.shape[1] * scale)
	height = int(img.shape[0] * scale)
	dim = (width, height)
	# resize image
	resized = cv2.resize(img, dim, interpolation = cv2.INTER_CUBIC)
	return resized
 
known_image = face_recognition.load_image_file('C:\\Users\\Leslie\\Desktop\\Leslie\\DigitalIdentity\\obama1.jpg')
known_image = cv2.cvtColor(known_image,cv2.COLOR_BGR2RGB)

unknown_image = face_recognition.load_image_file('C:\\Users\\Leslie\\Desktop\\Leslie\\DigitalIdentity\\musk2.jpg')
unknown_image = cv2.cvtColor(unknown_image,cv2.COLOR_BGR2RGB)
 
known_face_locations = face_recognition.face_locations(known_image)[0]
known_encoding = face_recognition.face_encodings(known_image)[0]
cv2.rectangle(known_image,(known_face_locations[3],known_face_locations[0]),(known_face_locations[1],known_face_locations[2]),(255,0,255),2)
 
unknown_face_locations = face_recognition.face_locations(unknown_image)[0]
unknown_encodings = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([known_encoding],unknown_encodings, tolerance = 0.5)
face_distance = face_recognition.face_distance([known_encoding],unknown_encodings)
print(results,face_distance)
#cv2.putText(unknown_image,f'{results} {round(face_distance[0],2)}',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
test_result	= None
color = None

if results[0] == True:
	test_result = "PASS"
	color = (0,200,0)
else:
	test_result = "FAIL"
	color = (0,0,200)

cv2.rectangle(unknown_image,(unknown_face_locations[3],unknown_face_locations[2]),(unknown_face_locations[1],unknown_face_locations[2]+20),color,cv2.FILLED)
cv2.rectangle(unknown_image,(unknown_face_locations[3],unknown_face_locations[0]),(unknown_face_locations[1],unknown_face_locations[2]+20),color,2)
cv2.putText(unknown_image,test_result,(unknown_face_locations[3]+5,unknown_face_locations[2]+15),cv2.FONT_HERSHEY_COMPLEX,0.45,(250,250,250),1)

  
cv2.imshow('Reference Image',known_image)
cv2.imshow('Test Image',unknown_image)
cv2.waitKey(0)