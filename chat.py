from openai import OpenAI
from scipy.spatial.distance import cosine

from openai import OpenAI

client = OpenAI(
    api_key="NULL",
)

def create_context(
    question, df, max_len=1800, size="ada"
):
    """
    Create a context for a question by finding the most similar context from the dataframe
    """

    q_embeddings = client.embeddings.create(input=question, model='text-embedding-3-small').data[0].embedding

    df["distances"] = df["embeddings"].apply(lambda x: cosine(q_embeddings, x))


    returns = []
    cur_len = 0

    for _, row in df.sort_values('distances', ascending=True).iterrows():

        cur_len += row['n_tokens'] + 4

        if cur_len > max_len:
            break

        returns.append(row["text"])

    return "\n\n###\n\n".join(returns)

def answer_question(
    df,
    model="gpt-3.5-turbo",
    question="Am I allowed to publish model outputs to Twitter, without a human review?",
    max_len=1800,
    size="ada",
    debug=False,
    max_tokens=150,
    stop_sequence=None
):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context(
        question,
        df,
        max_len=max_len,
        size=size,
    )
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"You are a confident Capital One virtual assistant with decades of training. Answer the questions with this context: {context}" },
                {"role": "user", "content": question},
                
            ],
            temperature=0.7,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
        )
        return str(response.choices[0].message.content).strip() + "\nFor more assistance, visit the help center here: \nhttps://www.capitalone.com/help-center/"
    except Exception as e:
        print(e)
        return ""

