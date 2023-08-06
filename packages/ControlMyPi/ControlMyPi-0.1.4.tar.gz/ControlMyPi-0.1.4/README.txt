=============
Control My Pi
=============

`ControlMyPi <http://www.controlmypi.com>`_ provides a web based service to allow simple Python 
scripts to be controlled from a panel over the Internet. Your 
Python script defines a widget layout of labels, buttons, status 
indicators and more for ControlMyPi to display. When a button is 
clicked your script will get a message. If you have some status to 
report, your script can send that to ControlMyPi at any time and 
it'll be pushed out to your web browser. 

Simple echo example::

	import logging
	from controlmypi import ControlMyPi
	
	def on_msg(conn, key, value):
		if key == 'echobox':
			conn.update_status({'echo':'Echo: '+value})
	
	logging.basicConfig(level=logging.ERROR)
	p = [ [ ['E','echobox','send'],['S','echo','-'] ] ]
	conn = ControlMyPi('jid@dom.com', 'pwd', 'tiny', 'Tiny', p, on_msg)
	if conn.start_control():
		try:
			raw_input("Press Enter to finish\n")
		finally:
			conn.stop_control()

Please read the documentation links on `ControlMyPi <http://www.controlmypi.com>`_ for more help.
