import pymysql



def selectKey():
    conn = pymysql.connect(host='ip', user='id', password='pwd', db='dbname', charset='utf8')
    curs=conn.cursor(pymysql.cursors.DictCursor)
    sql = "select RfidKey from doorLockKey where model='DL-01'"
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        print(row['RfidKey'])
        
    conn.close()
def insertKey(client_socket):
    client_socket.send('i')
    msg=client_socket.recv(1024)
    print("msg1")
    print(msg)
    msg+=client_socket.recv(1024)
    print("msg2")
    print(msg)
    
    """
    conn = pymysql.connect(host='192.168.219.110', user='root', password='tjdgk7518', db='SmartHome', charset='utf8')
    curs=conn.cursor()
    sql = insert into RfidKey(name, kind, model, RfidKey) values(%s, %s, %s, %s)
    curs.execute(sql, ('도어락', '도어락', 'DL-01',msg))
    conn.commit()
    conn.close()
    """
