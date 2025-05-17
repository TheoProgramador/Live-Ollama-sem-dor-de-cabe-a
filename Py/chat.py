import json
import requests

MODEL = "deepseek-r1:7b"
URL = "http://localhost:11434/api/generate"

def perguntar_ollama_stream(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": True,
        "options": {
            "numa": True,
            "num_ctx": 4096,
            "gpu_layers": 100  # Força uso de GPU em todas as camadas, se suportado
        }
    }

    try:
        with requests.post(URL, json=payload, stream=True) as response:
            response.raise_for_status()
            print("Ollama: ", end='', flush=True)
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = line.decode('utf-8')
                        data = json.loads(chunk)  # agora é a forma correta
                        print(data['response'], end='', flush=True)
                    except Exception as e:
                        print(f"\n[Erro de parsing do chunk]: {e}")
            print()  # quebra de linha final
    except Exception as e:
        print(f"\nErro na conexão com o Ollama: {e}")

def chat():
    print(f"🔗 Conectado ao modelo: {MODEL}")
    print("Digite 'sair' para encerrar.")
    while True:
        user_input = input("Você: ")
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o chat.")
            break
        perguntar_ollama_stream(user_input)

if __name__ == "__main__":
    chat()
