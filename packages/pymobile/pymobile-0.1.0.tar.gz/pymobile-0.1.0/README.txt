This is a startproject for web-projects using python3, bottle, jquerymobile, asyncio,
websockets and worker-threads.

Workflow:
* Web-templates should be placed in views-folder.
* Database-modules should be placed in models-folder.
* Modules for bottle and worker-threads should be placed in controllers-folder.
* Static webfiles should be placed in static-folder
* Run project with serve.py. All modules in controllers-folder is imported 
  automatically, all worker-threads is started and bottle webserver is started.

Have a look at the examples included in controllers, models and views or 
delete them if you don't need them.

DOCUMENTATION:
python3:        http://docs.python.org/3/library/index.html
bottle:         http://bottlepy.org/docs/stable/
jquerymobile:   http://view.jquerymobile.com/1.3.1/dist/demos/
shared workerthreads:
                Have a look at controllers/livecounter.py and controllers/wol.py


TIPS:

To change host or port you can create a new python-file:

: touch run.py

Then paste following text into the python-file:
---- START ----
#!/usr/bin/env python3
import serve
if __name__ == '__main__':
    serve.run(port=58580)
----- STOP ----


TIPS:

To start pym automatically at system startup you should create a new upstart conf-file:
: sudo touch /etc/init/pym.conf

Then paste following text into the conf-file:
---- START ----
# start pym

description     "pym"

start on (local-filesystems
          and started dbus
          and static-network-up)
stop on stopping dbus

exec python3 /path/to/pym/serve.py
----- STOP ----