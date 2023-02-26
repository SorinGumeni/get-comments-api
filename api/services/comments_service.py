import json
from typing import List
from fastapi import HTTPException
import requests
import logging

from models.comments_model import CommentsModel
from config import get_environment_config

def get_comments(omit_fields: List[str]) -> List[CommentsModel]:
    """Function that returns a list of Comment objects.
    Args:
        omit_fields (List[str]): List of fields to be removed from the comment objects

    Returns:
        List[CommentsModel]: List of Comment objects
    """
    logging.info("Get comments start")
    #Validate the fileds to be omitted
    validate_omit_fields(omit_fields)

    #Get the data from the external api
    response = get_comments_from_endpoint(
        url=get_environment_config().url
    )
    comments = []
    if response:
        #Load the json string
        comments = json.loads(response.text)

    #If we have the omit fields and the endpoint has returned data
    #Then we filter out the fields that we don't need
    if omit_fields and comments:
        comments_list = []
        for item in comments:
            parsed_item = CommentsModel.parse_obj(remove_fields(item, omit_fields))
            comments_list.append(parsed_item.dict(exclude_none=True))
        return comments_list
    logging.info("Get comments end")
    return comments


def get_comments_from_endpoint(url: str) -> requests.Response:
    logging.info("Get comments from endpoint start")
    response = []
    try:
        #Send the get request
        response = requests.get(url, timeout=30)
        #Raise the excetion if there is any
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Fatal error:", err)
        raise SystemExit(err)
    logging.info("Get comments from endpoint end")
    
    return response


def remove_fields(item, fields: List[str]) -> CommentsModel:
    """Helper function to remove the kyes from a Comment object.
    Args:
        item : Comment object used to remove the keys from
        keys (List[str]): List of keys to be removed from the Comment item

    Returns:
        CommentsModel: New Comment object without the keys that are removed
    """
    return {x: item[x] for x in item if x not in fields}


def validate_omit_fields(omit_fields: List[str]):
    """ Helper function to validate omit fields

    Args:
        omit_fields (List[str]): Omit fields used for validation

    Raises:
        HTTPException: Raises exception if any invalid value is detected
    """    
    logging.debug("Validate omit fields start")

    if omit_fields:
        allowed_fields = ["body", "email", "id", "name", "postId"]
        illegal = [x for x in omit_fields if x not in allowed_fields]
        if illegal:
            raise HTTPException(
                status_code=400,
                detail="Omit field has illegal values, only the following values are allowed [body, email, id, name, postId]",
            )
    logging.info("Validate omit fields end")

