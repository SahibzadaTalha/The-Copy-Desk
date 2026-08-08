import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ .env file mein GROQ_API_KEY nahi mili. Check karo.")
else:
    print("✅ API key mil gayi, ab test kar rahe hain...")
    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Say hello in one short sentence."}],
        temperature=0.7,
    )
    print("✅ API sahi kaam kar rahi hai!")
    print("Response:", response.choices[0].message.content)