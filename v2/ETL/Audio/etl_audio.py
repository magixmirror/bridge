import os
import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"
from moviepy.editor import VideoFileClip
import mysql.connector
from pydub import AudioSegment
from tkinter.filedialog import askopenfilename
DB_USER = "root"
DB_PWD = ""
DB_SERVER = "localhost"
DB_NAME = "Bridge_Audio"
 
 
# Function to convert MP4 to MP3
def convert_mp4_to_mp3(input_file, output_file):
    video = VideoFileClip(input_file)
    audio = video.audio
    audio.write_audiofile(output_file)
    audio.close()

def convert_video_to_audio(input_file, output_file):
    video = AudioSegment.from_file(input_file)
    output_directory = 'media'
    os.makedirs(output_directory, exist_ok=True)
    output_file_path = os.path.join(output_directory, output_file)
    video.export(output_file_path, format="mp3")
    return output_file_path

# Function to insert data into the DimFilePaths table and get the ID

def insert_path_get_id(path, mysql_connection):
    cursor = mysql_connection.cursor()
    insert_query = "INSERT INTO file_path (path) VALUES (%s)"
    cursor.execute(insert_query, (path,))
    mysql_connection.commit()
    cursor.close()
    return cursor.lastrowid 

# Function to insert data into the DimFileNames table and get the ID
def insert_name_get_id(name, mysql_connection):
    cursor = mysql_connection.cursor()
    insert_query = "INSERT INTO file_name (name) VALUES (%s)"
    cursor.execute(insert_query, (name,))
    mysql_connection.commit()
    cursor.close()
    return cursor.lastrowid 

# Function to insert data into the DimVideos table and get the ID
def insert_video_get_id(video_duration, video_type, mysql_connection):
    cursor = mysql_connection.cursor()
    insert_query = "INSERT INTO video (duration, type) VALUES (%s, %s)"
    cursor.execute(insert_query, (video_duration, video_type))
    mysql_connection.commit()
    cursor.close()
    return cursor.lastrowid  

# Function to insert data into the DimAudio table and get the ID
def insert_audio_get_id(audio_duration, audio_type, mysql_connection):
    cursor = mysql_connection.cursor()
    insert_query = "INSERT INTO audio (duration, type) VALUES (%s, %s)"
    cursor.execute(insert_query, (audio_duration, audio_type))
    mysql_connection.commit()
    cursor.close()
    return cursor.lastrowid

# Function to save file data in the fact table
def save_file_data_to_fact(file_name_id, file_size, file_type, file_path_id, video_id, utility_id, mysql_connection):
    cursor = mysql_connection.cursor()
    insert_query = "INSERT INTO facts (file_name_id, file_size, file_type, file_path_id, video_id, utility_id) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (file_name_id, file_size, file_type, file_path_id, video_id, utility_id))
    mysql_connection.commit()
    cursor.close()


def save_audio(input_audio_file):
    media_folder = 'media'
    os.makedirs(media_folder, exist_ok=True)
    input_audio_basename = os.path.basename(input_audio_file)
    new_path = os.path.join(media_folder, input_audio_basename)
    audio = AudioSegment.from_file(input_audio_file)
    audio.export(new_path, format="mp3")
    return os.path.abspath(new_path)

 

# Function to insert is_silent_audio into the utility table and get the ID
def insert_utility_data(is_silent, mysql_connection):
    cursor = mysql_connection.cursor()
    if is_silent:
        is_silent = 0
    else:
        is_silent = 1
    insert_query = "INSERT INTO utility (no_silent) VALUES (%s)"
    cursor.execute(insert_query, (is_silent,))
    mysql_connection.commit()
    cursor.close()
    return cursor.lastrowid  

# Function to analyze audio and check for silence
def is_silent_audio(audio_file):
    audio = AudioSegment.from_file(audio_file)
    average_loudness = audio.dBFS
    silence_threshold = -50  # Adjust this threshold as needed
    return average_loudness <= silence_threshold


# Main function to process the MP4 file
def process_video(input_file,output_path):
    try:
        cnx = mysql.connector.connect(user = DB_USER, password = DB_PWD, host = DB_SERVER)
        cnx.database = DB_NAME
        # Get video duration
        video = VideoFileClip(input_file)
        video_duration = video.duration

        # Get the basename of the input MP4 file without extension
        input_mp4_basename = os.path.splitext(os.path.basename(input_file))[0]

        output_mp3_file = output_path + ".mp3"

        # Convert MP4 to MP3
        convert_mp4_to_mp3(input_file, output_path)


        # Insert file path into DimFilePaths and get the ID
        file_path_id = insert_path_get_id(output_path, cnx)

        # Insert file name into DimFileNames and get the ID
        file_name_id = insert_name_get_id(input_mp4_basename, cnx)

        # Insert video duration into DimVideos and get the ID
        duration_in_minutes = video_duration / 60
        duration_string = f"{duration_in_minutes:.2f} min"
        video_id = insert_video_get_id(duration_string, "MP4", cnx)

        # Analyze audio for silence
        is_silent = is_silent_audio(output_path)

        # Insert the result into the utility table
        utility_id = insert_utility_data(is_silent, cnx)

        # Insert file data into the fact table
        size_in_bytes = os.path.getsize(output_path)
        size_in_mb = size_in_bytes / (1024 * 1024)  # Convert to megabytes
        size_in_mb_str = f"{size_in_mb:.3f} MB"
        save_file_data_to_fact(file_name_id, size_in_mb_str, "MP3", file_path_id, video_id, utility_id, cnx)
        print("File data saved in the database.")

        return video_id
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the database connection in the finally block
        cnx.close()



def process_audio(input_media_file):
    try:
            cnx = mysql.connector.connect(user = DB_USER, password = DB_PWD, host = DB_SERVER)
            cnx.database = DB_NAME

            # Process MP3 file
            new_audio_path = save_audio(input_media_file)
            audio = AudioSegment.from_file(new_audio_path)
            audio_duration = len(audio) / 1000
            input_media_basename = os.path.splitext(os.path.basename(input_media_file))[0]

            file_path_id = insert_path_get_id(new_audio_path, cnx)
            file_name_id = insert_name_get_id(input_media_basename, cnx)
            duration_in_minutes = audio_duration/60
            duration_string = f"{duration_in_minutes:.2f} min"
            audio_id = insert_audio_get_id(duration_string, "MP3", cnx)
            is_silent = is_silent_audio(new_audio_path)
            utility_id = insert_utility_data(is_silent, cnx)
            size_in_bytes = os.path.getsize(new_audio_path)
            size_in_mb = size_in_bytes / (1024 * 1024)
            size_in_mb_str = f"{size_in_mb:.3f} MB"
            save_file_data_to_fact(file_name_id, size_in_mb_str, "MP3", file_path_id, None,audio_id, utility_id, cnx)

            print("MP3 file data saved in the database.")

            return audio_id
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cnx.close()


