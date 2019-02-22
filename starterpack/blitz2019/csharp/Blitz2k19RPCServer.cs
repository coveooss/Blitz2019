using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Xml;
using System.Xml.XPath;

namespace Blitz2019
{
    public class Blitz2k19RPCServer
    {
        private IBot bot;

        public Blitz2k19RPCServer(IBot bot)
        {
            this.bot = bot;
        }

        public void ProcessRequest(HttpListenerContext httpListenerContext)
        {
            XmlDocument document = new XmlDocument();
            XPathNavigator navigator = document.CreateNavigator();
            document.Load(httpListenerContext.Request.InputStream);

            String response = "";

            switch(navigator.SelectSingleNode("/methodCall/methodName").Value)
            {
                case "initialize":
                    response = processInitializeRequest(navigator);
                    break;
                case "play":
                    response = processPlayRequest(navigator);
                    break;
            }

            StreamWriter writer = new StreamWriter(httpListenerContext.Response.OutputStream);
            httpListenerContext.Response.ContentType = "application/xml";

            writer.Write(response);
            writer.Close();
        }

        private string processInitializeRequest(XPathNavigator navigator)
        {
            Board board = parseBoard(navigator);
            int[] players = parseArrayOfNumbers(navigator.Select("//param[2]//value//value")).ToArray();
            double? time_left = parseNillableDouble(navigator.SelectSingleNode("//param[3]//value"));

            try
            {
                bool answer = this.bot.initialize(board, players, time_left);
                return "<?xml version=\"1.0\"?><methodResponse><params><param><value><boolean>[ANSWER]</boolean></value></param></params></methodResponse>".Replace("[ANSWER]", answer ? "1": "0");
            } catch(Exception ex)
            {
                return getErrorResponse(ex.Message);
            }
        }

        private double? parseNillableDouble(XPathNavigator node)
        {
            if(!node.InnerXml.Contains("nil"))
            {
                return node.SelectSingleNode(".//double").ValueAsDouble;
            }

            return null;
        }

        private string processPlayRequest(XPathNavigator navigator)
        {
            Board board = parseBoard(navigator);
            int player = navigator.SelectSingleNode("//param[2]//value//int").ValueAsInt;
            int step = navigator.SelectSingleNode("//param[3]//value//int").ValueAsInt;
            double? time_left = parseNillableDouble(navigator.SelectSingleNode("//param[4]//value"));

            try
            {
                Move answer = this.bot.play(board, player, step, time_left);
                return "<?xml version=\"1.0\"?><methodResponse><params><param><value><array><data><value><string>[TYPE]</string></value><value><int>[X]</int></value><value><int>[Y]</int></value></data></array></value></param></params></methodResponse>"
                    .Replace("[TYPE]", answer.type)
                    .Replace("[X]", answer.position.x.ToString())
                    .Replace("[Y]", answer.position.y.ToString());
            }
            catch (Exception ex)
            {
                return getErrorResponse(ex.Message);
            }
        }

        private string getErrorResponse(string message)
        {
            return "<?xml version=\"1.0\"?><methodResponse><fault><value><struct><member><name>faultCode</name><value><int>18</int></value></member><member><name>faultString</name><value><string>[Exception]</string></value></member></struct></value></fault></methodResponse>".Replace("[Exception]", message);
        }

        private Board parseBoard(XPathNavigator navigator)
        {
            Board board = new Board();
            board.size = navigator.SelectSingleNode("//param[1]//member[1]/value/int").ValueAsInt;
            board.rows = navigator.SelectSingleNode("//param[1]//member[2]/value/int").ValueAsInt;
            board.cols = navigator.SelectSingleNode("//param[1]//member[3]/value/int").ValueAsInt;
            board.starting_walls = navigator.SelectSingleNode("//param[1]//member[4]/value/int").ValueAsInt;
            board.pawns = parseArrayOfPositions(navigator.Select("//param[1]//member[5]//value//value//value")).ToArray();
            board.goals = parseArrayOfPositions(navigator.Select("//param[1]//member[6]//value//value//value")).ToArray();
            board.nb_walls = parseArrayOfNumbers(navigator.Select("//param[1]//member[7]//value//value")).ToArray();
            board.horiz_walls = parseArrayOfPositions(navigator.Select("//param[1]//member[8]//value//value//value")).ToArray();
            board.verti_walls = parseArrayOfPositions(navigator.Select("//param[1]//member[9]//value//value//value")).ToArray();

            return board;
        }

        private List<Position> parseArrayOfPositions(XPathNodeIterator node)
        {
            List<Position> positions = new List<Position>();

            while (node.MoveNext())
            {
                Position position = new Position();
         
                position.x = parseNillableInt(node);
                node.MoveNext();
                position.y = parseNillableInt(node);

                positions.Add(position);
            }

            return positions;
        }

        private List<int> parseArrayOfNumbers(XPathNodeIterator node)
        {
            List<int> numbers = new List<int>();

            while (node.MoveNext())
            {
                if (!node.Current.InnerXml.Contains("nil"))
                {
                    numbers.Add(node.Current.SelectSingleNode("./int").ValueAsInt);
                }
            }

            return numbers;
        }

        private int? parseNillableInt(XPathNodeIterator node)
        {
            if (!node.Current.InnerXml.Contains("nil"))
            {
                return node.Current.SelectSingleNode("./int").ValueAsInt;
            }

            return null;
        }
    }
}