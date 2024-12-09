import os
from groq import Groq
os.environ['GROQ_API_KEY'] = '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'

def generate_mcqs(topic, num_questions):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": f"Generate {num_questions} multiple-choice questions about {topic}, each with four options and the correct answer marked. make sure questions are not too easy or too tough"},
        ],
        model="llama3-8b-8192",
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    topic = input("Enter the topic: ")
    num_questions = int(input("Enter the number of questions: "))
    mcqs = generate_mcqs(topic, num_questions)
    print("Generated MCQs:\n",mcqs)