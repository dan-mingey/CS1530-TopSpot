from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash
from User import User
import friendslist_functions 
from floor import get_current_capacity, get_max_capacity, get_seats, clear_floor
from map import get_seat, claim_seating, unclaim_seating

app = Flask(__name__)

SECRET_KEY = 'development key'
DEBUG = True

app.config.from_object(__name__)

import pymysql, json


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


@app.route("/")
def default():
	print("rendering the homepage")
	return redirect(url_for("login"))

@app.route("/SelectFloor")
def floor_select():
    return render_template("FloorSelect.html", GroundFloorCount=get_current_capacity(0), FirstFloorCount=get_current_capacity(1), SecondFloorCount=get_current_capacity(2), FourthFloorCount=get_current_capacity(4)) 


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
      
        # check the username and password 
        usernameEntered = request.form['username']
        passwordEntered = request.form['password']
        cursor = con.cursor()
        sql = "SELECT count(*) FROM topspot.Users WHERE user_id = %s AND password = %s"

        cursor.execute(sql, (usernameEntered, passwordEntered))

        
        if(usernameEntered == "admin" and passwordEntered == "admin"):
            return render_template("AdminHome.html")

        OneIfUser = cursor.fetchone()[0]

        if OneIfUser == 1:
            print("username and password are correct")
            sql = "SELECT * FROM topspot.Users WHERE user_id = %s AND password = %s"
            cursor.execute(sql, (usernameEntered, passwordEntered))
            current_user = cursor.fetchall()[0]
            session['current_user'] = current_user[0]
            return render_template("FloorSelect.html", GroundFloorCount=get_current_capacity(0), FirstFloorCount=get_current_capacity(1), SecondFloorCount=get_current_capacity(2), FourthFloorCount=get_current_capacity(4)) 
            # return render_template("AdminHome.html")
        else:
            print("username and password are incorrect")
            return render_template("login.html")
        

        # Dan password

    return render_template("login.html")

@app.route("/unclaim_seating", methods=["GET"])
def unclaim_spot():
    refreshDatabase()
    print("inside unclaim seating")
    current_user_id = session['current_user']
    cursor = con.cursor()
    sql = "SELECT * FROM topspot.Users WHERE user_id = %s"
    cursor.execute(sql, current_user_id)   
    
  
    current_user = cursor.fetchall()[0]
    
    user_id = current_user[0]
    seat_id = current_user[2] 
    
    # unclaim the seat by passing in the current user id and the seat id of that user
    unclaim_seating(user_id, seat_id)

    refreshDatabase()

    cursor = con.cursor()
    sql = "SELECT * FROM topspot.Seats WHERE seat_id = %s"
    rows_count = cursor.execute(sql, seat_id)   
    
    if rows_count > 0:
        seat_to_change = cursor.fetchall()[0]
        return seat_to_change[5]
   
    return "NoSeatOccupied"

    

@app.route("/claim_seating", methods=["POST"])
def reserve_spot():
    if request.method == 'POST':
        seat_location = request.form['seat_location']
        current_floor = request.form['current_floor']
        print("seat: "+seat_location+" on floor "+current_floor+" is being claimed")
        

        cursor = con.cursor()
        sql = "SELECT * FROM topspot.Seats WHERE floor_id = %s AND location = %s"
        cursor.execute(sql, (current_floor, seat_location))
        
        
        seat_id = cursor.fetchall()[0]
        cursor.close()
        user_id = session['current_user']

        print(seat_id[0])
        print(user_id)
        claim_seating(user_id, seat_id[0])

        print("seat: "+seat_location+" on floor "+current_floor+" was claimed by "+user_id)
        #call the claim seating function from the map class
        
    return ""


@app.route("/get_seat_info", methods=["POST"])
def get_seat_info():
    if request.method == 'POST':
        seat_location = request.form['seat_location']
        current_floor = request.form['current_floor']
        #print("seat: "+seat_location+" on floor "+current_floor+" was claimed")
        seat = get_seat(current_floor, seat_location)[0]
        print("This is the seat info:  "+str(seat))
        return json.dumps(seat)


        
    return ""

@app.route("/get_spots", methods=["POST"])
def get_spots():
    if request.method == 'POST':
        refreshDatabase()
        current_floor = request.form['current_floor']
        print(current_floor)
        spots = get_seats(current_floor)
        print("\n\n\n\n\n")
        print(spots)
        return json.dumps(spots)


        
    return ""


@app.route("/get_user_status", methods=["GET"])
def get_user_status():
    if request.method == 'GET':
        refreshDatabase()
        current_user_id = session['current_user']

        #get the current user information from the database
        cursor = con.cursor()
        sql = "SELECT * FROM topspot.Users WHERE user_id = %s"
        cursor.execute(sql, current_user_id)
        current_user = cursor.fetchall()[0]
        cursor.close()

        print("\n\nThis is the current users seat id")
        print(current_user[2])
        return(str(current_user[2]))

        
    return ""


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        

        #get the user name and password from the user
        usernameEntered = request.form['username']
        passwordEntered = request.form['password']
        passwordEntered2 = request.form['password2']

        cursor = con.cursor()
        #check to see if someone is already in the database with that username
        sql = "SELECT count(*) FROM topspot.Users WHERE user_id = %s"
        cursor.execute(sql, (usernameEntered, ))
        OneIfUserAlreadyExists = cursor.fetchone()[0]

        #if passwords do not match
        if passwordEntered != passwordEntered2:
            print("passwords do not match")
            return render_template("register.html")

        #if someone already exists, make re-render register.html
        if OneIfUserAlreadyExists == 1:
            print("username already exists")
            return render_template("register.html")
        #if no one exists with this username yet, add them to the database
        else:
            print("new username, adding user to database")


            data = []
            newUser = User(usernameEntered, passwordEntered)  
            data.append(newUser.__dict__)

            cursor.executemany("""
            INSERT INTO Users (user_id, password, seat_id)
            VALUES (%(user_id)s, %(password)s, %(seat_id)s)""", data)
            con.commit() 

            return redirect(url_for('login'))

    return render_template("register.html")


@app.route("/GroundFloor", methods=["GET", "POST"])
def GroundFloor():
    print(get_seats(0))
    return render_template("GroundFloor.html", seats=get_seats(0), current_user=session['current_user'])

@app.route("/FirstFloor", methods=["GET", "POST"])
def FirstFloor():
    return render_template("FirstFloor.html", seats=get_seats(1), current_user=session['current_user'])
    #return render_template("FirstFloor.html")


@app.route("/SecondFloor", methods=["GET", "POST"])
def SecondFloor():
    return render_template("SecondFloor.html", seats=get_seats(2), current_user=session['current_user'])
    #return render_template("SecondFloor.html")


@app.route("/ThirdFloor", methods=["GET", "POST"])
def ThirdFloor():
    return render_template("ThirdFloor.html", seats=get_seats(0), current_user=session['current_user'])
    #return render_template("ThirdFloor.html")


@app.route("/FourthFloor", methods=["GET", "POST"])
def FourthFloor():
    return render_template("FourthFloor.html", seats=get_seats(4), current_user=session['current_user'])
    #return render_template("FourthFloor.html")

@app.route("/logout")
def logout():
    session['current_user'] = ""
    return redirect(url_for('default'))


@app.route("/friends", methods=["GET", "POST"])
def friends():
    refreshDatabase()

    print("getting user friends")
    current_user_id = session['current_user']
    friends = friendslist_functions.getFriendsList(current_user_id)
    print(friends)
    return render_template("Friends.html", friends = friends)

@app.route("/get_friends", methods=["GET"])
def get_friends():
    refreshDatabase()

    current_user_id = session['current_user']
    friends = friendslist_functions.getFriendsList(current_user_id)
    return json.dumps(friends)


@app.route("/add_friend", methods=["GET", "POST"])
def add_friend():
    if request.method == 'POST':
        refreshDatabase()

        friend = request.form['Friend']
        current_user_id = session['current_user']

        friend_check = friendslist_functions.checkFriend(friend)
        friend_exists = friendslist_functions.checkTable(current_user_id, friend)

        if friend_exists[0] == 0:
            if friend_check != None:
                friendslist_functions.addFriend(current_user_id, friend_check)
                friends = friendslist_functions.getFriendsList(current_user_id)
                print(friends)
                return render_template("Friends.html", friends = friends)
            else:
                friends = friendslist_functions.getFriendsList(current_user_id)
                return render_template("Friends.html", friends = friends, Error=True)
        else:
            friends = friendslist_functions.getFriendsList(current_user_id)
            return render_template("Friends.html", friends = friends)

    return ""

@app.route("/floor_select_help")
def show_fs_help():
    return render_template("FloorSelectHELP.html")

@app.route("/floor_plan_help")
def show_fp_help():
    return render_template("FloorPlanHelp.html")

@app.route("/friends_help")
def show_friends_help():
    return render_template("FriendsHELP.html")

@app.route("/remove_friend/<ID>")
def remove_friend(ID):
    current_user_id = session['current_user']
    friend_to_remove = ID
    friendslist_functions.deleteFriend(current_user_id, friend_to_remove)
    return redirect(url_for('friends'))

@app.route("/admin_floor")
def admin_floor():
    return render_template("AdminFloors.html", GroundFloorCount=get_current_capacity(0), FirstFloorCount=get_current_capacity(1), SecondFloorCount=get_current_capacity(2), FourthFloorCount=get_current_capacity(4))

@app.route("/admin_users", methods=["GET", "POST"])
def admin_users():
    users = friendslist_functions.getUsers()
    print(users)
    return render_template("AdminUsers.html", users = users)

@app.route("/remove_user/<ID>")
def remove_user(ID):
    user_to_remove = ID
    friendslist_functions.deleteUser(user_to_remove)
    return redirect(url_for('admin_users'))

@app.route("/clear_floor/<ID>")
def delete_floor(ID):
    floor= ID
    clear_floor(floor)
    refreshDatabase()
    return redirect(url_for('admin_floor'))

@app.route("/admin_home")
def admin_home():
    return render_template("AdminHome.html")

if __name__ == 'main':
    app.run(debug=True)
