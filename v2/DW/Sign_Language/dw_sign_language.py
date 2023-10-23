import mysql.connector
from mysql.connector import errorcode


DB_USER = "root"
DB_PWD = ""
DB_SERVER = "localhost"
DB_PORT = 3306
DB_NAME = "Bridge_Video_V2"
TABLES = {}
DB_STRING = "mysql+mysqlconnector://{}@{}:{}/{}".format(DB_USER,DB_SERVER,DB_PORT,DB_NAME)

# Dimension 1 (Video)
TABLES['Video'] = (
    "CREATE TABLE `Video` ("
    "  `video_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `duration` varchar(255) NOT NULL,"
    "  `number_frames` int(11) NOT NULL,"
    "  PRIMARY KEY (`video_id`)"
    ") ENGINE=InnoDB")

# Dimension 2 (Frame)
TABLES['Frame'] = (
    "CREATE TABLE `Frame` ("
    "  `frame_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `has_landmarks` boolean NOT NULL,"
    "  `path` varchar(255) NOT NULL,"
    "  `number` int(11) NOT NULL,"
    "  `landmarks` text NOT NULL,"
    "  `has_decision` boolean NOT NULL,"
    "  PRIMARY KEY (`frame_id`)"
    ") ENGINE=InnoDB")

# Dimension 3 (Decision)
TABLES['Decision'] = (
    "CREATE TABLE `Decision` ("
    "  `decision_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `hand_gesture` varchar(255) NOT NULL,"
    "  `palm_orientation` varchar(255) NOT NULL,"
    "  PRIMARY KEY (`decision_id`)"
    ") ENGINE=InnoDB")

# Facts table (Fact)
TABLES['Fact'] = (
    "CREATE TABLE `Fact` ("
    "  `fact_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `video_id` int(11) NOT NULL,"
    "  `frame_id` int(11) NOT NULL,"
    "  `decision_id` int(11) NOT NULL,"
    "  FOREIGN KEY (`video_id`) REFERENCES Video(`video_id`),"
    "  FOREIGN KEY (`frame_id`) REFERENCES Frame(`frame_id`),"
    "  FOREIGN KEY (`decision_id`) REFERENCES Decision(`decision_id`),"
    "  UNIQUE (`frame_id`),"
    "  PRIMARY KEY (`fact_id`)"
    ") ENGINE=InnoDB")


def create_database(cnx,cursor,db_name):
    try:
        cursor.execute("USE {}".format(db_name))
        print("Connected to database {}".format(db_name))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(db_name))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            try:
                cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
            except mysql.connector.Error as err:
                print("Failed creating database: {}".format(err))
                exit(1)
            print("Database {} created successfully.".format(db_name))
            cnx.database = db_name
        else:
            print(err)
            exit(1)

# Create tables
def create_tables(cnx, cursor, Tables):
    for table_name in Tables:
        table_description = Tables[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")



# Connect to mysql and init databse and tables
def init_dw():
    cnx = mysql.connector.connect(user = DB_USER, password = DB_PWD, host = DB_SERVER)
    cursor = cnx.cursor()
    create_database(cnx,cursor,DB_NAME)
    create_tables(cnx, cursor, TABLES)
    cnx.close()