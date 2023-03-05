
from IPython.display import Audio
import whisper
import librosa
import googletrans
import torch
import os
from googletrans import Translator
import soundfile


# loading the whisper model
model = whisper.load_model("tiny")


def speech_to_text(audio_input,language_code):
    try:
        audio, sr = librosa.load(audio_input)
        if not language_code:
            audio_text = model.transcribe(audio)
            if 'text' not in audio_text:
                raise AttributeError("Unable to transcribe audio file.")
            text = audio_text['text']
            translater = Translator()
            out = translater.detect(text)
            lang_code = out.lang
            result = translater.translate(text,src=lang_code,dest='en')
            if result.text is None:
                raise ValueError("Failed to translate text.")
            text = result.text

        # if language code is 'en', use whisper model directly to transcribe speech to text
        if language_code == 'en':
            audio_text = model.transcribe(audio)
            if 'text' not in audio_text:
                raise AttributeError("Unable to transcribe audio file.")
            text = audio_text['text']
        # if language code is not 'en', first convert to English using Google Translate API
        else:
            audio_text = model.transcribe(audio)
            if 'text' not in audio_text:
                raise AttributeError("Unable to transcribe audio file.")
            text = audio_text['text']
            translater = Translator()
            result = translater.translate(text,src=language_code,dest='en')
            if result.text is None:
                raise ValueError("Failed to translate text.")
            text = result.text

        return {'transcription': text}

    except FileNotFoundError:
        return {'error': 'Audio file not found'}
    except AttributeError as e:
        return {'error': str(e)}
    except ValueError as e:
        return {'error': str(e)}
    except Exception as e:
        return {'error': str(e)}


if __name__ == '__main__':
    try:
        output_dict = speech_to_text(audio_path,language_code)
        print(output_dict)

    except Exception as e:
        print("Error:", str(e))