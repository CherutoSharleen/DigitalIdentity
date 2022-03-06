import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
# To install this module, run:
# python -m pip install Pillow
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition
import matplotlib.pyplot as plt

# This key will serve all examples in this document.
KEY = "5d7dba6e3b714344b44a2394ee2fb2e3"

# This endpoint will be used in all examples in this quickstart.
ENDPOINT = "https://phoenixfacerecognition.cognitiveservices.azure.com/"

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# Base url for the Verify and Facelist/Large Facelist operations
IMAGE_BASE_URL = 'Samples\\'

# The source photos contain this person
source_image_file_path = 'Samples\\african1.jpg'
target_image_file_path = 'Samples\\african2.jpg'

source_image = open(source_image_file_path, "rb")
target_image = open(target_image_file_path, "rb")

# Detect face(s) from source image 1, returns a list[DetectedFaces]
# We use detection model 3 to get better performance.
source_detected_faces = face_client.face.detect_with_stream(source_image, detection_model='detection_03')
# Add the returned face's face ID
source_image_id = source_detected_faces[0].face_id
print('{} face(s) detected from image {}.'.format(len(source_detected_faces), source_image_file_path))

# Detect face(s) from source image 2, returns a list[DetectedFaces]
target_detected_faces = face_client.face.detect_with_stream(target_image, detection_model='detection_03')
# Add the returned face's face ID
target_image_id = target_detected_faces[0].face_id
print('{} face(s) detected from image {}.'.format(len(target_detected_faces), target_image_file_path))


# Verification example for faces of the same person. The higher the confidence, the more identical the faces in the images are.
# Since target faces are the same person, in this example, we can use the 1st ID in the detected_faces_ids list to compare.
verify_result_same = face_client.face.verify_face_to_face(source_image_id, target_image_id)
print('Faces from {} & {} are of the same person, with confidence: {}'
    .format(source_image_file_path, target_image_file_path, verify_result_same.confidence)
    if verify_result_same.is_identical
    else 'Faces from {} & {} are of a different person, with confidence: {}'
        .format(source_image_file_path, target_image_file_path, verify_result_same.confidence))

if verify_result_same.is_identical:
	print("PASSED")
else:
	print("FAILED")