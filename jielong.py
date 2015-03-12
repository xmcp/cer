# coding=utf-8
import cherrypy
from mako.template import Template
import os
import sys
import json
import time

server_path=os.path.split(sys.argv[0])[0]

def auth(gnumber):
    if 'gnumber' in cherrypy.session:
        if cherrypy.session['gnumber']!=gnumber:
            del cherrypy.session['gnumber']
            return False
        else:
            return 'name' in cherrypy.session
    return False

class JieLong:
    playing=False
    game_number=0
    waiting_list={}

    def refresh_waiting_list(self):
        time_limit=time.time()-3
        for name in tuple(self.waiting_list):
            if self.waiting_list[name]['time']<time_limit:
                del self.waiting_list[name]

    @cherrypy.expose
    def index(self):
        if self.playing:
            raise cherrypy.HTTPRedirect('/game')
        else:
            raise cherrypy.HTTPRedirect('/join')

    @cherrypy.expose
    def join(self):
        cherrypy.session['gnumber']=self.game_number
        return Template(filename=os.path.join(server_path,'template/join.mako'),input_encoding='utf-8').render()

    @cherrypy.expose
    def ping(self,status,name):
        self.refresh_waiting_list()
        if status!='idle':
            if name not in self.waiting_list:
                self.waiting_list[name]={'name':name,'time':time.time(),'okay':status=='okay'}
                cherrypy.session['gnumber']=self.game_number
                cherrypy.session['name']=name
            else:
                tmp=self.waiting_list[name]
                tmp['time']=time.time()
                tmp['okay']=status=='okay'
        return json.dumps(list(self.waiting_list.values()))

cherrypy.quickstart(JieLong(),'/',{
    'global': {
         'engine.autoreload.on':False,
        'server.socket_host':'0.0.0.0',
        'server.socket_port':7654,
    },
    '/': {
        'tools.sessions.on':True,
    },
})