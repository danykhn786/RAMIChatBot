import re
from src.logger import logging
from src.exception import CustomException
import sys

def extract_session_id(session_str: str):
    logging.info("extract_session_id method starts")
    try:
        match = re.search(r"/sessions/(.*?)/contexts/",session_str)
        if match:
            exctracted_string = match.group(1)
            return exctracted_string
    except Exception as e:
        logging.info(f"EXception occured at extract_session_id stage")
        raise CustomException(e,sys)
    return ""

def get_str_from_food_dict(food_dict: dict):
    logging.info(f"get_str_from_food_dict method starts")
    try:
        return", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
    except Exception as e:
        logging.info("Exception occured at get_str_from_food_dict stage")
        raise CustomException(e,sys)



# if __name__ == "__main__":
#      print(extract_session_id(1))
    


