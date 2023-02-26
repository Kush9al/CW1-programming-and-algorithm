import socket,sys,threading,time
from tkinter import *

#Scan Variable
ip_start=1
ip_finish=1024
log= []  #scan file save
ports =[]
target="localhost" #defining target
#Scanning Function
def Scanport(target, port):
    try:   #function run on a inside of thread
        s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(4)
        c=s.connect_ex((target,port))
        if c==0:
            m="port%d\t[open]" %(port,)
            log.append(m)
            ports.append(port)
            listbox.insert("end",str(m))
            updateResult()
            s.close()
    except OSError:print("> Too many open sockets. Port"+str(port))
    except:
        c.close()
        s.close()
        sys.exit()
    sys.exit()
def updateResult():
        rtext="[" +str(len(ports)) + "/" +str(ip_finish) +"]~" +str(target)
        result1.configure(text=rtext)
def startScan():
    global ports, log, target, ip_finish
    clearScan()
    log=[]
    ports=[]
#Get Ports ranges fro GUI
    ip_start=int(entry1.get())
    ip_finish=int(entry2.get())
       
#Start Writing the log file
    log.append(">Port Scanner")
    log.append("="*14 + "\n")
    log.append("Target:\t"+ str(target))
    
    try:
        target=socket.gethostbyname(str(L22.get()))
        log.append("IP ADRESS:\t"+ str(target))
        log.append("Ports:\t"+ str(ip_start)+ "/"+str(ip_finish)+"]")
        log.append("\n")
    
       #Lets start scanning Ports
        while ip_start <=ip_finish:
            try:
             scan= threading.Thread(target=Scanport, args=(target, ip_start))
             scan.setDaemon(True)
             scan.start()
            except:time.sleep(0.01)
            ip_start +=1
    except:
        m="> Target" +str(target.get()) + "not found:"
        log.append(m)
        listbox.insert(0,str(m))
             
    def saveScan():
     global log,target,ports,ip_finish
    log[5]="Results:\t[" + str(len(ports)) + "/" + str(ip_finish) +"]\n"
    with open("portscan-"+str(target)+".txt", mode="wt",encoding="utf-8") as myfile:
        myfile.write("\n".join(log))
       
def clearScan():
    listbox.delete(0,'end')
        
        
def saveScan():
    print("saving Scan")

#GUI
gui=Tk()
gui.title("Port Scanner By Kushal")
gui.geometry("400x600+20+20")

#colors
m1c = '#00ee00'
bgc = '#222222'
dbg = '#000000'
fgc = '#111111'

gui.tk_setPalette(background=bgc, foreground=m1c, activeBackground=fgc,activeForeground=bgc, highlightColor=m1c, highlightBackground=m1c)

#Labels
heading= Label(gui,text="Port scanner",font=("Times New Roman",18, "bold" ))
heading.place(x=18, y=10)

target= Label(gui,text="Target",font=("Times New Roman",18, "bold" ))
target.place(x=18, y=90)

L22= Entry(gui,text="localhost",font=("Times New Roman",18,))
L22.place(x=180, y=90)
L22.insert(0, "localhost")

portno = Label(gui, text="Port:")
portno.place(x=18,y=158)

entry1 = Entry(gui, text="1")
entry1.place(x=180, y=158,width=95)
entry1.insert(0,"1")

entry2 = Entry(gui, text="1024")
entry2.place(x=290, y=158,width=95)
entry2.insert(0,"1024")

result= Label(gui, text = "Details:")
result.place(x=16, y=220)
result1=Label(gui,text="[...]")
result1.place(x=180, y=220)

#Ports List
frame=Frame(gui)
frame.place(x=18,y=275,width=370,height=215)
listbox= Listbox(frame, width=59, height=6)
listbox.place(x=0, y=0)
listbox.bind("<<ListboxSelect>>")
scrollbar= Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

#Buttons/Scans
button1= Button(gui, text="Start Scan", command=startScan)
button1.place(x=18, y=500, width= 170)
button2= Button(gui, text="Save Details", command=saveScan)
button2.place(x=210, y=500, width= 170)

#Start GUI
gui.mainloop()
