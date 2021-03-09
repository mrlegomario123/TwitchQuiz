<?php

require_once('phpwebsockets/websockets.php');

class wsuser extends WebSocketUser {
    public $myId;

    function __construct($id, $socket) {
        parent::__construct($id, $socket);
    }
}

class twitchSocketServer extends WebSocketServer
{

    function __construct($addr, $port, $bufferLength = 2048) {
        parent::__construct($addr, $port, $bufferLength);
        $this->userClass = 'wsuser';
    }

    /* Incoming socket message */
    protected function process( $user, $message ) {
		echo "message = $message";
    }

    public function send_message( $user, $mess ) {
        $response = $mess->socketencode();
        $this->send($user, $response);
    }

    protected function connected($user) {
		echo "Connected";
	}
    
    protected function closed($user) {
		echo "Closed";
	}

}
