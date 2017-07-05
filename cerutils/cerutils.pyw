#coding=utf-8
from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog
from mhcp import MHCP001

tk=Tk()
tk.title('MHCP Utility')

book=Notebook(tk)
cmdf=Frame(book)
evalf=Frame(book)
execf=Frame(book)
playerf=Frame(book)

server=StringVar(value='127.0.0.1')
result=StringVar(value='Powered by MHCP001.')
evalvar=StringVar()
evaltext=Text(evalf,font='Consolas -12')
mhcp=MHCP001(
    dialog=simpledialog,
    servervar=server,
    resultvar=result,
    evalvar=evalvar,
    evaltext=evaltext,
)

tk.rowconfigure(1,weight=1)
tk.columnconfigure(0,weight=1)

Entry(tk,textvariable=server).grid(row=0,column=0,sticky='we')

book.grid(row=1,column=0,sticky='nswe')

book.add(cmdf,text='Command') #####
cmdf.columnconfigure(0,weight=1)

for ind,(k,vs) in enumerate(mhcp.cmds):
    lf=LabelFrame(cmdf,text=k)
    lf.grid(row=ind,column=0,sticky='we')
    for col,v in enumerate(vs):
        Button(lf,text=v,command=mhcp.runner(k,v)).grid(row=0,column=col)

book.add(evalf,text='Evaluate') #####
evalf.columnconfigure(0,weight=1)
evalf.rowconfigure(1,weight=1)

evalentry=Entry(evalf,textvariable=evalvar,font='consolas')
evalentry.grid(row=0,column=0,sticky='we')
evalentry.bind('<Return>',lambda _:mhcp.submit_eval())
evaltext.grid(row=1,column=0,sticky='nswe')
evaltext.tag_configure('prompt',foreground='#777777')
evaltext.tag_configure('input',foreground='#0000ff')

book.add(execf,text='Execute') #####
execf.columnconfigure(0,weight=1)
execf.rowconfigure(0,weight=1)

exect=Text(execf,font='Consolas')
with open('exec.default.txt') as f:
    exect.insert('end',f.read())
exect.grid(row=0,column=0,sticky='nswe')

def submit_exec():
    result.set(
        mhcp.post_cmd('eval', 'exec(%r)' % exect.get(1.0, 'end'))
    )

exect.bind('<Shift-Return>',lambda _:'break'+('' if submit_exec() else ''))

Button(execf,text='Run',command=submit_exec).grid(row=1,column=0,sticky='we')

##### end

Label(tk,textvariable=result,width=20).grid(row=2,column=0,sticky='we')

mhcp.init_auth(
    simpledialog.askstring('MHCP','Username'),
    simpledialog.askstring('MHCP','Password'),
)

tk.bind('<Escape>',lambda _:result.set(''))
mainloop()