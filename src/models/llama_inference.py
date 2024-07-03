from llama_cpp import Llama
from env import SYSTEM_PROMPT

model = Llama(
    model_path="src/weights/saiga-q4_K.gguf",
    n_ctx=8192,
    n_parts=1,
    verbose=False,
    n_threads=7
)

def generate(message, response_format=None):
    messages = [{
        "role": "system", 
        "content": SYSTEM_PROMPT
    }]

    messages.append({
        "role": "user", 
        "content": message
    })
    
    response = ""
    for part in model.create_chat_completion(
            messages,
            temperature=0.7,
            top_k=50,
            top_p=0.85,
            repeat_penalty=1.2,
            stream=True,
            response_format=response_format
        ):
            delta = part["choices"][0]["delta"]
            if "content" in delta:
                response += delta["content"]
                yield response 
