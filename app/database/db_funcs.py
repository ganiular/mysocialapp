from database import get_connection
    
def execute(statement, args=()):
    cursor = get_connection().cursor()
    cursor.execute(statement, args)
    return cursor

def fetchall(statement, args=()):
    return execute(statement, args).fetchall()

def fetchone(statement, args=()):
    return execute(statement, args).fetchone()

