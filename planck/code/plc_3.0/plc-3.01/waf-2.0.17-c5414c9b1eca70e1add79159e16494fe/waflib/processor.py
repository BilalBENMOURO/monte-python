#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import os,sys,traceback,base64,signal
try:
	import cPickle
except ImportError:
	import pickle as cPickle
try:
	import subprocess32 as subprocess
except ImportError:
	import subprocess
try:
	TimeoutExpired=subprocess.TimeoutExpired
except AttributeError:
	class TimeoutExpired(Exception):
		pass
def run():
	txt=sys.stdin.readline().strip()
	if not txt:
		sys.exit(1)
	[cmd,kwargs,cargs]=cPickle.loads(base64.b64decode(txt))
	cargs=cargs or{}
	if not'close_fds'in kwargs:
		kwargs['close_fds']=False
	ret=1
	out,err,ex,trace=(None,None,None,None)
	try:
		proc=subprocess.Popen(cmd,**kwargs)
		try:
			out,err=proc.communicate(**cargs)
		except TimeoutExpired:
			if kwargs.get('start_new_session')and hasattr(os,'killpg'):
				os.killpg(proc.pid,signal.SIGKILL)
			else:
				proc.kill()
			out,err=proc.communicate()
			exc=TimeoutExpired(proc.args,timeout=cargs['timeout'],output=out)
			exc.stderr=err
			raise exc
		ret=proc.returncode
	except Exception ,e:
		exc_type,exc_value,tb=sys.exc_info()
		exc_lines=traceback.format_exception(exc_type,exc_value,tb)
		trace=str(cmd)+'\n'+''.join(exc_lines)
		ex=e.__class__.__name__
	tmp=[ret,out,err,ex,trace]
	obj=base64.b64encode(cPickle.dumps(tmp))
	sys.stdout.write(obj.decode())
	sys.stdout.write('\n')
	sys.stdout.flush()
while 1:
	try:
		run()
	except KeyboardInterrupt:
		break
