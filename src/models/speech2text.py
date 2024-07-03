from faster_whisper import WhisperModel


whisper_model = WhisperModel("medium")


def transcribe_audio(audio_file):
    segments, _ = whisper_model.transcribe(audio_file, )
    for segment in segments:
        yield segment.text
