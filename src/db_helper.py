import mysql.connector
global conn 
import sys
from src.logger import logging 
from src.exception import CustomException


conn = mysql.connector.connect(
    host = "localhost",
    user="root",
    password="root",
    database="rami_foods"
)

def get_order_id():
    logging.info(f"get_order_id method starts")
    cursor = conn.cursor()
    result = None
    try: 
        query = "select max(order_id) from orders"
        cursor.execute(query)

        result = cursor.fetchone()[0]
    except Exception as e:
        logging.info(f"Exception Occured at get_order_id stage")
    finally:
        if cursor:
            cursor.close()

    return result


def insert_order_item(food_item, quantity,order_id):
    try:
        logging.info(f"insert_order_item method starts")
        cursor = conn.cursor()

        cursor.callproc('insert_order_item', (food_item, quantity, order_id))
        
        conn.commit()
        cursor.close()

    except Exception as e:
        logging(f"Exception occured at insert_order_item stage")
        conn.rollback()
        raise CustomException(e,sys)
    finally:
        if cursor:
            cursor.close()
    return -1


def get_total_order_price(order_id):
    logging.info(f"get_total_order_price method starts")
    cursor = conn.cursor()
    try:
        query = f"select get_total_order_price({order_id})"
        cursor.execute(query)

        result = cursor.fetchone()[0]
    except Exception as e:
        logging.info(f"Exception occured at get_total_order_price stage")
        raise CustomException(e,sys)
    finally:
        if cursor:
            cursor.close()

    return result


def insert_order_tracking(order_id,status):
    logging.info(f"insert_order_tracking method starts")
    cursor = conn.cursor()
    try:
        insert_query = "INSERT INTO order_tracking(order_id,status) VALUES (%s,%s);"

        cursor.execute(insert_query,(order_id,status))

        conn.commit()
    except Exception as e:
        logging.info(f"Exception occured at insert_order_tracking stage")
    finally:
        if cursor:
            cursor.close()


def get_order_status(order_id: int):
    logging.info(f"get_order_status method starts")
    cursor  = conn.cursor()
    try:
        query = ("select status from order_tracking where order_id = %s")

        cursor.execute(query,(order_id,))

        result = cursor.fetchone()

        if result is not None:
            return result[0]
        else:
            return None
    except Exception as e:
        logging.info(f"Exception occured at get_order_status stage")
    finally:
        if cursor:
            cursor.close()
