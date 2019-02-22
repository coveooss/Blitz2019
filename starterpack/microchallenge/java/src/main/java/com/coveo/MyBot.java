package com.coveo;

import io.javalin.Javalin;
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

  public static void main (String [] args) {
    Args arguments = new Args();
    new CommandLine(arguments).parse(args);

    Javalin app = Javalin.create().start(arguments.port);
    app.get("/microchallenge", ctx -> {
      
      System.out.println("\n\n\n-------------------------- REQUEST LOGS STARTING HERE --------------------------");
      System.out.println("You can log stuff and download the logs from the UI in the replay section.");
      System.out.println("Here is the current problem:");
      System.out.println(ctx.queryParam("problem")); // problem is in json format
      System.out.println("---------------------------------------------------------------------------------");
      
      ctx.result(Integer.toString(18));
    });
  }

}
