import bcrypt, database_common

def hash_password(password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash

@database_common.connection_handler
def check_login_password(cursor, username, password):
    query = """
    SELECT password FROM accounts
    WHERE username = %s"""
    
    cursor.execute(query, (username, ))
    db_hashed_password = cursor.fetchone()
    user_pw_in_bytes = password.encode('utf-8')
    
    return bcrypt.checkpw(user_pw_in_bytes, db_hashed_password)