import aws_cdk as cdk
from aws_cdk.assertions import Template
from ci_cd_testing.lambda_stack import LambdaStack


# Lesson 3.7: Test for DynamoDB resource in stack
def test_dynamodb_table_created():
    app = cdk.App()
    # WHEN
    stack = LambdaStack(app, "MyTestStack", stage_name="Dev")
    # THEN
    template = Template.from_stack(stack)
    template.has_resource("AWS::DynamoDB::Table", {
        "Properties": {"TableName": "Devci_cd_testing_table"},
    })
