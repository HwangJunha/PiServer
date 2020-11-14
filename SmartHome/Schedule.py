import schedule
import time
import pymysql
import AirCleanerBluetooth
import MoodLightBluetoothRoom1 #room1 modeLight
import SmartWindow
import HumidifierBluetooth
import FlowerpotBluetooth
import socket
class UserAI:
    def __init__(self, bluetoothDic):
        self.bluetoothDic=bluetoothDic
    def AisetSelect():
        conn = pymysql.connect(host='ip', user='id', password='pwd', db='dbname', charset='utf8')
        curs=conn.cursor(pymysql.cursors.DictCursor)
        sql = "select*from defaultRole"
        curs.execute(sql)
        rows = curs.fetchall()
        Aiset=[]
        print(rows)
        for row in rows:    
            line=[row['model'],row['temperature'],row['temperature_rule'],row['dust'],row['dust_rule'],row['humidity'],row['humidity_rule'],row['onoff'],row['day'],row['time'],row['aiInterval'],row['execution']]
            Aiset.append(line)

        conn.close()
        print("Finished")
        print(Aiset)
        return Aiset
    def currentData(room):
        conn = pymysql.connect(host='ip', user='id', password='pwd', db='dbname', charset='utf8')
        curs=conn.cursor(pymysql.cursors.DictCursor)
        print(room)
        sql = "select*from deviceData where number=(select MAX(number) from deviceData where room="+"'"+room+"'"+" group by room)"
        curs.execute(sql)
        rows = curs.fetchall()
        line=[]
        print(rows)
        for row in rows:    
            line=[row['temperature'],row['dust'],row['humidity']]
        
        conn.close()
        print("Finished")
        print(line)
        return line
    def counter(hour,minute,minuteAdd):
        minute += minuteAdd
        hour += minute / 60
        minute %= 60
        hour %= 24
        return int(hour), int(minute)
    def jobA(self):
        print(self.bluetoothDic)
    
    
    def timeCondition(self, condition, day, model, action, interval,sensor, Scondition):
        if condition == 'none':
            current=time.strftime('%H:%M', time.localtime(time.time())) #현재 시간 저장
            hour, minute=current.split(":")
            hour, minute=UserAI.counter(int(hour), int(minute),int(interval))
            if hour >= 0 and hour <10:
                hour='0'+str(hour)
            if minute >= 0 and minute <10:
                minute='0'+str(minute)
            
            current=str(hour)+":"+str(minute)
            print('current')
            print(current)
            UserAI.dayCondition(self,current,day,model,action, sensor, Scondition)
        else:
            UserAI.dayCondition(self,condition,day,model,action, sensor, Scondition)
            
    def dayCondition(self, startTime,day, model, action, sensor, condition):
        if day == '월':
            schedule.every().monday.at(startTime).do(UserAI.sensorCondition,self,model,action,sensor,condition) #월요일 등록시간
        elif day == '화':
            schedule.every().tuesday.at(startTime).do(UserAI.sensorCondition,self,model,action,sensor,condition) #화요일 등록시간
        elif day == '수':
            schedule.every().wednesday.at(startTime).do(UserAI.sensorCondition,self,model,action,sensor,condition) #수요일 등록시간        
        elif day == '목':
            schedule.every().thursday.at(startTime).do(UserAI.sensorCondition,self,model,action,sensor,condition) #목요일 등록시간
        elif day == '금':
            schedule.every().friday.at(startTime).do(UserAI.sensorCondition,self,model,action,sensor,condition) #금요일 등록시간
        elif day == '토':
            schedule.every().saturday.at(startTime).do(UserAI.sensorCondition,self,model,action,sensor,condition) #토요일 등록시간
        elif day == '일':
            schedule.every().sunday.at(startTime).do(UserAI.sensorCondition,self,model,action,sensor,condition) #일요일 등록시간
    
    def sensorCondition(self, model, action, sensor,condition):
        data=UserAI.currentData('room1')
        
        if condition[0] == 'up' and condition[1] == 'up' and condition[2] == 'up':
            if data[0] >= sensor[0] and data[1] >= sensor[1] and data[2] >= sensor[2]:
                UserAI.weekCondition(self,model, action)
        elif condition[0] == 'up' and condition[1] == 'up' and condition[2] == 'down':
            if data[0] >= sensor[0] and data[1] >= sensor[1] and data[2] < sensor[2]:
                UserAI.weekCondition(self,model, action)
        elif condition[0] == 'up' and condition[1] == 'down' and condition[2] == 'up':
            if data[0] >= sensor[0] and data[1] < sensor[1] and data[2] >= sensor[2]:
                UserAI.weekCondition(self,model, action)
        elif condition[0] == 'up' and condition[1] == 'down' and condition[2] == 'down':
            if data[0] >= sensor[0] and data[1] < sensor[1] and data[2] < sensor[2]:
                UserAI.weekCondition(self,model, action)
        elif condition[0] == 'down' and condition[1] == 'up' and condition[2] == 'up':
            if data[0] < sensor[0] and data[1] >= sensor[1] and data[2] >= sensor[2]:
                UserAI.weekCondition(self,model, action)
        elif condition[0] == 'down' and condition[1] == 'up' and condition[2] == 'down':
            if data[0] < sensor[0] and data[1] >= sensor[1] and data[2] < sensor[2]:
                UserAI.weekCondition(self,model, action)
        elif condition[2] == 'down' and condition[1] == 'down' and condition[2] == 'up':
            if data[0] < sensor[0] and data[1] < sensor[1] and data[2] >= sensor[2]:
                UserAI.weekCondition(self,model, action)
        elif condition[2] == 'down' and condition[1] == 'down' and condition[2] == 'down':
            if data[0] < sensor[0] and data[1] < sensor[1] and data[2] < sensor[2]:
                UserAI.weekCondition(self,model, action)
    
    def weekCondition(self, model, action):
        A, B=model.split("-")
        if A == 'ACL':
            UserAI.ACLProduct(self, model,action)
        elif A == 'ML':
            UserAI.MLProduct(self, model,action)
        elif A == 'SW':
            UserAI.SWProduct(self, model, action)
        elif A == 'HF':
            UserAI.HFProduct(self, model, action)
        elif A == 'FP':
            UserAI.FPProduct(self, model, action)
    
    def FPProduct(self, model, action):
        print('-----CHECK-----')
        print(self.bluetoothDic[model])
        
        #블루투스 bluetoothDic[model]
        if action == 'ON': 
            FlowerpotBluetooth.onMode(self.bluetoothDic[model])
        else:
            FlowerpotBluetooth.offMode(self.bluetoothDic[model])
    
    def HFProduct(self, model, action):
        print('-----CHECK-----')
        print(self.bluetoothDic[model])
        
        #블루투스 bluetoothDic[model]
        if action == 'ON': 
            HumidifierBluetooth.onMode(self.bluetoothDic[model])
        else:
            HumidifierBluetooth.offMode(self.bluetoothDic[model])
    
    def ACLProduct(self, model, action):
        print('-----CHECK-----')
        print(self.bluetoothDic[model])
       
        if action == 'ON': 
            AirCleanerBluetooth.onMode(self.bluetoothDic[model]) #월요일 등록시간
        else:
            AirCleanerBluetooth.offMode(self.bluetoothDic[model]) #월요일 등록시간
        
    def MLProduct(self, model, action):
            #블루투스 bluetoothDic[model]
        if action == 'ON': 
            MoodLightBluetoothRoom1.onLight(self.bluetoothDic[model]) #월요일 등록시간
        else:
            MoodLightBluetoothRoom1.offLight(self.bluetoothDic[model]) #월요일 등록시간
        
    def SWProduct(self, model, action):
            #블루투스 bluetoothDic[model]
        if action == 'ON':
            SmartWindow.manualMode(self.bluetoothDic[model])
            SmartWindow.openWindow(self.bluetoothDic[model]) #월요일 등록시간
        else:
            SmartWindow.manualMode(self.bluetoothDic[model]) #월요일 등록시간
            SmartWindow.closeWindow(self.bluetoothDic[model])
        
    def AIStart(self):
        Aiset=UserAI.AisetSelect()
        print(Aiset)
        for i in Aiset:
            if i[11] == 0: #0 비활성화 1활성화
                continue 
            sensor=[i[1],i[3],i[5]]
            condition=[i[2],i[4],i[6]]
           
            UserAI.timeCondition(self,i[9], i[8], i[0], i[7],i[10],sensor,condition)
            
        while True:
            schedule.run_pending()
            time.sleep(1)
