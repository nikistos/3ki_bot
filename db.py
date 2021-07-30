import psycopg2
from collections.abc import Iterable

DATABASE_NAME = 'tricks_database'
DATABASE_USER = 'tricks_bot'
DATABASE_PASSWORD = 'trikstriks123'
DATABASE_HOST = 'localhost'

TABLE_USERS = 'users'
TABLE_CODES = 'codes'
TABLE_USER_CODE = 'user_code'

FUNCTION_CREATE_USER = "create_user_if_not_exists"
FUNCTION_HAS_USER_CODE = "has_user_code"
FUNCTION_IS_VALID_CODE = "is_valid_code"
FUNCTION_REGISTER_CODE = "register_code_for_user"
FUNCTION_LEADERS = "get_leader_board"


def get_leader_board():
    get_leaders_query = build_select_from_function_query(FUNCTION_LEADERS, args='')
    leaders_result = send_transaction(get_leaders_query)
    return leaders_result


def insert_user_if_not_exists(username, user_id):
    insert_user_query = build_select_from_function_query(
        function=FUNCTION_CREATE_USER,
        args=f'\'{username}\', \'{user_id}\''
    )
    insert_result = send_transaction(transaction=insert_user_query)
    return get_single_value(insert_result)


def check_code_is_valid(code):
    check_code_query = build_select_from_function_query(
        function=FUNCTION_IS_VALID_CODE,
        args=f'\'{code}\''
    )
    check_result = send_transaction(transaction=check_code_query)
    return get_single_value(check_result)


def has_user_code(user_id, code):
    has_user_code_query = build_select_from_function_query(
        function=FUNCTION_HAS_USER_CODE,
        args=f'\'{code}\',\'{user_id}\''
    )
    has_user_code_result = send_transaction(transaction=has_user_code_query)
    return get_single_value(has_user_code_result)


def register_user_code(user_id, code):
    register_code_query = build_select_from_function_query(
        function=FUNCTION_REGISTER_CODE,
        args=f'\'{user_id}\',\'{code}\''
    )
    register_code_result = send_transaction(register_code_query)
    return get_single_value(register_code_result)


def send_transaction(transaction):
    try:
        print(transaction)
        con = psycopg2.connect(
            dbname=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST
        )
        db_cursor = con.cursor()
        con.autocommit = True
        db_cursor.execute(transaction)
        result = []
        for row in db_cursor:
            result.append(row)
        db_cursor.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        con.close()


def get_single_value(cursor_result):
    print(cursor_result)
    while isinstance(cursor_result, Iterable):
        cursor_result = cursor_result[0]
    return cursor_result


def build_select_from_function_query(function, args):
    return f'SELECT * FROM {function}({args});'


def unbox_table_to_array(table):
    return table[0]
