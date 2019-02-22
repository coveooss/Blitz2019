package com.coveo.rpc;

import java.util.HashMap;
import java.util.Map;
import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.server.PropertyHandlerMapping;

public class CustomPropertyHandlerMapping extends PropertyHandlerMapping {

  //This is really dumb and I hope there is a better way to do this.
  public void addHandler(String pKey, Class pClass) throws XmlRpcException {
    this.registerPublicMethods(pKey, pClass);

    //Reinsert the methods with a mapping without the preceding "className.".
    Map toAdd = new HashMap();

    for(Object objName : this.handlerMap.keySet()) {
      String name = (String) objName;
      String methodName = name.split("\\.")[1];
      toAdd.put(methodName, handlerMap.get(objName));
    }

    toAdd.entrySet().forEach((o) -> {
      Map.Entry entry = (Map.Entry)o;
      handlerMap.put(entry.getKey(), entry.getValue());
    });
  }
}
