import src.utils as utils
import src.db_helper as db_helper
import sys 

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from src.exception import CustomException
from src.logger import logging

app = FastAPI()

inprogress_orders = {}
@app.post("/")
async def handle_request(request: Request):
    logging.info(f"handle_request method starts")
    try:
        payload = await request.json()

        intent = payload['queryResult']['intent']['displayName']
        parameters = payload['queryResult']['parameters']
        output_contexts = payload['queryResult']['outputContexts']
        session_id = utils.extract_session_id(output_contexts[0]['name'])
        intent_handler_dict = {
            'order.add-context:ongoing-order':add_to_order,
            'order.remove-context: ongoing order': remove_from_order,
            'order.complete-context:ongoing-order': complete_order,
            'track.order-context:ongoing-tracking': track_order,
            'new.order': new_order_reset
        }

        return intent_handler_dict[intent](parameters,session_id)
    except Exception as e:
        logging.info(f"Exception occured in handling request stage")
        raise CustomException(e,sys)


def new_order_reset(parameters: dict, session_id: str):
    logging.info(f"new_order_reset method starts")
    try:
        del inprogress_orders[session_id]
    except Exception as e:
        logging.info(f"Exception occured in new_order_reset stage")
        raise CustomException(e,sys)

#Add order
def add_to_order(parameters: dict, session_id: str):
    logging.info(f"add_to_order method starts")
    try:
        food_items = parameters["food-item"]
        quantities = parameters["number"]

        if len(food_items) != len(quantities):
            fulfillment_text = f"Sorry I didn't understand. Can you please specify food items and quantity properly"
        else:
            new_food_dict = dict(zip(food_items,quantities))

            if session_id in inprogress_orders:
                current_food_dict = inprogress_orders[session_id]
                current_food_dict.update(new_food_dict)
                inprogress_orders[session_id] = current_food_dict
            else:
                inprogress_orders[session_id] = new_food_dict

            print(inprogress_orders)

            order_str = utils.get_str_from_food_dict(inprogress_orders[session_id])
            fulfillment_text = f"So far you have {order_str} items in your list"
        
        
        return JSONResponse(content=
                            {
                                "fulfillmentText" : fulfillment_text
                            })
    except Exception as e:
        logging.info(f"Exception occured in add_to_order stage")


#Order Place
def complete_order(parameters: dict, session_id: str):
    logging.info(f"complete_order method starts")
    try: 
        if session_id not in inprogress_orders:
            fulfillment_text = " I am having trouble finding your order. Apologies! Can you place the order again?"
        else:
            order = inprogress_orders[session_id] 
            order_id = save_to_db(order)

            if order_id == -1:
                fulfillment_text = f"Sorry the order could not be processed due to some error. Please try again"
            else:
                order_total = db_helper.get_total_order_price(order_id)
                fulfillment_text = f"""Awesome! We have placed your order
                here is your order id {order_id} 
                your order total is {order_total} Which can be paid at the time of delivery"""

            del inprogress_orders[session_id] 
        return JSONResponse(content={
            "fulfillment_text" : fulfillment_text
        })
    except Exception as e:
        logging.info(f"Exception occured at complete_order stage")
        raise CustomException(e,sys)

def save_to_db(order: dict):
    logging.info(f"save_to_db method starts")
    try:
        order_id = None
        for food_item, quantity in order.items():
            if order_id is None:    
                db_helper.insert_order_item(
                    food_item,
                    quantity,
                    order_id  
                )
                order_id = db_helper.get_order_id()
            else:
                db_helper.insert_order_item(
                    food_item,
                    quantity,
                    order_id  
                )
        db_helper.insert_order_tracking(order_id,"In Progress")   
        return order_id
    except Exception as e:
        logging.info(f"Error occured at save_to_db stage")
        raise CustomException(e,sys)



#Tracking order
def track_order(parameters: dict, session_id: str):
    logging.info(f"track_order method starts")
    try:
        order_id = int(parameters['order_id'])
        order_status = db_helper.get_order_status(order_id)

        if order_status:
            fulfillment_text = f"The order status for order id {order_id} is {order_status}"
        else:
            fulfillment_text = f"No order found with order id {order_id}"
        return JSONResponse(content=
                            {
                                "fulfillmentText" : fulfillment_text
                            })
    except Exception as e:
        logging.info(f"Exception occured at track_order stage")
        raise CustomException(e,sys)

#Remove Order
def remove_from_order(parameters: dict, session_id: str):
    logging.info(f"remove_from_order method starts")
    try:
        if session_id not in inprogress_orders:
            fulfillment_text = f"I am having trouble locating your order. Can you please place the order again ?"
        
        current_order = inprogress_orders[session_id]
        food_items = parameters["food-item"]
        removed_items = []
        unmatched_items = []
        for item in food_items:
            if item not in current_order:
                unmatched_items.append(item)
            else: 
                removed_items.append(item)
                del current_order[item]
        
        if len(removed_items) > 0:
            fulfillment_text = f'Removed {", ".join(removed_items)}  from your order'
        
        if len(unmatched_items) > 0:
            fulfillment_text = f'Your current order does not have {",".join(unmatched_items)}'
        
        if len(current_order.keys()) == 0:
            fulfillment_text += f"Your order is empty!"
        else:
            order_str = utils.get_str_from_food_dict(current_order)
            fulfillment_text = f"Here are the remaining items in your order: {order_str}"
        
        return JSONResponse(content={
            "fulfillmentText" : fulfillment_text
            })
    except Exception as e:
        logging.info("Exception occured at remove_from_order stage")
        raise CustomException(e,sys)






