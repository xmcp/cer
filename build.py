#coding=utf-8
import os,shutil
from cx_Freeze import setup, Executable
base = None
executables = [Executable(script='cer.py',
               base=base,
               targetName="Cer.exe",
               compress=True)]
setup(name='cer',
      version='1.0',
      description='史诗级网游',
      options = {"build_exe":{"optimize": 2,'includes' : 'cherrypy.wsgiserver'}},
      executables=executables)
      
print('===== CLEANING UP =====')

os.remove('build/exe.win32-3.4/_ssl.pyd')
shutil.copytree('static','build/exe.win32-3.4/static')
shutil.copytree('template','build/exe.win32-3.4/template')
shutil.copyfile('dict.txt','build/exe.win32-3.4/dict.txt')
shutil.copyfile('config.py','build/exe.win32-3.4/config.py')
