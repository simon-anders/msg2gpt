import sys, struct, json

with open( "/home/anders/tmp/prm/tmpr33zjgwa" ) as f:
	m = f.read()

s = json.dumps( { "task": "write_to_tmp_log", "message": m } ).encode('ascii')
sys.stdout.buffer.write( struct.pack( "=I", len(s) ) )
sys.stdout.buffer.write( s )
