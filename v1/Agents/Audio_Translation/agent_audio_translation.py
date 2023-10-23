import whisper
from cubes import PointCut,Cell


def browse_cube_video(cube_browser, video_id):
    cuts = [
        PointCut(dimension="utility", path=[1]),
        PointCut(dimension="video", path=[video_id])
    ]
    cell = Cell(cube_browser.cube, cuts = cuts)
    result = list(cube_browser.facts(cell))
    if(len(result) != 0):
        return result[0]["file_path.path"]
    return None


def browse_cube_audio(cube_browser, audio_id):
    cuts = [
        PointCut(dimension="utility", path=[1]),
        PointCut(dimension="audio", path=[audio_id])
    ]
    cell = Cell(cube_browser.cube, cuts = cuts)
    result = list(cube_browser.facts(cell))
    if(len(result) != 0):
        return result[0]["file_path.path"]
    return None


def audio_to_text(audio_file_path):
    # Load the model
    model = whisper.load_model("base")

    # Load the audio
    audio = whisper.load_audio(audio_file_path)

    # Transcribe the audio
    result = model.transcribe(audio, fp16=False)

    # Pad or trim the audio
    #audio = whisper.pad_or_trim(audio)

    # Make a log-Mel spectrogram and move it to the same device as the model
   # mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # Detect the spoken language
    #_, probs = model.detect_language(mel)

    #detected_language = max(probs, key=probs.get)

    return result["text"]

def process_cube_video(cube_browser, video_id):
    audio_path = browse_cube_video(cube_browser = cube_browser, video_id = video_id)
    if audio_path is not None:
        return audio_to_text(audio_file_path = audio_path)
    else:
        return "_No speech found in video_"
    
def process_cube_audio(cube_browser, audio_id):
    audio_path = browse_cube_audio(cube_browser = cube_browser, audio_id = audio_id)
    if audio_path is not None:
        return audio_to_text(audio_file_path = audio_path)
    else:
        return "_No specch found in audio_"


