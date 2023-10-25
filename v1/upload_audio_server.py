import asyncio
import websockets
import uuid
import cv2
import os
import json
import sys
import multiprocessing
from multiprocessing import Process, Queue

# Audio imports
from DW.Audio import dw_audio
from ETL.Audio import etl_audio
from OLAP.Audio import olap_audio
from Agents.Audio_Translation import agent_audio_translation

# Text translation imports 
from Agents.Text_Translation import agent_text_translation



# Audio variables
AUDIOS_PATH = "./media/audios"
OLAP_AUDIO_MODEL_PATH = "./OLAP/Audio/olap_model_audio.json"

async def video_server(websocket, path):
    try:

        ########################### Collect video ###########################
        video_id = str(uuid.uuid1())
        video_path = os.path.join(AUDIOS_PATH, video_id +".mp3")
        print("Begining video upload")
        with open( video_path, 'ab') as file:
            async for video_data in websocket:
                if(video_data == "_DONE_"):
                     break
                else:
                    file.write(video_data)
        
        await websocket.send("_UPLOAD_COMPLETE_")

        result = exec_audio_bi_arch(video_path, video_id)
        await websocket.send(result)

        await websocket.send("_DONE_")
    except  Exception as e:
        print(f"Error : {e}")
        pass


def exec_audio_bi_arch(audio_path, video_id):
    audio_db_id = etl_audio.process_audio(audio_path)
    cube_browser = olap_audio.create_olap_cube(dw_audio.DB_STRING, OLAP_AUDIO_MODEL_PATH)
    result = agent_audio_translation.process_cube_audio(cube_browser, audio_db_id)
    inputs = [(result, "en"),(result, "fr"), (result, "de"), (result, "it"), (result, "es")]
    with multiprocessing.Pool(processes=5) as pool:
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
    
    return json.dumps(result_translated)




if __name__ == "__main__":
    ########################### DW ###########################
    # Initiate audio datawarehouse
    dw_audio.init_dw()

    ########################### RUN SERVER ###########################
    print("Started listening on websocket video server : ws://192.168.1.19:8764")
    start_server = websockets.serve(video_server, "192.168.1.19", 8764)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()