from database import get_connection

def get_user_by_id(user_id, cursor):
    cursor.execute("SELECT * FROM user WHERE id=? LIMIT 1", (user_id,))
    return cursor.fetchone()

def get_user_by_email(email, cursor):
    cursor.execute("SELECT * FROM user WHERE email=? LIMIT 1", (email,))
    return cursor.fetchone()

def reister_user(email, first_name, surname, phone, password, cursor):
    cursor.execute("INSERT INTO user(email, first_name, surname, phone, password) VALUES(?,?,?,?,?)",
                    (email, first_name, surname, phone, password))

def set_confirmation(user_id, _type, code, time, cursor):
    cursor.execute("REPLACE INTO confirmation(user_id, type, code, created) "
                   "VALUES(?,?,?,?)", (user_id, _type, code, time))

def get_confirmation(user_id, cursor):
    return cursor.execute("SELECT * FROM confirmation WHERE user_id=? LIMIT 1",
                          (user_id,)).fetchone()

def make_user_verification(user_id, cursor):
    cursor.execute("UPDATE user SET verified=1 WHERE id=?", (user_id,))
