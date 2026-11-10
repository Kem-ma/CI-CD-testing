import json
import pathlib
import sys

# Lesson 4.5: Lambda function test cases
# Make the src/ folder importable (TS: import { lambdaHandler } from "../src/createWeather")
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

from create_weather import lambda_handler as create_weather  # noqa: E402
from get_weather import lambda_handler as get_weather  # noqa: E402
from list_weathers import lambda_handler as list_weathers  # noqa: E402
from update_weather import lambda_handler as update_weather  # noqa: E402
from delete_weather import lambda_handler as delete_weather  # noqa: E402


def assert_lambda_response(result):
    # Jest: expect(result).toMatchObject({ body: expect.any(String), statusCode: expect.any(Number) })
    assert isinstance(result, dict)
    assert isinstance(result["statusCode"], int)
    assert isinstance(result["body"], str)


def test_create_weather():
    result = create_weather({"body": json.dumps({"weather": "hot", "town": "Douala"})})
    assert_lambda_response(result)


def test_get_weather():
    result = get_weather({"pathParameters": {"id": "123"}})
    assert_lambda_response(result)


def test_list_weathers():
    result = list_weathers({})
    assert_lambda_response(result)


def test_update_weather():
    result = update_weather({
        "pathParameters": {"id": "123"},
        "body": json.dumps({"weather": "cold", "town": "Buea"}),
    })
    assert_lambda_response(result)


def test_delete_weather():
    result = delete_weather({"pathParameters": {"id": "123"}})
    assert_lambda_response(result)
