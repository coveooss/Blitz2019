package com.coveo.rpc;

import java.io.IOException;
import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.server.PropertyHandlerMapping;
import org.apache.xmlrpc.server.XmlRpcServer;
import org.apache.xmlrpc.server.XmlRpcServerConfigImpl;
import org.apache.xmlrpc.webserver.WebServer;

public class Blitz2k19RPCServer<A extends Agent> {

  public Blitz2k19RPCServer(Class<A> AgentClass, int port) throws XmlRpcException, IOException {
    WebServer webServer = new WebServer(port);

    XmlRpcServer xmlRpcServer = webServer.getXmlRpcServer();

    PropertyHandlerMapping phm = new CustomPropertyHandlerMapping();
    phm.addHandler("Agent", AgentClass);
    xmlRpcServer.setHandlerMapping(phm);

    XmlRpcServerConfigImpl serverConfig =
        (XmlRpcServerConfigImpl) xmlRpcServer.getConfig();
    serverConfig.setEnabledForExtensions(true);
    serverConfig.setContentLengthOptional(false);

    xmlRpcServer.setTypeFactory(new TypeFactory(xmlRpcServer));

    System.out.println("Starting the server");
    webServer.start();
  }
}
