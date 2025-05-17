import json
import requests

MODEL = "deepseek-coder:6.7b-instruct"
URL = "http://localhost:11434/api/chat"

# Histórico do chat no formato API
chat_history = [
    {
        "role": "system",
        "content": "Você é um assistente técnico direto, que responde com profundidade para um desenvolvedor experiente em .NET, IA local e automações complexas."
    }
]

def perguntar_ollama_stream(user_input):
    #print (chat_history)
    chat_history.append({"role": "user", "content": user_input})

    payload = {
        "model": MODEL,
        "messages": chat_history,  # ✅ corrigido aqui
        "stream": True
    }

    try:
        with requests.post(URL, json=payload, stream=True) as response:
            response.raise_for_status()
            print("Ollama: ", end='', flush=True)
            assistant_reply = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = line.decode('utf-8')
                        data = json.loads(chunk)
                        content = data.get('message', {}).get('content', '')
                        print(content, end='', flush=True)
                        assistant_reply += content
                    except Exception as e:
                        print(f"\n[Erro de parsing do chunk]: {e}")
            print()  # quebra de linha final
            chat_history.append({"role": "assistant", "content": assistant_reply})
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
