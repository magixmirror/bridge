import mysql.connector
from mysql.connector import errorcode


DB_USER = "root"
DB_PWD = ""
DB_SERVER = "localhost"
DB_PORT = 3306
DB_NAME = "Bridge_Audio"
TABLES = {}
DB_STRING = "mysql+mysqlconnector://{}@{}:{}/{}".format(DB_USER,DB_SERVER,DB_PORT,DB_NAME)

# Dimension 1 (Video)
TABLES['Video'] = (
    "CREATE TABLE `Video` ("
    "  `video_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `duration` varchar(255) NOT NULL,"
    "  `type` varchar(255) NOT NULL,"
    "  PRIMARY KEY (`video_id`)"
    ") ENGINE=InnoDB")

TABLES['Audio'] = (
    "CREATE TABLE `Audio` ("
    "  `audio_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `duration` varchar(255) NOT NULL,"
    "  `type` varchar(255) NOT NULL,"
    "  PRIMARY KEY (`audio_id`)"
    ") ENGINE=InnoDB")

# Dimension 2 (Utility)
TABLES['Utility'] = (
    "CREATE TABLE `Utility` ("
    "  `utility_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `no_silent` int(11) NOT NULL,"
    "  PRIMARY KEY (`utility_id`)"
    ") ENGINE=InnoDB")


# Dimension 3 (File_path)
TABLES['File_path'] = (
    "CREATE TABLE `File_path` ("
    "  `path_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `path` varchar(255) NOT NULL,"
    "  PRIMARY KEY (`path_id`)"
    ") ENGINE=InnoDB")

# Dimension 4 (File_name)
TABLES['File_name'] = (
    "CREATE TABLE `File_name` ("
    "  `name_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(255) NOT NULL,"
    "  PRIMARY KEY (`name_id`)"
    ") ENGINE=InnoDB")


# Facts table (Fact)
TABLES['Facts'] = (
    "CREATE TABLE `Facts` ("
    "  `file_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `video_id` int(11),"
    "  `audio_id` int(11),"
    "  `utility_id` int(11) NOT NULL,"
    "  `file_path_id` int(11) NOT NULL,"
    "  `file_name_id` int(11) NOT NULL,"
    "  `file_size` varchar(255) NOT NULL,"
    "  `file_type` varchar(255) NOT NULL,"
    "  FOREIGN KEY (`video_id`) REFERENCES Video(`video_id`),"
    "  FOREIGN KEY (`audio_id`) REFERENCES Audio(`audio_id`),"
    "  FOREIGN KEY (`utility_id`) REFERENCES Utility(`utility_id`),"
    "  FOREIGN KEY (`file_path_id`) REFERENCES File_path(`path_id`),"
    "  FOREIGN KEY (`file_name_id`) REFERENCES File_name(`name_id`),"
    "  PRIMARY KEY (`file_id`)"
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
    return cnx,cursor