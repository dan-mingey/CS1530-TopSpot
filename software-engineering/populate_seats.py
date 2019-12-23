from Seat import Seat
import pymysql

# Connect to users database
con = pymysql.connections.Connection(user='root', password='TopSpotAWS',
                              host='topspot.cbjrgugeafkg.us-east-1.rds.amazonaws.com',
                              database='topspot')


data = []
cap = [64, 53, 22, 0, 43]
for x in range(5):
    if(x == 3):
        continue
    for y in range(cap[x]):
        if (y == 0):
            continue
        if y < 10: 
            s_id = str(x) + str(0) + str(y)
        else:
            s_id = str(x) + str(y)
        s = Seat(s_id, x)
        data.append(s.__dict__)


cursor = con.cursor()

cursor.executemany("""
    INSERT INTO Seats (seat_id, floor_id, occupied, user_id, outlet) #row_loc, col_loc)
    VALUES (%(seat_id)s, %(floor_id)s, %(occupied)s, %(user_id)s, %(outlet)s)""",data) #, %(row_loc)s, %(col_loc)s)""", data)

con.commit() 
con.close()

