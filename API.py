from flask import Flask, request, jsonify, abort
import pandas as pd
import numpy as np
from chat import answer_question
import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv, dotenv_values 

load_dotenv()
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

df = pd.read_csv("embeddings.csv")
df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)



#The neural multilingual voice can speak different languages based on the input text.
speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'
file_name = "outputaudio.mp3"  
file_config = speechsdk.audio.AudioOutputConfig(filename=file_name) 
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)  

# Get text from the console and synthesize to the default speaker.
print("Enter a question")
ques = input()
text = answer_question(df, question=ques)
print(text)

speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()



app = Flask(__name__)

@app.route('/api/message', methods = ['POST'])
def respond():

    if not request.json or 'question' not in request.json:
        abort(400, description = "Request must have a 'question' field.")

    question = request.json['question']

    try:
        answer = answer_question(df=df, question=question) + "\nFor additional help, visit the Help Center here: \nhttps://www.capitalone.com/help-center/"
    except Exception as e:
        abort(500, description="An error occurred while processing your request.")

    return jsonify(answer=answer)

if __name__ == '__main__':
    app.run(debug=True)
