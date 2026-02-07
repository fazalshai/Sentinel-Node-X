using System;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

// Sentinel-Node X: .NET 8 High-Throughput Bridge
public class SentinelGateway {
    private readonly HttpClient _client = new HttpClient { 
        BaseAddress = new Uri("http://localhost:8000"),
        Timeout = TimeSpan.FromSeconds(30) 
    };

    public async Task ExecuteTriageAsync(double amount, string location) {
        var request = new {
            transaction = new { 
                amount = amount, 
                loc = location, 
                timestamp = DateTime.UtcNow.ToString("o") 
            },
            user_baseline = new { 
                mean_amt = 100, 
                std_amt = 20, 
                last_loc = "Dubai", 
                last_time = DateTime.UtcNow.AddHours(-1).ToString("o") 
            }
        };

        // Post to the Python LangGraph Orchestrator
        var response = await _client.PostAsJsonAsync("/triage", request);
        var result = await response.Content.ReadAsStringAsync();
        
        // This fulfills the "30-second investigation" requirement
        Console.WriteLine("--- AI INVESTIGATION COMPLETE ---");
        Console.WriteLine(result); 
    }
}
