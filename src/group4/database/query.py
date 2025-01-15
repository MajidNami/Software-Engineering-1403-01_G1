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
        print("Connection to MySQL DB successful")
    except mysql.Error as e:
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



import mysql.connector as mysql

def g4saveResult(mydb, userid, readingid, date, score):
    my_cursor = mydb.cursor()
    
    q = "INSERT INTO g4results(readinId, userid, date, score) VALUES(%s, %s, %s, %s)"
    
    try:
        my_cursor.execute(q, (readingid, userid, date, score))
        mydb.commit()
    except Exception as e:
        print("NU UH ", e)
    finally:
        my_cursor.close()

def g4joinReadinResult(mydb):
    my_cursor = mydb.cursor()
    
    q = "SELECT * FROM g4readings INNER JOIN g4results ON g4readings.id=g4results.readinId;"
    try:
        my_cursor.execute(q)
        res = my_cursor.fetchall()
        return res
    except Exception as e:
        print("NU UH ", e)
    finally:
        my_cursor.close()

def g4savetip(mydb, title, description, username, file1=None):
    my_cursor = mydb.cursor()
    
    q = "INSERT INTO g4educationalContent(username, title, file, description) VALUES(%s, %s, %s, %s)"
    
    try:
        my_cursor.execute(q, (username, title, file1, description))
        mydb.commit()
    except Exception as e:
        print("NU UH ", e)
    finally:
        my_cursor.close()

def g4updateUser(mydb, id, newAttribute, newValue):
    my_cursor = mydb.cursor()
    
    q = "UPDATE g4users SET " + str(newAttribute) + " = " + str(newValue) + " WHERE (id = " + str(id) + ");"
    print(q)
    try:
        my_cursor.execute(q)
        mydb.commit()
        print("DONE!")
    except Exception as e:
        print("NU UH ", e)
    finally:
        my_cursor.close()

def g4saveReading(mydb, context, q1body, q1cans, q1wans1, q1wans2, q1wans3, q2body, q2cans, q2wans1, q2wans2, q2wans3, q3body, q3cans, q3wans1, q3wans2, q3wans3, title, lvl):
    my_cursor = mydb.cursor()
    
    q= "INSERT INTO g4readings (context, q1body, q1cans, q1wans1, q1wans2, q1wans3, q2body, q2cans, q2wans1, q2wans2, q2wans3, q3body, q3cans, q3wans1, q3wans2, q3wans3, title, lvl) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    try:
        my_cursor.execute(q, (context, q1body, q1cans, q1wans1, q1wans2, q1wans3, q2body, q2cans, q2wans1, q2wans2, q2wans3, q3body, q3cans, q3wans1, q3wans2, q3wans3, title, lvl))
        mydb.commit()
    except Exception as e:
        print("NU UH", e)
    finally:
        my_cursor.close()
        

def g4fetchall(mydb, tableName):
    my_cursor = mydb.cursor()

    
    myQuery = f"""
    SELECT * FROM  {tableName}
    """
    try:
        my_cursor.execute(myQuery)
        res = my_cursor.fetchall()    
        print("fetched.")
        return res
    except mysql.Error as err:
        print("Failed to fetchall :", err)
    finally:
        my_cursor.close()

        

def g4saveUser(mydb, name, email, dateOfBirth, username, password, usertype, lvl):
    my_cursor = mydb.cursor()

    # دستور SQL برای اضافه کردن کاربر
    add_user_query = """
    INSERT INTO g4users (name, email, dateOfBirth, username, password, type, lvl)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    
    add_teacher_query =  """
    INSERT INTO g4users (name, email, dateOfBirth, username, password, type)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    # print("inp")
    # print(name, email, dateOfBirth, username, password, usertype, lvl)
    
    try:
        #usertype 1 for USER!!!!!!
        if usertype:
            if lvl == "beginner":
                lvl = 1
            elif lvl == "intermediate":
                lvl = 2
            elif lvl == "advanced":
                lvl = 3
            my_cursor.execute(add_user_query, (name, email, dateOfBirth, username, password, usertype, lvl))
        else:
            print("HERE?!")
            lvl = 0
            my_cursor.execute(add_teacher_query, (name, email, dateOfBirth, username, password, usertype))
            
        mydb.commit() # تایید تغییرات
        print("User saved successfully.")
    except mysql.Error as err:
        print("Failed to insert user:", err)
    finally:
        my_cursor.close()


def save_user(mydb, name, username, password, email, age):
    my_cursor = mydb.cursor()

    # دستور SQL برای اضافه کردن کاربر
    add_user_query = """
    INSERT INTO users (name, username, password, email, age)
    VALUES (%s, %s, %s, %s, %s);
    """
    
    try:
        # اجرای دستور و اضافه کردن کاربر
        my_cursor.execute(add_user_query, (name, username, password, email, age))
        mydb.commit() # تایید تغییرات
        print("User saved successfully.")
    except mysql.Error as err:
        print("Failed to insert user:", err)
    finally:
        my_cursor.close()



def save_post(mydb, description, email, state, category, image_address, image_name, image_tags, user_id):
    my_cursor = mydb.cursor()

    # دستور SQL برای اضافه کردن پست
    add_post_query = """
    INSERT INTO posts (description, email, state, category, image_address, image_name, image_tags, user_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    try:
        # اجرای دستور و اضافه کردن پست
        my_cursor.execute(add_post_query, (description, email, state, category, image_address, image_name, image_tags, user_id))
        mydb.commit() # تایید تغییرات
        print("Post saved successfully.")
        return my_cursor.lastrowid
    except mysql.Error as err:
        print("Failed to insert post:", err)
    finally:
        my_cursor.close()




def get_user_id_by_username(db_connection, username):
    cursor = db_connection.cursor()
    query = "SELECT id FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()  # Fetchone برای دریافت نتیجه اول کوئری استفاده می‌شود
    cursor.close()

    if result:
        return result[0]  # بازگرداندن id کاربر
    else:
        return None  # اگر کاربری با این username وجود نداشته باشد
    


def get_posts_by_user_id(db_connection, user_id):
    cursor = db_connection.cursor(dictionary=True)  # استفاده از dictionary=True برای بازگرداندن نتایج به صورت دیکشنری
    query = "SELECT * FROM posts WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    posts = cursor.fetchall()  # Fetchall برای دریافت تمام نتایج مطابق با کوئری استفاده می‌شود
    cursor.close()

    return posts


def get_posts_for_user(db_connection, username):
    cursor = db_connection.cursor(dictionary=True)

    # پیدا کردن id کاربر با استفاده از username
    find_user_query = "SELECT id FROM users WHERE username = %s"
    cursor.execute(find_user_query, (username,))
    user_result = cursor.fetchone()

    posts_list = []  # ایجاد یک لیست خالی برای نگهداری دیکشنری‌های پست

    if user_result:
        user_id = user_result['id']

        # دریافت تمام پست‌های مربوط به این کاربر
        get_posts_query = "SELECT * FROM posts WHERE user_id = %s"
        cursor.execute(get_posts_query, (user_id,))
        posts_list = cursor.fetchall()  # این حالا یک لیست از دیکشنری‌ها است

    cursor.close()
    return posts_list


def search_posts_tag_for_user(db_connection, username, query):
    cursor = db_connection.cursor(dictionary=True)

    # پیدا کردن id کاربر با استفاده از username
    find_user_query = "SELECT id FROM users WHERE username = %s"
    cursor.execute(find_user_query, (username,))
    user_result = cursor.fetchone()

    posts_list = []  # ایجاد یک لیست خالی برای نگهداری دیکشنری‌های پست

    if user_result:
        user_id = user_result['id']

        # اصلاح کوئری برای دریافت پست‌هایی که در ستون category حاوی کلمه query هستند
        # و مربوط به کاربر مشخص شده با user_id هستند
        get_posts_query = """
        SELECT * FROM posts
        WHERE user_id = %s AND category LIKE %s
        """
        like_pattern = "%" + query + "%"
        cursor.execute(get_posts_query, (user_id, like_pattern))
        posts_list = cursor.fetchall()  # این حالا یک لیست از دیکشنری‌ها است

    cursor.close()
    return posts_list



def search_posts_tag_for_all(db_connection, query):
    cursor = db_connection.cursor(dictionary=True)

    posts_list = []  # ایجاد یک لیست خالی برای نگهداری دیکشنری‌های پست

    # اصلاح کوئری برای دریافت پست‌هایی که در ستون category حاوی کلمه query هستند
    get_posts_query = "SELECT * FROM posts WHERE category LIKE %s"
    like_pattern = "%" + query + "%"
    cursor.execute(get_posts_query, (like_pattern,))
    posts_list = cursor.fetchall()  # این حالا یک لیست از دیکشنری‌ها است

    cursor.close()
    return posts_list
