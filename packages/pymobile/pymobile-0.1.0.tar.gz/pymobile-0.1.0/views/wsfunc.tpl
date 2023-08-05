function livedatainfo(txt){
    //alert(txt);
}

function wsfunc(method, args, kwargs, onmessage){
  if ("WebSocket" in window){
        var ws = new WebSocket("ws://{{host}}:{{port}}/");
        
        ws.onopen = function(){
            ws.send(JSON.stringify([method, args, kwargs]));
        };
        
        ws.onmessage = onmessage;
        
        ws.onerror = function (evt){ 
            livedatainfo("error");
        };
        
        ws.onclose = function(){ 
            livedatainfo("Connection is closed..."); 
        };
    }
    else{
        livedatainfo("WebSocket NOT supported by your Browser!");
    }
    return ws;
}
