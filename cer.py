# coding=utf-8
import cherrypy
from mako.template import Template
import os
import sys
import json
import time
from config import validate

server_path=os.path.split(sys.argv[0])[0]
def post_only():
    if cherrypy.request.method.upper()!='POST':
        cherrypy.response.headers['Allow']='POST'
        raise cherrypy.HTTPError(405)
cherrypy.tools.post=cherrypy.Tool('on_start_resource',post_only)
MAXLIVE=10

def auth(gnumber):
    if 'gnumber' in cherrypy.session:
        if cherrypy.session['gnumber']!=gnumber:
            del cherrypy.session['gnumber']
            return False
        else:
            return 'name' in cherrypy.session
    return False

class Cer:
    playing=False
    game_number=time.time()%100000
    waiting_list={}
    players=[]
    current='hello'
    activeNum=0

    def refresh_waiting_list(self):
        time_limit=time.time()-3
        for name in tuple(self.waiting_list):
            if self.waiting_list[name]['time']<time_limit:
                del self.waiting_list[name]

    @cherrypy.expose()
    def index(self):
        if self.playing:
            raise cherrypy.HTTPRedirect('/game')
        else:
            raise cherrypy.HTTPRedirect('/join')

    @cherrypy.expose()
    def join(self):
        if self.playing:
            raise cherrypy.HTTPRedirect('/game')
        cherrypy.session['gnumber']=self.game_number
        return Template(filename=os.path.join(server_path,'template/join.html'),input_encoding='utf-8').render()

    @cherrypy.expose()
    @cherrypy.tools.post()
    def ping(self,status,name):
        if self.playing:
            return json.dumps({
                'error':'[start]'
            })
        self.refresh_waiting_list()
        if status!='idle':
            if name not in self.waiting_list:
                self.waiting_list[name]={'name':name,'time':time.time(),'okay':status=='okay'}
                cherrypy.session['gnumber']=self.game_number
                cherrypy.session['name']=name
            else:
                if not (auth(self.game_number) and cherrypy.session['name']==name):
                    return json.dumps({
                        'error':'昵称已经存在'
                    })
                tmp=self.waiting_list[name]
                tmp['time']=time.time()
                tmp['okay']=status=='okay'
        return json.dumps({
            'plist':list(self.waiting_list.values())
        })

    @cherrypy.expose()
    @cherrypy.tools.post()
    def start(self,name):
        before=[]
        for a in self.waiting_list.values():
            if not a['okay']:
                return '没有完全准备好'
            else:
                before.append(a['name'])
                if a['name']==name:
                    a['time']+=4
        time.sleep(4)
        self.refresh_waiting_list()
        if [a['name'] for a in self.waiting_list.values() if a['okay']]!=before:
            return '有人中途退出'
        self.players=[{'name':a,'live':MAXLIVE} for a in before]
        self.playing=True
        self.activeNum=0
        return '[okay]'

    @cherrypy.expose()
    def game(self):
        if not self.playing:
            raise cherrypy.HTTPRedirect("/join")
        return Template(filename=os.path.join(server_path,'template/game.html'),input_encoding='utf-8')\
            .render(players=self.players,username=cherrypy.session['name'] if 'name' in cherrypy.session else None,MAXLIVE=MAXLIVE)

    @cherrypy.expose()
    def gameStatus(self):
        if not auth(self.game_number):
            return json.dumps({
                'error':'Not Authed'
            })
        return json.dumps({
            'current':self.current,
            'players':self.players,
            'turn':self.players[self.activeNum]['name']
        })

    @cherrypy.expose()
    def waitStatus(self,now):
        while now==self.gameStatus():
            time.sleep(.5)
        return self.gameStatus()

    @cherrypy.expose()
    @cherrypy.tools.post()
    def enter(self,word):
        if not auth(self.game_number):
            return json.dumps({
                'error':'Not Authed'
            })
        if not self.players[self.activeNum]['name']==cherrypy.session['name']:
            return json.dumps({
                'error':'Not your turn'
            })
        msg=validate(self.current,word)
        if msg:
            return json.dumps({
                'error':msg
            })
        self.current=word
        self.activeNum=(self.activeNum+1)%len(self.players)


cherrypy.quickstart(Cer(),'/',{
    'global': {
         'engine.autoreload.on':False,
        'server.socket_host':'0.0.0.0',
        'server.socket_port':7654,
    },
    '/': {
        'tools.sessions.on':True,
        'tools.sessions.locking':'explicit',
    },
})