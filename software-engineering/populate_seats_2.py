from Seat2 import Seat
import pymysql

# Connect to users database
con = pymysql.connections.Connection(user='root', password='TopSpotAWS',
                              host='topspot.cbjrgugeafkg.us-east-1.rds.amazonaws.com',
                              database='topspot')


def delete_all_seats():
    print("deleting all seats")

    cursor = con.cursor()
    sql = "DELETE FROM Seats"
    cursor.execute(sql)

    con.commit()
    con.close()



data = []
#changed floor one to have 62 seats instead of 63
cap = [63, 53, 22, 0, 43]

GroundFloorSpots = ["1,1", "1,2","1,5" , "1,6","1,10", "1,11","1,14","1,15","2,1","2,2","2,5","2,6","2,10","2,11","2,14","2,15", "4,1","4,5","4,6","4,10","4,11","4,15","5,1", "5,5", "5,6", "5,10", "5,11", "5,15", "7,1", "7,5", "7,6", "7,10", "7,11", 
"7,15", "8,1", "8,5", "8,6", "8,10", "8,11", "8,15", "10,1", "10,2", "10,5", "10,6", "10,10", "10,11", "10,14","10,15", "12,1", "12,2", "12,5", "12,6", "12,10", "12,11", "12,14", "12,15", "15,1", "15,3", "15,5", "15,11", "15,13", 
"15,15"]

FirstFloorSpots = ["1,1","1,2","1,14","1,15","2,1","2,2","2,4","2,5","2,11","2,12","2,14","2,15","3,4","3,5","3,11","3,12","4,1","4,2","4,14","4,15","5,1","5,2","5,4","5,5","5,11","5,12","5,14","5,15","6,4","6,5","6,11","6,12","7,1","7,2","7,14","7,15",
"8,1","8,2","8,14","8,15","9,4","9,12","10,4","10,12","11,1","11,15","12,4","12,12","13,1","13,4","13,12","13,15"]

SecondFloorSpots = ["2,5","2,6","2,8","2,10","2,11","3,2","3,14","4,2","4,14","6,2","6,14","7,2","7,14","9,2","9,14","10,2","10,14","12,2","12,14","13,2","13,14"]


FourthFloorSpots = ["2,1","2,3","2,4","2,5","2,7","2,8","2,9","2,11","2,12","2,13","2,15","4,1","4,3","4,4","4,5","4,7","4,8","4,9","4,11","4,12","4,13","4,15",
"6,1","6,3","6,4","6,12","6,13","6,15","8,1","8,3","8,4","8,12","8,13","8,15","10,1","10,3","10,4","10,12","10,13","10,15","12,1","12,15"]
#print(len(GroundFloorSpots))

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
            
        if(x == 0):
            s = Seat(s_id, x, GroundFloorSpots[y-1])
        elif x == 1:
            s = Seat(s_id, x, FirstFloorSpots[y-1])
        elif x == 2:
            s = Seat(s_id, x, SecondFloorSpots[y-1])
        elif x == 3:
            s = Seat(s_id, x, "")
        elif x == 4:
            s = Seat(s_id, x, FourthFloorSpots[y-1])    
        data.append(s.__dict__)


cursor = con.cursor()

cursor.executemany("""
    INSERT INTO Seats (seat_id, floor_id, occupied, user_id, outlet, location) #row_loc, col_loc)
    VALUES (%(seat_id)s, %(floor_id)s, %(occupied)s, %(user_id)s, %(outlet)s, %(location)s)""",data) #, %(row_loc)s, %(col_loc)s)""", data)

con.commit() 
con.close()

