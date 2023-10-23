import asyncio
import websockets
import uuid
import cv2
import os
import json
import sys
from multiprocessing import Process, Queue, Pool

# Audio imports
from DW.Audio import dw_audio
from ETL.Audio import etl_audio
from OLAP.Audio import olap_audio
from Agents.Audio_Translation import agent_audio_translation

# Sign language imports
from DW.Sign_Language import dw_sign_language
from ETL.Sign_Language import etl_sign_language
from OLAP.Sign_Language import olap_sign_language
from Agents.Sign_Language_Translation import agent_sign_language_translation

# Text translation imports 
from Agents.Text_Translation import agent_text_translation



# Audio variables
AUDIOS_PATH = "./media/audios"
OLAP_AUDIO_MODEL_PATH = "./OLAP/Audio/olap_model_video.json"

# Sign language variables
VIDEOS_PATH = "./media/videos"
OLAP_SL_MODEL_PATH = "./OLAP/Sign_Language/olap_model_sign_language.json"
SIGN_TRANSLATION_MODEL_PATH = "./Agents/Sign_Language_Translation/model.p"

async def video_server(websocket, path):
    try:

        ########################### Collect video ###########################
        video_id = str(uuid.uuid1())
        video_path = os.path.join(VIDEOS_PATH, video_id +".mp4")
        print("Begining video upload")
        with open( video_path, 'ab') as file:
            async for video_data in websocket:
                if(video_data == "_DONE_"):
                     break
                else:
                    file.write(video_data)
        
        await websocket.send("_UPLOAD_COMPLETE_")

        audio_queue = Queue()
        sl_queue = Queue()

        audio_process = Process(target = exec_audio_bi_arch, args = (video_path, video_id, audio_queue))
        sl_process = Process(target = exec_video_bi_arch, args = (video_path, sl_queue))

        audio_process.start()
        sl_process.start()

        while (audio_process.is_alive() or sl_process.is_alive()):
            if(not audio_process.is_alive()):
                await websocket.send(audio_queue.get())
                await websocket.send(sl_queue.get())
                break

            if(not sl_process.is_alive()):
                await websocket.send(sl_queue.get())
                await websocket.send(audio_queue.get())
                break

        audio_process.join()
        sl_process.join()

        await websocket.send("_DONE_")
    except  Exception as e:
        print(f"Error : {e}")
        pass


def exec_audio_bi_arch(video_path, video_id, queue):
    video_db_id = etl_audio.process_video(video_path, os.path.join(AUDIOS_PATH,video_id + ".mp3"))
    cube_browser = olap_audio.create_olap_cube(dw_audio.DB_STRING, OLAP_AUDIO_MODEL_PATH)
    result = agent_audio_translation.process_cube_video(cube_browser, video_db_id)

    inputs = [(result, "en"),(result, "fr"), (result, "de"), (result, "it"), (result, "es")]
    with Pool(processes=5) as pool:
            outputs = pool.map(agent_text_translation.translate, inputs)
            pool.close()
            pool.join()
            
    result_translated = { "audio" : {
            "en" : outputs[0],
            "fr" : outputs[1],
            "de" : outputs[2],
            "it" : outputs[3],
            "es" : outputs[4]
            }
        }
    
    queue.put(json.dumps(result_translated))


def exec_video_bi_arch(video_path, queue):
    video_db_id = etl_sign_language.process_video(video_path)
    cube_browser = olap_sign_language.create_olap_cube(dw_sign_language.DB_STRING, OLAP_SL_MODEL_PATH)
    result_array = agent_sign_language_translation.process_cube_by_video(cube_browser,video_db_id, SIGN_TRANSLATION_MODEL_PATH)
    result_phrase = ' '.join(result_array)
    
    inputs = [(result_phrase, "fr"), (result_phrase, "de"), (result_phrase, "it"), (result_phrase, "es")]
    with Pool(processes=4) as pool:
            outputs = pool.map(agent_text_translation.translate, inputs)
            pool.close()
            pool.join()
            
    result_translated = { "sign language" : {
            "en" : result_phrase,
            "fr" : outputs[0],
            "de" : outputs[1],
            "it" : outputs[2],
            "es" : outputs[3]
            }
        }
    
    queue.put(json.dumps(result_translated))




if __name__ == "__main__":
    ########################### DW ###########################
    # Initiate sign language datawarehouse
    dw_sign_language.init_dw()
    # Initiate audio datawarehouse
    dw_audio.init_dw()

    ########################### RUN SERVER ###########################
    print("Started listening on websocket video server : ws://192.168.1.19:8765")
    start_server = websockets.serve(video_server, "192.168.1.19", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()