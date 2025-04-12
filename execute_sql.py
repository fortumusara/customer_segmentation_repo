import snowflake.connector
from config.snowflake_config import get_snowflake_connection

def execute_sql_script(file_path):
    conn = get_snowflake_connection()
    cursor = conn.cursor()

    with open(file_path, 'r') as f:
        sql_commands = f.read()
    
    for command in sql_commands.strip().split(';'):
        if command.strip():
            cursor.execute(command)
    
    cursor.close()
    conn.close()
