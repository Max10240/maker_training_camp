from sakshat import SAKSHAT
import time
import threading 
from last_my_send import send_email
from last_my_recieve import recieve_email
from light_on import *
from chr_to_mp3 import change
touch_n=0
display_n=0
list_message=[]
list_light=[0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]  
SAKS=SAKSHAT()
def alarm_on():
    SAKS.buzzer.on()
    SAKS.ledrow.on_for_index(6)
    time.sleep(0.05)
    SAKS.buzzer.off()
    SAKS.ledrow.off_for_index(6)
def display_on(*args):
    if not args:
        a=list(time.localtime())[3]
        b=list(time.localtime())[4]
        SAKS.digital_display.show(("%02d%02d." % (a,b))) 
    else:
        a,b=args
        SAKS.digital_display.show(("%02d%02d." % (a,b)))
        
def my_touch(a,b):
    global touch_n
    touch_n+=1
    if  not touch_n%2:
        return
    if len(list_message)>0:
        change(list_message.pop())
        send_email('to_wechat!')
    else:
        y,m,d,h,minute=list(time.localtime())[:5]
        weekday=list(time.localtime())[6]+1
        weekday=str(weekday) if weekday!=7 else '日'
        speak_ctn='现在时间      %s年 %s月 %s日 %s点 %s分 星期%s'%(y,m,d,h,minute,weekday)
        change(speak_ctn)
        for x in list_light:
            light_on(x)
            time.sleep(0.3)
    
    '''print('I Have Been Touched!')
    #display_on()
    time.sleep(0.1)
    light_on(list_light[1])
    time.sleep(1)
    alarm_on()
    time.sleep(0.5)
    light_on(list_light[-1])
    time.sleep(1)
    #display_on(0,0)
    time.sleep(0.5)'''
    
SAKS.tact_event_handler=my_touch
def f_recieve():
    while 1:
        try:
            a=recieve_email()
        except:
            a=''
        if a and a.startswith('to_mp3'):
            list_message.append(a[6:])
            change('收到一条消息,现在您共有%s 条未读消息!'%len(list_message))
def f():
    while 1:
        if len(list_message):
            light_on(0xff)
            display_on(0,len(list_message))
        else:
            light_on(0x00)
            display_on()
        time.sleep(0.2)
if __name__=='__main__':
    threads=[]
    a=threading.Thread(target=f_recieve,args=())
    a.start()
    threads.append(a)
    a=threading.Thread(target=f,args=())
    a.start()
    threads.append(a)
    for x in threads:
        x.join()
        
