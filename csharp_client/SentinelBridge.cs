using System;
using System.Net.Http;
using System.Net.Http.Json;
using System.Text.Json;
using System.Threading.Tasks;

public class SentinelBridge {
    private readonly HttpClient _client = new HttpClient { BaseAddress = new Uri("http://localhost:8000") };

    public async Task ProcessTransactionAsync(object tx, object baseline) {
        var payload = new { transaction = tx, user_baseline = baseline };
        
        // High-concurrency call to the Python LangGraph Orchestrator
        var response = await _client.PostAsJsonAsync("/triage", payload);
        
        if (response.IsSuccessStatusCode) {
            var result = await response.Content.ReadFromJsonAsync<JsonElement>();
            
            // Safe property access
            string summary = result.TryGetProperty("summary", out var summaryProp) ? summaryProp.GetString() : "No summary available.";
            bool isSuspicious = result.TryGetProperty("is_suspicious", out var suspProp) && suspProp.GetBoolean();

            // Logic to turn 2,000 alerts into 50 cases
            if (isSuspicious) {
                Console.WriteLine("🚨 ALERT FLAGGED BY AI ARCHITECT ENGINE");
                Console.WriteLine(summary); // Render the 30-second investigation summary
            }
        }
    }
}
