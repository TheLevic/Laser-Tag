import psycopg2
# Database methdos for connecting, inserting, fethching, and deleting.
def connectToDatabase():
    return psycopg2.connect(
            host = "ec2-34-234-240-121.compute-1.amazonaws.com",
            database = "d3pvstjgsdbmjp",
            user = "rmbmdpagnloizn",
            password = "c371c84f18d0b18a39d271bce2a695c6f4a2dbe4974d036cac1a86a2f5f4d076",
            port = "5432",
        );

# Add insert fetch (delete if needed) below this line
