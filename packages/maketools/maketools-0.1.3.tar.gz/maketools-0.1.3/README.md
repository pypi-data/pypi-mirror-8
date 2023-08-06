Python maketools
=============

Customisable build targets for python.

Basic Usage
------------

Define a target by subclassing the Target class
```
from maketools import Target

class MyTarget(Target):
	sh_build_commands = ('ls -la',
						 'mkdir test',
						 'echo {VARIABLE}')

	depends = ('requirements.txt')
	output = 'myfile.txt'

# And when you're ready to use it
top_target = MyTarget()
top_target.build(format_dict={'VARIABLE': 'HELLO'})

```

For further documentation of the Target class, see [readthedocs](http://python-maketools.readthedocs.org/en/latest/). It has a few more options for extendability. 


Advanced Target
-----------------

```
from maketools import Target

class MyOtherTarget(Target):
	# Define another target just to use it as a dependency. 
	pass

class MyTarget(Target):
	sh_build_commands = ('ls -la',
						 'mkdir test')
	depends = ('requirements.txt')
	output = 'myfile.txt'
	echo = True
	always_build = False
	depends = (MyOtherTarget, 'requirements.txt')

	def py_build_commands()
		print ("Do something in python")
```