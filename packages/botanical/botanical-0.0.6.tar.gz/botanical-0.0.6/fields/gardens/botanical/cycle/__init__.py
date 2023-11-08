

import time

'''
	cycle.presents ([])
	cycle.presents ([], {})
'''
class presents:
	def __init__ (this, * positionals):
		this.positionals = positionals [0]
		
		if (len (positionals) >= 2):
			this.keywords = positionals [1]
		else:
			this.keywords = {}


def params (
	fn, 
	fn_params, 
	
	delay = 1, 
	loop = 0,
	records = 0
):
	try:
		return fn (* fn_params [ loop ]);			
	except Exception as E:
		if (records >= 1):
			print ("cycle didn't work.", E)

	time.sleep (delay)
	
	return params (
		fn, 
		fn_params, 
		
		delay = delay,
		loop = loop + 1,
		records = records
	)

import botanical.modules.exceptions.parse as parse_exception

'''

'''
def loops (
	* positionals, 
	** keywords
):
	#print ("loops called")

	fn = positionals [0]
	fn_presents = positionals [1] 
	
	this_loops = keywords ["loops"],
	
	if ("loops" in keywords):
		this_loops = keywords ["loops"]
	else:
		this_loops = 1
	
	if ("delay" in keywords):
		this_delay = keywords ["delay"]
	else:
		this_delay = 1
		
	if ("records" in keywords):
		this_records = keywords ["records"]
	else:
		this_records = 0
		
	if ("loop_number" in keywords):
		this_loop_number = keywords ["loop_number"]
	else:
		this_loop_number = 1
		
	if (this_loop_number > this_loops):
		raise Exception (f"The loop limit was reached.")

	if (this_records >= 1):
		print ("at loop number ", this_loop_number, "of", this_loops)

	'''
		try the function,
			if it doesn't work 
	'''
	try:
		return fn (
			* fn_presents.positionals,
			** fn_presents.keywords
		);			
	except Exception as E:
		if (this_records >= 1):		
			print (
				"cycle didn't work, received exception", 
				parse_exception.now (E)
			)

	time.sleep (float (this_delay))
	
	keywords ["loop_number"] = this_loop_number + 1
	return loops (
		* positionals, 
		** keywords
	)
	