using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Xml;
using System.Xml.Linq;
using System.Xml.XPath;
using Blitz2019;
using CommandLine;

public static class Program
{
    class Options
    {
        [Option('p', "port", HelpText = "Set port number (default: 8010)", Default = 8010)]
        public int Port { get; set; }
    }

    public static void Main(string[] args)
    {
        Parser.Default.ParseArguments<Options>(args).WithParsed(o =>
        {
            
            HttpListener listener = new HttpListener();

            listener.Prefixes.Add("http://*:" + o.Port + "/");
            listener.Start();

            while (true)
            {
                Blitz2k19RPCServer server = new Blitz2k19RPCServer(new MyBot());
                server.ProcessRequest(listener.GetContext());
            }
        });
    }
}