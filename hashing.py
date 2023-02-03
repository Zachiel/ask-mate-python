import bcrypt, database_common

def hash_password(password):
    to_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(to_bytes, salt)
    hashed = hashed.decode('utf-8')
    return hashed

@database_common.connection_handler
def check_login_password(cursor, username, password):
    query = """
    SELECT password FROM accounts
    WHERE username = %s"""
    cursor.execute(query, (username, ))
    db_hashed_password = cursor.fetchone()
    return bcrypt.checkpw(password.encode('utf-8'),
                            db_hashed_password['password'].encode('utf-8'))
