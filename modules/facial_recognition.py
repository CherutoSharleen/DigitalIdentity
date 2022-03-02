import cv2
import face_recognition
 
known_image = face_recognition.load_image_file('musk1.jpg')
known_image = cv2.cvtColor(known_image,cv2.COLOR_BGR2RGB)

unknown_image = face_recognition.load_image_file('musk2.jpg')
unknown_image = cv2.cvtColor(unknown_image,cv2.COLOR_BGR2RGB)
 
known_face_locations = face_recognition.face_locations(known_image)[0]
known_encoding = face_recognition.face_encodings(known_image)[0]
cv2.rectangle(known_image,(known_face_locations[3],known_face_locations[0]),(known_face_locations[1],known_face_locations[2]),(255,0,255),2)
 
unknown_face_locations = face_recognition.face_locations(unknown_image)[0]
unknown_encodings = face_recognition.face_encodings(unknown_image)[0]
cv2.rectangle(unknown_image,(unknown_face_locations[3],unknown_face_locations[0]),(unknown_face_locations[1],unknown_face_locations[2]),(255,0,255),2)
 
results = face_recognition.compare_faces([known_encoding],unknown_encodings, tolerance = 0.5)
face_distance = face_recognition.face_distance([known_encoding],unknown_encodings)
print(results,face_distance)
cv2.putText(unknown_image,f'{results} {round(face_distance[0],2)}',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
 
cv2.imshow('Elon Musk',known_image)
cv2.imshow('Elon Test',unknown_image)
cv2.waitKey(0)