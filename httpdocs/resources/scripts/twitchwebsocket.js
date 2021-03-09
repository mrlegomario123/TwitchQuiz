
var websocket;

//var server_uri = "192.168.0.80";

// Run on the same machine
var server_uri = "localhost"; //look on this device
//var server_uri = "home.twitchchat.com"; //look on this device
var myid = uuidv4(); //create local id

//socket create, called at start
function screate(onopenfnc, onclosefnc, onreceivefnc) {

	//uri of the websocket server on local host
	//different to uri of website
	//can have multiple websites accesing same websocket server
	//this websocket server is stored locally
	//give it port 9006
	//e.g http: 80, https: 443, (all reserved)
	// websocket standard port: 9006
	// having many different ports => same ip adress can have different functionaonallity depending on port it comes in 
	var wsUri = "ws://" + server_uri + ":9006/";
	
	websocket = new WebSocket(wsUri);//creates websocket connection (javascript implementaion)
	//websocket is protocal so different implementaions in different languages
	//websocket is async -> non blocking, these are callbacks, want to run in background

	//on event websocket open -> run function "onopenfnc()"
	//event driven, so knows to call apropriate function 
	websocket.onopen = function(evt) { onopenfnc(evt); }; 
	websocket.onclose = function(evt) { onclosefnc(evt);  };
	//important: onmessage function from api, when incoming data from websocket, call onreceivefnc(), pass evt data
	websocket.onmessage = function(evt) { onreceivefnc(evt); };
	websocket.onerror = function(evt) { console.log('websocket error'); };

}


/**
 * Send a message over web sockets
 * 
 * @param id        use this to identify an incoming message
 * @param command   A command
 * @param payload   Extra Payload in JSON
 */

 //send message function pass unique id plus what ever data you want
 // pass in json format
function sendMessage(id, command, payload ){

	//prepare json data
	var msg = {
		xid : myid,
		id : id,
		command: command,
		payload : payload
	};

	jmsg = JSON.stringify(msg); //convert to json (string that can be passed over)
	console.log("Sending message to websocket : " + jmsg);
	websocket.send(jmsg);//send that json message
}


function socketOpen(evt){		console.log("Socket Open");} 
function socketClosed(evt){		console.log("Socket Closed");} 
function socketError(evt){		console.log("Socket Error"); }

//create unique id
function uuidv4() {
	return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
		var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
		return v.toString(16);
	});
}	
