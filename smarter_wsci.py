from pathlib import Path
from ollama import chat
import json

question = """
I changed my university password this morning.
Now my Windows laptop won't connect to campus Wi-Fi,
but my phone still works.
"""

service_status = {"wifi": "operational"}
state = {
    "problem": question,
    "wi_fi status": "operational",
    "wi-fi_check": True
}

with open("state.json", "w") as file:
    json.dump(state, file, indent=2)

with open("state.json", "r") as file:
    state = json.load(file)
print(state)

def select_context(question):
    keyword_map = {
        "password": "knowledge/password_changes.txt",
        "wi-fi": "knowledge/wifi_setup.txt",
        "wifi": "knowledge/wifi_setup.txt",
        "campus": "knowledge/wifi_setup.txt",
        "service": "knowledge/service_status.txt",
        "status": "knowledge/service_status.txt"
    }
    q_lower = question.lower()
    selected = set()
    for kw, fp in keyword_map.items():
        if kw in q_lower:
            selected.add(fp)
    return list(selected)

selected_files = select_context(question)

context = ""
for fp in selected_files:
    context += Path(fp).read_text()
    context += "\n\n"

def compress_context(context):
    res = chat(
        model="qwen",
        options={
            "temperature": 0.1,
            "repeat_penalty": 1.5,
            "num_predict": 250
        },
        messages=[
            {
                "role": "system",
                "content": "Extract only the complete Windows eduroam Wi-Fi troubleshooting steps from the context. Output numbered steps only. No extra explanation, no macOS, no mobile content."
            },
            {"role": "user", "content": context}
        ]
    )
    return res.message.content.strip()

compressed_context = compress_context(context)
print("\nCompressed context characters:", len(compressed_context))
print("Compressed content:\n" + compressed_context)

response = chat(
    model="qwen",
    options={
        "temperature": 0.1,
        "repeat_penalty": 1.5,
        "num_predict": 250
    },
    messages=[
        {
            "role": "system",
            "content": "Turn the content below into a clean numbered list. Use ONLY the content given. Do NOT add any new steps, advice or disclaimers."
        },
        {"role": "user", "content": compressed_context}
    ]
)

print("\nSolution:")
print(response.message.content)

state["relevant_files"] = selected_files
state["compressed_context"] = compressed_context
state["solution"] = response.message.content

with open("state.json", "w") as file:
    json.dump(state, file, indent=2)

print("\nFinal state saved to state.json")
