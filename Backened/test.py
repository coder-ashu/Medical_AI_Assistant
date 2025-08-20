from google import genai

client = genai.Client(api_key="AIzaSyB3XrpR7gOxcvX0joLpXDOeIbagSiV0ejE")

resp = client.models.generate_content(
    model="gemini-2.5-pro",
    contents="Hello, Gemini!"
)
print(resp.text)
