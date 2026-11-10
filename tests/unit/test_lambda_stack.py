import aws_cdk as cdk
import pytest
from aws_cdk.assertions import Template, Capture
from ci_cd_testing.lambda_stack import LambdaStack


# Build the stack once and share the template between all tests in this file
# (Jest repeats "new cdk.App()" + "new LambdaStack()" in every test; a pytest
# fixture does the same job once).
@pytest.fixture(scope="module")
def template():
    app = cdk.App()
    # WHEN
    stack = LambdaStack(app, "MyTestStack", stage_name="Dev")
    # THEN
    return Template.from_stack(stack)


# Lessons 3.7 / 4.1: Test for DynamoDB resource in stack
def test_dynamodb_table_created(template):
    template.has_resource("AWS::DynamoDB::Table", {
        "Properties": {"TableName": "Devci_cd_testing_table"},
    })


# Lesson 4.2: Test for ApiGateway resource in stack
def test_api_gateway_rest_api_created(template):
    template.has_resource("AWS::ApiGateway::RestApi", {
        "Properties": {"Name": "Dev Weather Rest Api"},
    })


# Lesson 4.3: Verify the number of Lambda functions within the stack
def test_5_lambda_functions_created(template):
    template.resource_count_is("AWS::Lambda::Function", 5)


# Lesson 4.4: Verify Lambda properties and environment variables
def test_create_lambda_function_exists(template):
    template.has_resource("AWS::Lambda::Function", {
        "Properties": {"FunctionName": "Dev-cdk-python-create"},
    })

    env_capture = Capture()
    template.has_resource_properties("AWS::Lambda::Function", {
        "FunctionName": "Dev-cdk-python-create",
        "Environment": env_capture,
    })

    # The course hard-codes the table's logical ID (e.g. "DevCdkTypescriptWeatherTableA8D40B83").
    # We look it up instead so the test doesn't break if the hash changes.
    table_logical_id = next(iter(template.find_resources("AWS::DynamoDB::Table")))

    assert env_capture.as_object() == {
        "Variables": {
            "TABLE_NAME": {"Ref": table_logical_id},
            "STAGE_NAME": "Dev",
        },
    }
