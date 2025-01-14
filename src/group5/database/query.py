import mysql.connector as mysql
from database.query import create_table, create_db_connection
from database.secret import *

def create_dict_table(mydb):
    create_dict_table_query = """
    CREATE TABLE g5_dictionary (
        id INT AUTO_INCREMENT PRIMARY KEY, 
        word VARCHAR(255) NOT NULL,        
        pos VARCHAR(50),                   
        def TEXT                           
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    """
    create_table(mydb, create_dict_table_query)

def fetch_word_db(mydb, word):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM g5_dictionary WHERE word = %s", (word,))
    result = cursor.fetchall()
    cursor.close()
    return result

if __name__ == "__main__":
    mydb = create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
    print(fetch_word_db(mydb, "jesus"))
    mydb.close()