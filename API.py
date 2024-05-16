from flask import Flask, request, jsonify, abort
import pandas as pd
import numpy as np
from chat import answer_question

df = pd.read_csv("processedEmbeddings.csv")
df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)

app = Flask(__name__)

@app.route('/api/message', methods = ['POST'])
def respond():

    if not request.json or 'question' not in request.json:
        abort(400, description = "Request must have a 'question' field.")

    question = request.json['question']

    try:
        answer = answer_question(df=df, question=question)
    except Exception as e:
        abort(500, description="An error occurred while processing your request.")

    return jsonify(answer=answer)

if __name__ == '__main__':
    app.run(debug=True)
