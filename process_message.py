#!/bin/python

import sys, tempfile, struct, json

raw_length = sys.stdin.buffer.read( 4 )
message_length = struct.unpack( '=I', raw_length )[0]
json_message = sys.stdin.buffer.read( message_length )
message = json.loads( json_message )

log = tempfile.NamedTemporaryFile( mode='w', dir="/home/anders/tmp/prm", delete=False )
log.write( "Task: " + message["task"] + "\n" )
log.write( message["message"] )
log.close()