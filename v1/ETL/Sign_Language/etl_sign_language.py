#################################### Extract ####################################
# Imports
from datetime import timedelta
import cv2
import numpy as np
import os
import math
import uuid
from time import time

# Global variables and constants
VIDEOS_PATH = "/Users/layouni/Desktop/YassineISI/3 ING/BI/Project/ETL/Hand/code/videos"
SAVING_FRAMES_PER_SECOND = 2

def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g 00:00:20.05) 
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return (result + ".00").replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")

def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    # get the clip duration by dividing number of frames by the number of frames per second
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # use np.arange() to make floating-point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s

#################################### Transform ####################################
# Imports
import mediapipe as mp
import pickle
import base64
import json
from json import JSONEncoder

# Global variables and constants
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

#Extract landmark of a hand from an image
def frame_to_hand_landmarks(image):
    #convert image to numpy array (frame)
    frame = np.array(image, dtype=np.uint8)
    #convert the frame to RGB (mediapipe requires RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    data_aux = []
    x_ = []
    y_ = []
    # Process the frame
    results = hands.process(frame_rgb)
    # Extract the landmarks for one hand
    landmarks = any
    if(results.multi_hand_landmarks):
        landmarks = results.multi_hand_landmarks[0].landmark
    else:
        return False
    
    for i in range(len(landmarks)):
        x = landmarks[i].x
        y = landmarks[i].y
        x_.append(x)
        y_.append(y)

    for i in range(len(landmarks)):
        x = landmarks[i].x
        y = landmarks[i].y
        data_aux.append(x - min(x_))
        data_aux.append(y - min(y_))
    
    return [np.asarray(data_aux)]


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def encode_landmarks(landmarks):
    numpyData = {"array": landmarks}
    return json.dumps(numpyData, cls = NumpyArrayEncoder)



#################################### Load ####################################
import mysql.connector
DB_USER = "root"
DB_PWD = ""
DB_SERVER = "localhost"
DB_NAME = "Bridge_Video_V1"

def load_video(cnx, duration : str, number_frames : int):
    cursor = cnx.cursor()
    sql = "INSERT INTO Video (duration, number_frames) VALUES (%s, %s)"
    val = (duration, number_frames)
    cursor.execute(sql, val)
    cnx.commit()
    cursor.close()
    return cursor.lastrowid

def load_frame(cnx,has_landmarks:bool, path:str, number:int, landmarks:str, has_decision : bool):
    cursor = cnx.cursor()
    sql = "INSERT INTO Frame (has_landmarks,path,number,landmarks, has_decision) VALUES (%s, %s, %s, %s, %s)"
    val = (has_landmarks, path, number, landmarks, has_decision)
    cursor.execute(sql, val)
    cnx.commit()
    return cursor.lastrowid

def load_fact(cnx, video_id : int, frame_id : int):
    cursor = cnx.cursor()
    sql = "INSERT INTO Fact (video_id, frame_id) VALUES (%s, %s)"
    val = (video_id, frame_id)
    cursor.execute(sql, val)
    cnx.commit()
    cursor.close()
    return cursor.lastrowid


def update_last_video(cnx, duration : str, number_frames : int):
    cursor = cnx.cursor()
    sql = "UPDATE Video SET duration = %s, number_frames = %s WHERE video_id = (SELECT MAX(video_id) FROM Video)"
    val = (duration, number_frames)
    cursor.execute(sql, val)
    cnx.commit()
    cursor.close()
    return cursor.lastrowid


    


#################################### Main Functions ####################################

# Upload Video
def process_video(video_path):
    cnx = mysql.connector.connect(user = DB_USER, password = DB_PWD, host = DB_SERVER)
    cnx.database = DB_NAME
    cursor = cnx.cursor()
    filename, _ = os.path.splitext(video_path)
    filename += "_frames"
    # make a folder by the name of the video file
    if not os.path.isdir(filename):
        os.mkdir(filename)
    # read the video file    
    cap = cv2.VideoCapture(video_path)
    # get the FPS of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    # get the list of duration spots to save
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
    # start the loop
    count = 0
    frame_nbr = 0

    # Get video duration
    video_duration_seconds = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS)
    video_duration_formatted = format_timedelta(timedelta(seconds= video_duration_seconds))

    # Get video number of frames
    video_nbr_frames = math.ceil(2 * video_duration_seconds)

    # Load video and get the video id
    try:
        video_id = load_video(cnx, video_duration_formatted, video_nbr_frames)
    except:
        return "There was an error loading the video"

    while True:
        is_read, frame = cap.read()
        if not is_read:
            print("breaking")
            # break out of the loop if there are no frames to read
            break
        # get the duration by dividing the frame count by the FPS
        frame_duration = count / fps
        try:
            # get the earliest duration to save
            closest_duration = saving_frames_durations[0]
        except IndexError:
            # the list is empty, all duration frames were saved
            break
        if frame_duration >= closest_duration:
            # if closest duration is less than or equals the frame duration, 
            # then save the frame
            frame_nbr += 1
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            path = os.path.join(filename, f"frame_{frame_nbr}_{frame_duration_formatted}.jpg")
            cv2.imwrite(path, frame)

            # Transform
            hand_landmarks = frame_to_hand_landmarks(frame)
            has_landmarks = hand_landmarks != False

            try:
                # Load frame
                frame_id = load_frame(cnx, has_landmarks, path, frame_nbr, encode_landmarks(hand_landmarks) if has_landmarks else "",False)

                # Load fact
                load_fact(cnx, video_id, frame_id)

            except Exception as e:
                print("Error loading frame number {}".format(frame_nbr))
                print(e)
                pass

            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # increment the frame count
        count += 1

    cursor.close()
    cnx.close()
    return video_id