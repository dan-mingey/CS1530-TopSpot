from User import User
import pymysql

# Connect to users database
con = pymysql.connections.Connection(user='root', password='TopSpotAWS',
                              host='topspot.cbjrgugeafkg.us-east-1.rds.amazonaws.com',
                              database='topspot')

#insert 5 user objects into a data list
data = []
Sam = User('Sam', 'password')  
data.append(Sam.__dict__)

Jenni = User('Jenni', 'password')  
data.append(Jenni.__dict__)

Inna= User('Inna', 'password')  
data.append(Inna.__dict__)

Dan = User('Dan', 'password')  
data.append(Dan.__dict__)

Erik = User('Erik', 'password')  
data.append(Erik.__dict__)

cursor = con.cursor()

cursor.executemany("""
    INSERT INTO Users (user_id, password, seat_id)
    VALUES (%(user_id)s, %(password)s, %(seat_id)s)""", data)

con.commit() 
con.close()
