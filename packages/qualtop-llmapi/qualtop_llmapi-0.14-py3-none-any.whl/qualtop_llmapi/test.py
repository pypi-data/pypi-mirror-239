import openai

def main():
    openai.api_base = "http://localhost:8070/v1"
    openai.api_key = ""
    temperature = 0
    max_tokens = 500
    request_timeout=60
    messages = [
        {"role": "system", "content": "Eres un asistente inteligente."},
        {"role": "user", "content": "Cómo se llama J. Bieber?"}
        ]
    response = openai.ChatCompletion.create(
                model="mistral-7b-instruct-v0.1.Q4_0.gguf",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                request_timeout=request_timeout
            )
    print(response["choices"][0]["message"]["content"]
)

if __name__ == "__main__":
    main()
