using System;
using System.Net.Http;
using System.Net.Http.Json;
using System.Linq;
using System.Threading.Tasks;

namespace SentinelStressTest
{
    class Program
    {
        static async Task Main(string[] args)
        {
            var tester = new StressTester();
            await tester.RunHammer();
        }
    }
}
