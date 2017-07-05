#coding=utf-8
import requests

class MHCP001:
    cmds=[
        ('game',['start','stop','pause']),
        ('ban',['ip','name','clear']),
        ('player',['kill','heal']),
        ('set',['count','word','pos']),
        ('su',['on','off']),
    ]

    def __init__(self,dialog,servervar,resultvar,evalvar,evaltext):
        self.dialog=dialog
        self.s=requests.Session()
        self.s.trust_env=False
        self.servervar=servervar
        self.resultvar=resultvar
        self.evalvar=evalvar
        self.evaltext=evaltext

    def init_auth(self,un,pw):
        self.s.auth=(un,pw)
        
    def post_cmd(self,*args):
        try:
            return self.s.post(
                'http://'+self.servervar.get()+':7654/cardinal',
                data={
                    'cmd': ' '.join(args)
                }
            ).text
        except Exception as e:
            return '%s %s'%(type(e),e)

    def run(self,cmd1,cmd2):
        if cmd1=='player' or (cmd1=='ban' and cmd2!='clear') or cmd1=='set':
            another=self.dialog.askstring('MHCP001','%s %s'%(cmd1,cmd2))
            if another is not None:
                return self.post_cmd(cmd1,cmd2,another)
            else:
                return '(canceled)'
        else:
            return self.post_cmd(cmd1,cmd2)

    def runner(self,cmd1,cmd2):
        return lambda: self.resultvar.set(self.run(cmd1,cmd2))

    def submit_eval(self):
        arg=self.evalvar.get()
        self.evaltext.insert('end','>>> ','prompt')
        self.evaltext.insert('end',arg+'\n','input')
        self.evaltext.insert('end',self.post_cmd('eval',arg)+'\n')
        self.evaltext.see('end')