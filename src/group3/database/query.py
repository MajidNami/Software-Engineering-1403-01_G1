import mysql.connector as mysql

# تعریف تابع برای ایجاد اتصال به دیتابیس
def create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME):
    try:
        mydb = mysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = mydb.cursor()
        # ایجاد دیتابیس اگر وجود ندارد
        cursor.execute("CREATE DATABASE IF NOT EXISTS TickEightBoxDB")
        cursor.execute("USE TickEightBoxDB")

        # ایجاد جدول کاربران
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ایجاد جدول جعبه‌های تیک هشت
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS TickEightBoxes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            word VARCHAR(100) NOT NULL,
            translation VARCHAR(100) NOT NULL,
            box_number INT DEFAULT 1,
            correct_attempts INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
        )
        """)

        print("Database and tables created successfully!")
        print("Connection to MySQL DB successful")
    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")
    return mydb



def create_table(mydb, create_table_query):
    cursor = mydb.cursor()
    try:
        cursor.execute(create_table_query)
        mydb.commit()
        print("Table created successfully")
    except Exception as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()



def drop_table(mydb, table_name):
    cursor = mydb.cursor()
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        mydb.commit()
        print(f"Table {table_name} dropped successfully")
    except Exception as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()



def fetch_row_by_PRIMARY_KEY(mydb, table_name, id):
    cursor = mydb.cursor()
    try:
        query = f"SELECT * FROM {table_name} WHERE id = %s"
        cursor.execute(query, (id,))
        
        result = cursor.fetchone()
        
        if result:
            return result
        else:
            print("No row found for the given ID.")
            return None
    except Exception as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()

# افزودن کاربر جدید
def add_user(db, username, email):
    cursor = db.cursor()
    sql = "INSERT INTO Users (username, email) VALUES (%s, %s)"
    cursor.execute(sql, (username, email))
    db.commit()
    print(f"User {username} added successfully!")


# افزودن کلمه به جعبه 
def add_word_to_box(db, user_id, word, translation):
    cursor = db.cursor()
    sql = """
    INSERT INTO TickEightBoxes (user_id, word, translation)
    VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (user_id, word, translation))
    db.commit()
    print(f"Word '{word}' added to Leitner box for user {user_id}.")


# آپدیت جعبه‌ها (افزایش شماره جعبه)
def update_box(db, user_id, word):
    cursor = db.cursor()
    sql = """
    UPDATE TickEightBoxes
    SET box_number = box_number + 1, correct_attempts = correct_attempts + 1
    WHERE user_id = %s AND word = %s AND box_number < 9
    """
    cursor.execute(sql, (user_id, word))
    db.commit()
    print(f"Updated box for word '{word}' and user {user_id}.")
