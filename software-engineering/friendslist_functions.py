#friendslist functions
from Seat import Seat
import pymysql

# Connect to users database
con = pymysql.connections.Connection(user='root', password='TopSpotAWS',
                              host='topspot.cbjrgugeafkg.us-east-1.rds.amazonaws.com',
                              database='topspot')

def refreshDatabase():
    print("refreshing the database")
    global con 
    con = pymysql.connections.Connection(user='root', password='TopSpotAWS',
                              host='topspot.cbjrgugeafkg.us-east-1.rds.amazonaws.com',
                              database='topspot')


def addFriend(user_id, friend):
		refreshDatabase()
		print("adding friend")

		data = (user_id,friend)
		cursor = con.cursor()
		sql = "INSERT INTO user_friends (user_id, friend_id) VALUES (%s,%s)"
		cursor.execute(sql, data)

		con.commit()

		data = (friend,user_id)
		cursor = con.cursor()
		sql = "INSERT INTO user_friends (user_id, friend_id) VALUES (%s,%s)"
		cursor.execute(sql, data)

		con.commit()

		con.close()

def deleteFriend(user_id,friend):
		refreshDatabase()
		print("deleting friend")

		data = (user_id,friend)
		cursor = con.cursor()
		sql = "DELETE FROM user_friends WHERE user_id = %s AND friend_id = %s"
		cursor.execute(sql, data)

		con.commit()

		data = (friend,user_id)
		cursor = con.cursor()
		sql = "DELETE FROM user_friends WHERE user_id = %s AND friend_id = %s"
		cursor.execute(sql, data)

		con.commit()

def deleteUser(user_id):
		refreshDatabase()
		print("deleting user")

		data = (user_id)
		cursor = con.cursor()
		sql = "DELETE FROM Users WHERE user_id = %s"
		cursor.execute(sql, data)

		con.commit()

def addUser(user_id, password):
	refreshDatabase()
	print("adding user")
	data = (user_id, password)
	cursor = con.cursor()
	sql = "INSERT INTO Users (user_id, password) VALUES (%s, %s)"
	cursor.execute(sql, data)
	con.commit()


def getFriendsList(user_id):
		refreshDatabase()
		print("getting friends list")
		friendsList = []

		cursor = con.cursor()
		sql = "SELECT DISTINCT friend_id FROM topspot.user_friends WHERE user_id = %s"
		cursor.execute(sql,user_id)
		friendsQuerry = cursor.fetchall()
		print(friendsQuerry)
		for friendTuple in friendsQuerry:
			for friend in friendTuple:
				friendsList.append(friend)

		return friendsList

def getUsers():
		refreshDatabase()
		print("getting users")
		usersList = []

		cursor = con.cursor()
		sql = "SELECT user_id FROM topspot.Users"
		cursor.execute(sql)
		all_users = cursor.fetchall()
		print(all_users)
		for userTuple in all_users:
			for u in userTuple:
				if u != " " and u != "admin": 
					usersList.append(u)

		return usersList

def delete_all_friends(user_id):
		refreshDatabase()
		print("deleting all friends")

		cursor = con.cursor()
		sql = "DELETE FROM user_friends WHERE user_id = %s"
		cursor.execute(sql, user_id)

		con.commit()
		con.close()

def getFriend(user_id,friend):
	refreshDatabase()
	print("getting friend")
	data = (user_id,friend)
	cursor = con.cursor()
	sql = "SELECT friend_id FROM user_friends WHERE user_id = %s AND friend_id = %s"
	cursor.execute(sql, data)
	return cursor.fetchall()

def checkFriend(user_id):
	refreshDatabase()
	cursor = con.cursor()
	sql = "SELECT user_id FROM Users WHERE user_id = %s"
	cursor.execute(sql, user_id)
	return cursor.fetchone()

def checkTable(user_id, friend_id):
	refreshDatabase()
	data = (user_id,friend_id)
	cursor = con.cursor()
	sql = "SELECT count(*) FROM user_friends WHERE user_id = %s AND friend_id = %s "
	cursor.execute(sql, data)
	return cursor.fetchone()

# if not getFriend("Sam", "Dan"):
# 	print("no friend")
# else:
# 	print ("friend")

# addFriend("Inna", "Sam")
# addFriend("Jenni", "Sam")
# addFriend("Jenni", "Erik")
# addFriend("Erik", "Dan")
# addFriend("Sam", "Dan")