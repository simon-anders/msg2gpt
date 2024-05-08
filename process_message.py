#!/bin/python

import sys, tempfile, struct, json

def get_task_and_message():
	raw_length = sys.stdin.buffer.read( 4 )
	message_length = struct.unpack( '=I', raw_length )[0]
	json_message = sys.stdin.buffer.read( message_length )
	message_with_task = json.loads( json_message )
	return message_with_task["task"], message_with_task["message"]


def log_message( message ):
	log = tempfile.NamedTemporaryFile( mode='w', dir="/home/anders/tmp/prm", delete=False )
	log.write( "Task: " + message["task"] + "\n" )
	log.write( message["message"] )
	log.close()


def write_to_calendar( message ):
	pass

if __name__ == "__main__":
	task, message = get_task_and_message()
	if task == "write_to_tmp_log":
		log_message( message )
	elif task == "add_to_calendar":
		write_to_calendar( message )

