===================================
|PySTDF - The Pythonic STDF parser|
===================================
Developed by Casey Marshall <casey.marshall@gmail.com>

PySTDF is a parser for Standard Test Data Format (STDF) version 4 data files.
I wrote PySTDF to get familiar with functional programming idioms and 
metaclasses in Python.  As such, it uses some of the more powerful and 
expressive features of the Python language.

PySTDF is an event-based parser.  As an STDF file is parsed, you recieve 
record "events" in callback functions

Refer to the provided command line scripts for ideas on how to use PySTDF:

stdf2text, convert STDF to '|' delimited text format.
stdf2excel, convert STDF to MS Excel.
stdf_slice, an example of how to seek to a specific record offset in the STDF.

I have also included a very basic STDF viewer GUI, StdfExplorer.  I have plans 
to improve upon it further in Q4 2006 - Q5 2007.

=========
|INSTALL|
=========
Use the standard distutils setup.py.

On Windows: "python setup.py install"
On Unix: "sudo python setup.py install"

======
|BUGS|
======
PySTDF has no known bugs.  However, it is my experience that every ATE vendor 
has its quirks and "special interpretation" of the STDFv4 specification.

If you find a bug in PySTDF, please send me the STDF file that demonstrates it.
This will help me improve the library.

=========
|LICENSE|
=========
PySTDF is released under the terms and conditions of the GPL version 2 license.
You may freely use PySTDF, but you may not distribute it in closed-source 
proprietary applications.  Please contact me if you are interested in 
purchasing an alternative license agreement to develop commercial software 
with PySTDF.

If you need some STDF consulting/development work, I might be able to help you.
I have over 5 years experience with STDF and semiconductor data analysis 
systems.

If you're in the Austin area and just want to get some lunch, that is cool too :)

========
|THANKS|
========
Thanks for your interest in PySTDF.  You're the reason I open-sourced it.

Cheers,
Casey
