import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

def get_resume_score(resume_text, job_description):
    prompt = (
        f"You are a resume evaluator. \n\n"
        f"Here is the JOB DESCRIPTION that you are going to evaluate the resume for:\n{job_description}\n\n"
        f"RESUME:\n{resume_text}\n\n"
        f"Evaluate how well this resume matches the job.\n"
        f"Give a match score out of 100 and a one paragraph good useful explanation."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return response['choices'][0]['message']['content']
