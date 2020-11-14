from bluetooth import *
import pymysql

def openDoorLock(client_socket): #manualMode
    client_socket.send("o")
    print("Finished")

def selectKey(client_socket):
    client_socket.send("r") #reset-
    conn = pymysql.connect(host='192.168.225.49', user='root', password='tjdgk7518', db='SmartHome', charset='utf8')
    curs=conn.cursor(pymysql.cursors.DictCursor)
    sql = "select RfidKey from doorLockKey where model='DL-01'"
    curs.execute(sql)
    rows = curs.fetchall()
    print(rows)
    for row in rows:
        print(row['RfidKey'])
        client_socket.send(row['RfidKey'])
    
    conn.close()
    print("Finished")
def insertKey(client_socket):
    client_socket.send("i")
    print("Finished")