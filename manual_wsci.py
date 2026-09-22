from pathlib import Path
from ollama import chat

question = """
I changed my university password this morning.
Now my Windows laptop won't connect to campus Wi-Fi,
but my phone still works.
"""

selected_files = [
    "knowledge/password_changes.txt",
    "knowledge/wifi_setup.txt",
    "knowledge/service_status.txt"
]

context = ""
for file_path in selected_files:
    context += Path(file_path).read_text()
    context += "\n\n"

response = chat(
    model="qwen",
    options={
        "temperature": 0.1,
        "repeat_penalty": 1.3,
        "repeat_last_n": 128,
        "num_predict": 400
    },
    messages=[
        {
            "role": "system",
            "content": f"Use only the context below to answer. Give a short numbered list of Windows troubleshooting steps. Do not repeat anything.\n\nContext:\n{context}"
        },
        {"role": "user", "content": question}
    ]
)

print("Context characters:", len(context))
print("\nSolution:")
print(response.message.content)
