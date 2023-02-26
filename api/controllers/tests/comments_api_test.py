import json
from unittest import mock

import pytest
from fastapi.testclient import TestClient
import requests

from main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "url",
    [
        # Only page
        ("/api/comments?page=1"),
        # Page and total
        ("/api/comments?page=1&total=10"),
        # Page, total and one omit value
        ("/api/comments?page=1&total=10&omit=id"),
        # Page, total and two omit value
        ("/api/comments?page=1&total=10&omit=id&omit=postId"),
    ],
)
def test_valid_get_comments(url):
    response = client.get(url)

    assert response.status_code == 200


@mock.patch.object(requests, "get")
def test_valid_get_comments_with_omit_values(mockget):
    expected_id = 1
    expected_page = 1
    expected_total = 2

    mockresponse = mock.Mock()
    mockget.return_value = mockresponse
    mockget.status_code = 200
    mockresponse.text = """[
        {
            "postId": 1,
            "id": 1,
            "name": "id labore ex et quam laborum",
            "email": "Eliseo@gardner.biz",
            "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos"
        },
        {
            "postId": 2,
            "id": 2,
            "name": "quo vero reiciendis velit similique earum",
            "email": "Jayne_Kuhic@sydney.com",
            "body": "est natus enim nihil est dolore omnis voluptatem numquam"
        }
    ]"""

    response = client.get("/api/comments?page=1&total=1&omit=postId")
    response_dict = json.loads(response.text)

    actual_id = response_dict["items"][0]["id"]
    actual_page = response_dict["page"]
    actual_total = response_dict["total"]

    assert actual_id == expected_id
    assert actual_page == expected_page
    assert actual_total == expected_total
    assert response.status_code == 200
    assert None == response_dict["items"][0].get("postId")


def test_invalid_get_comments_total_value_should_return_400():
    response = client.get("/api/comments?total=0")

    assert response.status_code == 422


def test_invalid_get_comments_omit_values_should_return_400():
    response = client.get("/api/comments?omit=invalid_value")

    assert response.status_code == 400
    assert (
        response.text
        == '{"detail":"Omit field has illegal values, only the following values are allowed [body, email, id, name, postId]"}'
    )
