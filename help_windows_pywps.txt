Setup PyWPS in Windows in Embedded Mode:
1. Download and Install python 3.5
2. Download and Install Microsoft visual c++ 2017
3. Install Microsoft visual compiler package for python

4. Download apache from:
https://www.apachelounge.com/download/

5. Add the following lines in httpd.conf to define SRVROOT :
Define SRVROOT "D:/abhi/workspace/pywps/apache/Apache24"
ServerRoot "${SRVROOT}"

6. To add Apache as a windows service first go to bin folder of apache and run the command :
httpd.exe -k install -n "Apache HTTP Server"  
7. Run ApacheMonitor from bin folder to select specific apache instance.


8. Create system variable MOD_WSGI_APACHE_ROOTDIR as:(this will the path of your apache rootdir)
MOD_WSGI_APACHE_ROOTDIR = D:\abhi\workspace\pywps\apache\Apache24
9. Run the following command in x64 native tool cmd version 2017:
pip install mod_wsgi
10. Run the command :
mod_wsgi-express module-config
11. Copy all the output of the above command and add it to your Apache configuration file(i.e. httpd.conf). The output of above command will look like below. In your case there might be slight change.
	LoadFile "c:/program files/python35/python35.dll"
	LoadModule wsgi_module "c:/program files/python35/lib/sitepackages/mod_wsgi/server/mod_wsgi.cp35-win_amd64.pyd"
	WSGIPythonHome "c:/program files/python35"

12. Add wsgiScriptAlias in httpd.conf as:
    WSGIScriptAlias /wsgi-bin/ "${SRVROOT}/wsgi-bin/wsgi_app.py"
    <Directory "${SRVROOT}/wsgi-bin">
    AllowOverride None
    Options None
    Require all granted
    </Directory>  
	
13. Create a file wsgi_app.py in wsgi-bin folder , wsgi-bin folder is present in Apache24 folder, along htdocs folder. Add the following in wsgi_app.py:
def application(environ, start_response):
    status = '200 OK'
    output = b'Hello World!\n'
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]
	
	
14. save and restart the apache server 
15. Run http://localhost/wsgi-bin/

16.  create folders structure inside Apache24 as:
wsgi-bin – wsgi_app.py
htdocs-
      logs - pywps.log
      outputs
      workdir
      processes - __init__.py , sayhello.py
      wsgi - pywps.wsgi
      pywps.cfg
	  
	  
17. changes made in pywps.cfg:
    [server]
    maxsingleinputsize=1mb
    maxrequestsize=3mb
    url=http://localhost:80/wps    
    outputurl=http://localhost:80/outputs/
    outputpath=outputs
    workdir=workdir
    maxprocesses=10
    parallelprocesses=2
    [logging]
    level=INFO
    file=logs/pywps.log
    database=sqlite:///logs/pywps-logs.sqlite3
    [grass]
    gisbase=D:/abhi/workspace/pywps/grass_gis.7.4.0/  
	
	
18. changes made in httpd.conf:
    WSGIScriptAlias /pywps "${SRVROOT}/htdocs/wsgi/pywps.wsgi"
    <Directory "${SRVROOT}/htdocs/wsgi">
    AllowOverride None
    Options None
    Requre all granted
    </Directory>  

	
19. pywps.wsgi:
__author__="Abhijit Ambhore"
from pywps.app.Service import Service
import sys
import os
print("")
sys.path.append("D:/abhi/workspace/pywps/apache/Apache24/htdocs")
from processes.sayhello import SayHello
processes=[SayHello()]
application=Service(processes,['pywps.cfg'])


20. WPS Requests:
a. GetCapabilities:
http://localhost/pywps?request=GetCapabilities&service=wps
b. DescribeProcess:
http://localhost/pywps?request=describeProcess&identifier=say_hello&service=WPS&version=1.0.0
c. Execute:
http://localhost/pywps?request=Execute&identifier=say_hello&datainputs=name=%22anjali%22&service=WPS&version=1.0.0

References:
https://blogs.oracle.com/oswald/good-idea:-python-with-fastcgi-modfcgid
https://www.electricmonk.nl/docs/apache_fastcgi_python/apache_fastcgi_python.html
https://stackoverflow.com/questions/12715139/python-wsgi-multiprocessing-and-shared-data
https://serverfault.com/questions/105908/how-do-you-increase-the-apache-connection-limit-wamp

Note: There steps are tested on Windows 10 64-bit PC. So, there may be some changes needed for other platforms.





