import psycopg2
# Database methods for connecting, inserting, fetching, and deleting.

# This method connects us to our database
def connectToDatabase():
    return psycopg2.connect(
            host = "ec2-34-234-240-121.compute-1.amazonaws.com",
            database = "d3pvstjgsdbmjp",
            user = "rmbmdpagnloizn",
            password = "c371c84f18d0b18a39d271bce2a695c6f4a2dbe4974d036cac1a86a2f5f4d076",
            port = "5432",
        );

# This method commits values to a table in our database
def commitToDatabase(values):
    # Create connection and cursor
    conn = connectToDatabase()
    c = conn.cursor()

    # Insert command
    sql_command = "INSERT INTO Players VALUES" + str(values)
    exists = False
    
    #execute command
    try:
        c.execute(sql_command)
    except:
        print("ID already exists. Try again.")

    # Commit changes and close connection
    conn.commit()
    conn.close()

# This function returns all records in database
def getAllDbValues():
    conn = connectToDatabase()

    #create a cursor
    c = conn.cursor()

    #retreive records from database
    c.execute("SELECT * FROM Players")
    records = c.fetchall()

    return records;

#this function clears the records in the database
def clearDB():
    #connect to database
    conn = connectToDatabase();
    c = conn.cursor()

    #command to delete all records in database
    c.execute("DELETE FROM Players")

    #commit changes and close connection to database
    conn.commit();
    conn.close();

def getName(id):
    conn = connectToDatabase();
    c = conn.cursor()

    #query for name given ID
    c.execute("SELECT Name FROM Players WHERE ID = " + str(id))
    name = c.fetchall()

    conn.commit();
    conn.close();

    return name