using CommandLine;
using Microsoft.AspNetCore;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using System.Collections.Generic;

namespace Blitz_2019
{
    public class Program
    {
        public static int port;

        class Options
        {
            [Option('p', "port", HelpText = "Set port number (default: 8010)", Default = 8010)]
            public int Port { get; set; }
        }

        public static void Main(string[] args)
        {
            Parser.Default.ParseArguments<Options>(args).WithParsed(o =>
            {
                port = o.Port;
            });

            CreateWebHostBuilder(args).Build().Run();
        }


        public static IWebHostBuilder CreateWebHostBuilder(string[] args) =>
            WebHost.CreateDefaultBuilder(args)
                .UseUrls("http://*:" + port)
                .UseStartup<Startup>()
                .ConfigureAppConfiguration((context, config) =>
                {
                    config.AddInMemoryCollection(new Dictionary<string, string>
                    {
                        {"Logging:LogLevel:System", "Error"},
                        {"Logging:LogLevel:Microsoft", "Error"}
                    });
                })
                .UseKestrel(options => {
                    options.Limits.MaxRequestLineSize = (int)options.Limits.MaxRequestBufferSize;
        
                });
    }
}
