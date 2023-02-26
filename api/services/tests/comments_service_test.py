from unittest import mock
from fastapi.testclient import TestClient

import requests
from main import app
from models.comments_model import CommentsModel
import services.comments_service as comments_service
import pytest


client = TestClient(app)


@mock.patch.object(requests, "get")
def test_get_comments_success(mockget):
    expected_id = 1
    expected_postId = 1
    expected_email = "test@example.com"

    mockresponse = mock.Mock()
    mockget.return_value = mockresponse
    mockget.status_code = 200
    mockresponse.text = """[
        {
            "postId": 1,
            "id": 1,
            "name": "id labore ex et quam laborum",
            "email": "test@example.com",
            "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos"
        }
    ]"""

    omit_fields = ["name", "body"]
    result = comments_service.get_comments(omit_fields=omit_fields)

    actual_id = result[0]["id"]
    actual_postId = result[0]["postId"]
    actual_email = result[0]["email"]

    assert actual_id == expected_id
    assert actual_postId == expected_postId
    assert actual_email == expected_email
    assert None == result[0].get("name")
    assert None == result[0].get("body")


@mock.patch.object(requests, "get")
def test_get_comments_failure_http_exception(mockget):
    expected_result = []

    mockget.side_effect = requests.exceptions.HTTPError("Http exception")
    omit_fields = ["name", "body"]
    result = comments_service.get_comments(omit_fields=omit_fields)

    assert expected_result == result


@mock.patch.object(requests, "get")
def test_get_comments_failure_connexion_exception(mockget):
    expected_result = []

    mockget.side_effect = requests.exceptions.ConnectionError("Connection exception")
    omit_fields = ["name", "body"]
    result = comments_service.get_comments(omit_fields=omit_fields)

    assert expected_result == result


@mock.patch.object(requests, "get")
def test_get_comments_failure_timeout_exception(mockget):
    expected_result = []
    mockget.side_effect = requests.exceptions.Timeout("Timeout exception")
    omit_fields = ["name", "body"]
    result = comments_service.get_comments(omit_fields=omit_fields)

    assert expected_result == result


@mock.patch.object(requests, "get")
def test_get_comments_failure_request_exception(mockget):
    expected_result = []

    mockget.side_effect = requests.exceptions.RequestException("Request exception")
    omit_fields = ["name", "body"]

    result = []
    with pytest.raises(SystemExit):
        result = comments_service.get_comments(omit_fields=omit_fields)

    assert expected_result == result


def test_remove_fields_succes():
    expected_id = 1
    expected_name = "Test Name"
    expected_email = "email@example.com"
    expected_postid = 1

    omit_fields = ["body"]
    comment = {
        "body": "test_body",
        "email": "email@example.com",
        "id": 1,
        "name": "Test Name",
        "postId": 1,
    }

    result = comments_service.remove_fields(item=comment, fields=omit_fields)

    actual_id = result.get("id")
    actual_name = result.get("name")
    actual_email = result.get("email")
    actual_postid = result.get("postId")

    assert expected_id == actual_id
    assert expected_name == actual_name
    assert expected_email == actual_email
    assert expected_postid == actual_postid
    assert None == result.get("body")


def test_validate_omit_fields_succes():
    omit_fields = ["name", "body"]

    raised = False
    try:
        comments_service.validate_omit_fields(omit_fields=omit_fields)
    except:
        raised = True

    assert False == raised


def test_validate_omit_fields_failure():
    omit_fields = ["name", "invalid"]

    raised = False
    try:
        comments_service.validate_omit_fields(omit_fields=omit_fields)
    except:
        raised = True

    assert True == raised
