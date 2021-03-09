<?php

require_once('twitchsocket.php');

// Run on the local machine
$sockethost = 'localhost';

// This port must match the port in the javascript
$socketport = '9006';

$socketserver = new twitchSocketServer($sockethost, $socketport);

try {
    $socketserver->run();
} catch (Exception $e) {
    $socketserver->stdout($e->getMessage());
}

function procMsg($topic, $msg) {
    global $socketserver;
    echo "Recieved mqtt : {$topic} - {$msg}\n";
    $socketserver->send_message($msg, 'usermsg');
}






