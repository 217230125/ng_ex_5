from pathlib import Path
from ollama import chat

question = """
I changed my university password this morning.
Now my Windows laptop won't connect to campus Wi-Fi,
but my phone still works.
"""

context = ""
for file in Path("knowledge").glob("*.txt"):
    context += file.read_text()
    context += "\n\n"

print("Context characters:", len(context))

response = chat(
    model="qwen",
    messages=[
        {"role": "system", "content": f"You are a university IT support assistant. Answer using only the context below:\n\n{context}"},
        {"role": "user", "content": question}
    ]
)

print(response.message.content)
