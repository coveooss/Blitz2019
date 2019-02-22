package com.coveo;

import com.coveo.rpc.Blitz2k19RPCServer;
import java.io.IOException;
import org.apache.xmlrpc.XmlRpcException;
import picocli.CommandLine;
import picocli.CommandLine.Option;

public class MyBot
{
  public static class Args {
    @Option(names = { "-p", "--port" },
        description = "set port number (default: 8010)",
        defaultValue = "8010")
    public int port;
  }

  public static void main (String [] args) throws XmlRpcException, IOException {
    Args arguments = new Args();
    new CommandLine(arguments).parse(args);
    Blitz2k19RPCServer<RandomBot> BlitzServer = new Blitz2k19RPCServer<>(RandomBot.class, arguments.port);
  }

}
