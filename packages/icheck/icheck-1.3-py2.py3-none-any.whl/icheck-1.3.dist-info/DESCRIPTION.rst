======
icheck
======

quick (or not so quick) and dirty tool to run syntax checking on python code 
in a seperate screen window

features
---------
* Call a command on syntax failures
* terminal bell
* filter files by hashbang and globs
* color output with tty detection
* multiple output formats (oneline, short and long)


This program was mainly written to assit me in devlopeing python code and 
letting me know a couple of seconds before i try and run my program that there 
are basic syntax mistakes in the code.

to achive this inotify is used to wait for files to be written to and then if 
all pre conditions are fine (globs and hashbangs) then a syntax check is 
excuted. on an error a message is printed and it moves on to the next file

By using the 'bell' facility the window running icheck does not have to be 
visible to the programmer and isntead a message will be printed in the message 
line on error indicating attention may be required, allowing screen to be used 
as the windowing component of a fleixble IDE setup



.. :changelog:

Release History
---------------

1.3 (2014-10-20)
++++++++++++++++

- Add python 2.7 compatibility

1.2.1 (2014-10-20)
++++++++++++++++

**Bug Fixes**

- Fix packaging again and convert to module, now installs correctly

1.2 (2014-10-20)
++++++++++++++++

**Bug Fixes**

- Fix packaging so setup.py is included again

1.1 (2014-10-20)
++++++++++++++++

- Change-log now appended to project description

**Bug Fixes**

- Fixed (one) race condition on checking hashbang
- Fixed up entry point to eat stack trace on Keyboard Interrupt

1.0 (2014-10-19)
++++++++++++++++

- Initial Release




