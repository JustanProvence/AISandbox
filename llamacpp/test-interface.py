from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:8000/v1/", api_key="Not-a-real-key")

stream = client.chat.completions.create(
    model="mistral",
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
