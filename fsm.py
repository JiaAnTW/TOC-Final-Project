from transitions.extensions import GraphMachine
import datetime
import threading
from utils import send_text_message, send_template_message,active_send_text_msg
from msg_pool import *


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.timer=datetime.timedelta(hours=0,minutes = 0, seconds = 0)
        self.number={"now":0,"target":0}
        self.clock={"set":False, "time":datetime.timedelta(minutes = 0, seconds = 0)}
        self.threadPool=[]

    # center
    def is_going_to_center(self,*arg):
        return True

    def on_enter_center(self, event):
        reply_token = event.reply_token
        send_template_message(reply_token, get_center_msg())

    def on_exit_center(self,event):
        print("Leaving state1")

    # setClock
    def is_going_to_setClock(self, event):
        text = event.message.text
        print("開啟自訂計時\n")
        return text.lower() == "開啟自訂計時"


    def on_enter_setClock(self, event):
        reply_token = event.reply_token
        send_template_message(reply_token, get_set_clock_msg(self.timer,self.number))
        #self.go_back()

    def on_exit_setClock(self,event):
        if(event.message.text=="確定送出"):
            tmp=threading.Thread(target =  active_send_text_msg, args = (event.source.user_id,"排到了歐!",self.timer))
            tmp.start()
            self.threadPool.append(tmp)
        print("Leaving state2")
        return

    # setTime
    def is_going_to_setTime(self, event):
        text = event.message.text
        print("直接輸入時間\n")
        return text.lower() == "直接輸入時間"


    def on_enter_setTime(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入時間,例如3分12秒為「 3：12 」")
        #self.go_back()

    def on_exit_setTime(self,event):
        content=event.message.text.split(":")
        self.timer=datetime.timedelta(hours=0,minutes = int(content[0]), seconds = int(content[1]))
        print(event.message.text.split(":"))
        print("Leaving state2")

    #clockCenter
    def is_going_to_clockCenter(self, event):
        text = event.message.text
        print("enter cycle\n")
        return text.lower() == "設定時間"

    def cycle_in_clockCenter(self, event):
        text = event.message.text
        date = datetime.datetime.now()
        self.clock['set']=True
        self.clock['time']=datetime.timedelta(hours=date.hour,minutes = date.minute, seconds = date.second)
        return text.lower() == "開始計時"


    def on_enter_clockCenter(self, event):
        reply_token = event.reply_token
        send_template_message(reply_token, get_set_clockCenter_msg(self.timer,self.clock["set"]))
        #self.go_back()

    def on_exit_clockCenter(self,event):
        if event.message.text =="結束計時":
            date = datetime.datetime.now()
            tmp = self.clock['time']
            self.clock['time']=datetime.timedelta(hours=date.hour,minutes = date.minute, seconds = date.second)-tmp
            self.clock['set']=False
            self.timer=self.clock['time']
        print("Leaving clockCenter")

    #setNumber

    def is_going_to_setNumber(self, event):
        text = event.message.text
        print("設定號碼牌\n")
        return text.lower() == "設定號碼牌"


    def on_enter_setNumber(self, event):
        reply_token = event.reply_token
        send_template_message(reply_token, get_set_number_msg(self.number))
        #self.go_back()

    def on_exit_setNumber(self,event):
        print("Leaving setNumber")


    def is_going_to_setTarget(self, event):
        text = event.message.text
        print("設定你的號碼\n")
        return text.lower() == "設定你的號碼"


    def on_enter_setTarget(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入您的號碼（阿拉伯數字）")
        #self.go_back()

    def on_exit_setTarget(self,event):
        self.number['target']=int( event.message.text)  
        print("Leaving setTarget")
    
    def is_going_to_setNow(self, event):
        text = event.message.text
        print("設定目前號碼\n")
        return text.lower() == "設定目前號碼"

    def on_enter_setNow(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入目前的號碼（阿拉伯數字）")
        #self.go_back()

    def on_exit_setNow(self,event):
        self.number['now']=int( event.message.text)  
        print("Leaving setNow")
