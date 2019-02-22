using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using System;

namespace Blitz_2019
{
    [Route("/")]
    [ApiController]
    public class MyBot : ControllerBase
    {
        [HttpGet("/microchallenge")]
        public ActionResult<string> Solve(string problem)
        {
            Console.WriteLine("\n\n\n-------------------------- REQUEST LOGS STARTING HERE --------------------------");
            Console.WriteLine("You can log stuff and download the logs from the UI in the replay section.");
            Console.WriteLine("Here is the current problem:");
            Console.WriteLine(problem); // problem is in json format
            Console.WriteLine("---------------------------------------------------------------------------------");

            return 18.ToString();
        }
    }
}
