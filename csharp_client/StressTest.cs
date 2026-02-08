using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

public class StressTester {
    private readonly HttpClient _client = new HttpClient { 
        BaseAddress = new Uri("http://127.0.0.1:8000"),
        Timeout = TimeSpan.FromMinutes(2) 
    };

    public async Task RunHammer() {
        Console.WriteLine("🔨 Starting 'The Hammer' 2,000 Alert Stress Test...");
        
        var lines = File.ReadAllLines("attack_data.csv").Skip(1).ToArray(); // Skip header
        var tasks = new List<Task>();
        
        var stopwatch = Stopwatch.StartNew();

        // Simulate the firehose of 2,000 alerts
        // Using Parallel.ForEach logic via tasks list to simulate concurrent firehose
        foreach (var line in lines) {
            var parts = line.Split(',');
            // CSV columns: amount,loc,timestamp,mean_amt,std_amt,last_loc,last_time,type,ip_address
            
            var payload = new {
                transaction = new { 
                    amount = double.Parse(parts[0]), 
                    loc = parts[1], 
                    timestamp = parts[2],
                    type = parts.Length > 7 ? parts[7] : "TRANSFER",
                    ip_address = parts.Length > 8 ? parts[8] : "0.0.0.0"
                },
                user_baseline = new { 
                    mean_amt = double.Parse(parts[3]), 
                    std_amt = double.Parse(parts[4]), 
                    last_loc = parts[5], 
                    last_time = parts[6] 
                }
            };
            
            tasks.Add(_client.PostAsJsonAsync("/triage", payload));
        }

        await Task.WhenAll(tasks);
        stopwatch.Stop();
        
        Console.WriteLine($"\n✅ Hammered {lines.Length} alerts in {stopwatch.Elapsed.TotalSeconds:F2} seconds.");
        double tps = lines.Length / stopwatch.Elapsed.TotalSeconds;
        Console.WriteLine($"🚀 Throughput: {tps:F2} TPS (Target: 4,793 TPS)");
    }
}
