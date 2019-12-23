import pymysql

# Connect to users database
con = pymysql.connections.Connection(user='root', password='TopSpotAWS',
                              host='topspot.cbjrgugeafkg.us-east-1.rds.amazonaws.com',
                              database='topspot')


cursor = con.cursor()





def delete_table(): 
    sql = "TRUNCATE TABLE user_friends"
    cursor.execute(sql)

    con.commit()
    con.close()

delete_table()