#map
from Seat import Seat
import pymysql

# Connect to users database
con = pymysql.connections.Connection(user='root', password='TopSpotAWS',
                              host='topspot.cbjrgugeafkg.us-east-1.rds.amazonaws.com',
                              database='topspot')


# floor_id 		- integer
# User_id		- integer
# show_map() 		- method
# get_floor_plan() 	- method
# show_friends() 	- method
# claim_seating() 	- method
# unclaim_seating() 	- method
# Get_outlets() 		- method

def refreshDatabase():
    print("refreshing the database")
    global con 
    con = pymysql.connections.Connection(user='root', password='TopSpotAWS',
                              host='topspot.cbjrgugeafkg.us-east-1.rds.amazonaws.com',
                              database='topspot')


#claims a seat
def claim_seating(user_id, seat_id):
	refreshDatabase()
	print("beginning of claim seating")
	cursor = con.cursor()

	print("updating the seat database"+str(seat_id))
	#update the seat database
	data = (user_id,seat_id)
	print("1")
	sql = "UPDATE Seats SET occupied = 1, user_id = %s WHERE seat_id = %s"
	print("2")
	cursor.execute(sql,data)
	print("3")

	print("updating the user database")
	#update the user database
	data = (seat_id,user_id)
	sql = "UPDATE Users SET seat_id = %s WHERE user_id = %s"
	cursor.execute(sql,data)
	
	con.commit()
	con.close()

	print("ending of claim seating")


#unclaims a seat
def unclaim_seating(user_id, seat_id):
	refreshDatabase()
	print("inside unclaim seating")
	cursor = con.cursor()

	print(user_id)
	print(seat_id)
	#update the seat database 
	sql = "UPDATE Seats SET occupied = 0, user_id = null WHERE seat_id = %s"
	cursor.execute(sql,seat_id)

	#update the user database
	sql = "UPDATE Users SET seat_id = 0 WHERE user_id = %s"
	cursor.execute(sql,user_id)

	con.commit()
	con.close()

	print("leaving unclaim seating")

#list of all the spots with an outlet
def get_outlets(floor):
	cursor = con.cursor()
	sql = "SELECT seat_id FROM topspot.Seats WHERE outlet = 1 AND floor_id = %s"
	cursor.execute(sql,floor)
	return cursor.fetchall()

def get_seat(floor, location):
	refreshDatabase()
	cursor = con.cursor()
	sql = "SELECT * FROM topspot.Seats WHERE location = %s AND floor_id = %s"
	cursor.execute(sql,(location, floor))
	return cursor.fetchall()

