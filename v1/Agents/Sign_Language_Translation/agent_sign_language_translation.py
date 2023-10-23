import pickle
from cubes import PointCut, Cell
import base64
import json
import numpy as np



labels_dict = {0 : 'are', 1 : 'how', 2 : 'you', 3 : 'Hi', 4 : 'Thanks', 5: 'Bye'}

def browse_cube_by_frame(cube_browser, frame_id):
    cuts = [
        PointCut(dimension="Frame", path=[1,frame_id])]
    cell = Cell(cube_browser.cube, cuts = cuts)
    result = list(cube_browser.facts(cell))
    if(len(result) == 0):
        return None
    else:
        return result[0]

def browse_cube_by_video(cube_browser, video_id):
    cuts = [
        PointCut(dimension="Frame", path=[1]),
        PointCut(dimension="Video", path=[video_id])
        ]
    cell = Cell(cube_browser.cube, cuts = cuts)
    result = list(cube_browser.facts(cell))
    return result

def predict_video(model_path, cube_result):
    model_dict = pickle.load(open(model_path, 'rb'))
    model = model_dict['model']
    predictions = []
    for record in cube_result:
        landmarks = decode_landmarks(record["Frame.landmarks"])
        predicted_index = int((model.predict(landmarks))[0])
        predicted_word = labels_dict[predicted_index]
        predictions.append(predicted_word)
    return remove_repetition(predictions)


def predict_frame(model_path, cube_result):
    model_dict = pickle.load(open(model_path, 'rb'))
    model = model_dict['model']
    prediction = "" 
    landmarks = decode_landmarks(cube_result["Frame.landmarks"])
    predicted_index = int((model.predict(landmarks))[0])
    predicted_word = labels_dict[predicted_index]
    return predicted_word


def decode_landmarks(encoded_landmarks):
    decoded_landmarks = json.loads(encoded_landmarks)
    return np.asarray(decoded_landmarks["array"])

def remove_repetition(list):
    final_list = []
    for i, item in enumerate(list):
        if i == 0 or item != list[i - 1]:
            final_list.append(item)
    return final_list

def process_cube_by_video(cube_browser, video_id, model_path):
    frames = browse_cube_by_video(cube_browser = cube_browser, video_id = video_id)
    if(len(frames) == 0):
        return ["_No sign language found in video_"]
    else:
        return predict_video(model_path = model_path, cube_result = frames)
    

def process_cube_by_frame(cube_browser, frame_id, model_path):
    frame = browse_cube_by_frame(cube_browser = cube_browser, frame_id = frame_id)
    if(frame == None):
        return None
    else:
        return predict_frame(model_path = model_path, cube_result = frame)