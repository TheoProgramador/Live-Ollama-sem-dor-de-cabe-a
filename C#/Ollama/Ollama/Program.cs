using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

class Program
{
    static readonly HttpClient client = new HttpClient();
    const string url = "http://localhost:11434/api/generate";
    const string model = "deepseek-r1:32b";

    static async Task Main()
    {
        Console.WriteLine($"🔗 Conectado ao modelo: {model}");
        Console.WriteLine("Digite 'sair' para encerrar.");

        while (true)
        {
            Console.Write("Você: ");
            string userInput = Console.ReadLine();

            if (string.Equals(userInput, "sair", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("Encerrando o chat.");
                break;
            }

            await EnviarPromptAsync(userInput);
        }
    }

    static async Task EnviarPromptAsync(string prompt)
    {
        var payload = new
        {
            model = model,
            prompt = prompt,
            stream = false,
            options = new
            {
                numa = true,
                num_ctx = 4096,
                gpu_layers = 100
            }
        };

        var json = JsonSerializer.Serialize(payload);
        var content = new StringContent(json, Encoding.UTF8, "application/json");

        try
        {
            var response = await client.PostAsync(url, content);
            response.EnsureSuccessStatusCode();

            var resultJson = await response.Content.ReadAsStringAsync();
            using var doc = JsonDocument.Parse(resultJson);
            string resposta = doc.RootElement.GetProperty("response").GetString();

            Console.WriteLine($"\nOllama: {resposta}\n");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Erro: {ex.Message}");
        }
    }
}
