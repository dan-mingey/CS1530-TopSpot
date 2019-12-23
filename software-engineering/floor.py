#floor page
from Seat import Seat
import pymysql

# Connect to users database
con = pymysql.connections.Connection(user='root', password='TopSpotAWS',
                              host='topspot.cbjrgugeafkg.us-east-1.rds.amazonaws.com',
                              database='topspot')

FLOOR_0_MAX_CAPACITY = 63
FLOOR_1_MAX_CAPACITY = 52
FLOOR_2_MAX_CAPACITY = 21
FLOOR_3_MAX_CAPACITY = None
FLOOR_4_MAX_CAPACITY = 42


###########
#FUNCTIONS#
###########

def refreshDatabase():
    print("refreshing the database")
    global con 
    con = pymysql.connections.Connection(user='root', password='TopSpotAWS',
                              host='topspot.cbjrgugeafkg.us-east-1.rds.amazonaws.com',
                              database='topspot')

# get how many seats are taken on a specific floor
def get_current_capacity(floor):
	refreshDatabase()
	if floor > 4 or floor < 0:
		print("ERROR: please enter a floor numbered 0-4")
		return

	cursor = con.cursor()
	sql = "SELECT count(*) from Seats WHERE floor_id = %s AND occupied = 1"
	cursor.execute(sql, (str(floor), ))
	return cursor.fetchone()[0]

# get the maximum capacity of a specific floor
def get_max_capacity(floor):
	refreshDatabase()
	if floor > 4 or floor < 0:
		print("ERROR please enter a floor numbered 0-4")
		return

	cursor = con.cursor()
	sql = "SELECT count(*) from Seats WHERE floor_id = %s"
	cursor.execute(sql, (str(floor), ))
	return cursor.fetchone()[0]

# returns a list of all the seats and their information of the specified floor
def get_seats(floor):
	refreshDatabase()
	print("this is floor:" +str(floor))
	#if((floor > 4) or (floor < 0)):
	#	print(floor)
	#	print("ERROR please enter a floor numbered 0-4")
	#	return

	cursor = con.cursor()
	sql = "SELECT * from Seats WHERE floor_id = %s"
	cursor.execute(sql, (str(floor), ))
	return cursor.fetchall()

#stopped here
def clear_floor(floor):
	# refreshDatabase()
	# print("updating floor: " + str(floor))

	# # change occupied to 0
	# cursor = con.cursor()
	# sql = "UPDATE Seats set occupied = 0 where id= %s "
	# cursor.execute(sql, (str(floor), ))

	# # change user_id to null 
	# sql = "UPDATE Seats set user_id = null where id= %s "
	# cursor.execute(sql, (str(floor), ))
	print("CLEARING THE FLOOR NOW!!!!!!!!!!!!!")

	# change the seat_id of the user in the users table to null

