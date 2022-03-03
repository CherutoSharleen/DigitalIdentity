#IMPORT SYSTEM FILES
import argparse
import scipy.io.wavfile as wavfile
import traceback as tb
import os
import sys
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist, euclidean, cosine 
import warnings
from tensorflow.keras.models import load_model
import logging
logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore")
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # FATAL
logging.getLogger('tensorflow').setLevel(logging.FATAL)
#IMPORT USER-DEFINED FUNCTIONS
from feature_extraction import get_embedding, get_embeddings_from_list_file
from preprocess import get_fft_spectrum
import parameters as p

def enroll(name,file):
    """Enroll a user with an audio file
        inputs: str (Name of the person to be enrolled and registered)
                str (Path to the audio file of the person to enroll)
        outputs: None"""

    print("Loading model weights from [{}]....".format(p.MODEL_FILE))
    try:
        model = load_model(p.MODEL_FILE)
    except:
        print("Failed to load weights from the weights file, please ensure *.pb file is present in the MODEL_FILE directory")
        exit()
    
    try:
        print("Processing enroll sample....")
        enroll_result = get_embedding(model, file, p.MAX_SEC)
        enroll_embs = np.array(enroll_result.tolist())
        speaker = name
    except:
        print("Error processing the input audio file. Make sure the path.")
    try:
        np.save(os.path.join(p.EMBED_LIST_FILE,speaker +".npy"), enroll_embs)
        print("Succesfully enrolled the user")
    except:
        print("Unable to save the user into the database.")

def recognize(name, file):
    """Recognize the input audio file by comparing to saved users' voice prints
        inputs: str (Path to audio file of unknown person to recognize)
        outputs: str (Name of the person recognized)"""

    
    if not os.path.isfile(os.path.join(p.EMBED_LIST_FILE,name + ".npy")):
        print("User not enrolled")
        exit()
    print("Loading model weights from [{}]....".format(p.MODEL_FILE))
    try:
        model = load_model(p.MODEL_FILE)

    except:
        print("Failed to load weights from the weights file, please ensure *.pb file is present in the MODEL_FILE directory")
        exit()
        
    distances = {}
    print("Processing test sample....")
    print("Comparing test sample against enroll samples....")
    test_result = get_embedding(model, file, p.MAX_SEC)
    test_embs = np.array(test_result.tolist())

    enroll_embs = np.load(os.path.join(p.EMBED_LIST_FILE,name+".npy"))

    distance = euclidean(test_embs, enroll_embs)
    print("Distance : ",distance)

    if distance < p.THRESHOLD:
        print("Authentication Succesful")

    else:
        print("Authentication Failed")
        
#Helper functions
def file_choices(choices,filename):
    ext = os.path.splitext(filename)[1][1:]
    if ext not in choices:
        parser.error("file doesn't end with one of {}".format(choices))
    return filename

def get_extension(filename):
    return os.path.splitext(filename)[1][1:]

if __name__ == '__main__':

    name = "leslie"
    file = "Samples/hello1.wav"
    task = "recognize"


    if task == 'enroll':
        enroll(name, file)
    if task == 'recognize':
        recognize(name, file)


