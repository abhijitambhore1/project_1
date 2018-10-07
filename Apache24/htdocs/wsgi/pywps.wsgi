#!C:/Program Files/Python35/python.exe

__author__="Abhijit Ambhore"

from pywps.app.Service import Service
import sys
import os
print("")

sys.path.append("D:/abhi/workspace/pywps/apache/Apache24/htdocs")
from processes.sayhello import SayHello
processes=[SayHello()]
application=Service(processes,['pywps.cfg'])

