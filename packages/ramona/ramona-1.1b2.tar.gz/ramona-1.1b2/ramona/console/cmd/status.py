import json, time, itertools, collections, logging
from ... import cnscom
from ._completions import complete_ident

###

name = 'status'
cmdhelp = 'Show status of program(s)'

###

L = logging.getLogger('status')

###

def init_parser(parser):
	parser.add_argument('program', nargs='*', help='Optionally specify program(s) in scope of the command. If none is given, all programs are considered in scope')

###

def complete(console, text, line, begidx, endidx):
	textst = text.strip()
	ret = []
	ret.extend(complete_ident(console, textst))
	return ret

###

def main(cnsapp, args):
	params={}
	if len(args.program) > 0: params['pfilter'] = args.program
	ret = cnsapp.cnssvrcall(
		cnscom.callid_status, 
		json.dumps(params),
		auto_connect=True
	)

	status = json.loads(ret)
	
	for sp in status:

		details = collections.OrderedDict()

		exit_status = sp.pop('exit_status', None)
		if exit_status is not None: details["exit_status"] = exit_status

		pid = sp.pop('pid', None)
		if pid is not None: details["pid"] = pid

		details['launches'] = sp.pop('launch_cnt','')

		t = sp.pop('start_time', None)
		if t is not None: details["start_time"] = time.strftime("%d-%m-%Y %H:%M:%S",time.localtime(t))

		t = sp.pop('exit_time', None)
		if t is not None: details["exit_time"] = time.strftime("%d-%m-%Y %H:%M:%S",time.localtime(t))

		# Format uptime
		t = sp.pop('uptime', None)
		if t is not None:
			# TODO: Print pretty (e.g. uptime:2d 2h)
			details['uptime'] = "{0:.2f}s".format(t)

		state = sp.pop('state')
		stlbl = cnscom.program_state_enum.labels.get(state, "({0})".format(state))

		line = "{0:<16} {1:<10}".format(
			sp.pop('ident', '???'), 
			stlbl,
			)

		line += ', '.join(['{0}:{1}'.format(k,v) for k,v in itertools.chain(details.iteritems(), sp.iteritems())])
			

		print line
