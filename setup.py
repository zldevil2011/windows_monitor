from distutils.core import setup 
import py2exe 
 
setup(console=[{"script" : "MonitorWin32Process.py", "icon_resources" : [(1, "logo.ico")]}],   
) 
