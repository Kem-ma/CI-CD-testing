# Lesson 3.1: Importing dependencies
from aws_cdk import (
  Stack,
  aws_dynamodb as dynamodb,
  aws_lambda as _lambda,
  aws_apigateway as apigw,
  RemovalPolicy,
  )
from constructs import Construct

class LambdaStack(Stack):
  # Lesson 3.2: Stack props. TS "interface LambdaStackProps { stageName }"
  # becomes the stage_name keyword argument in Python
  def __init__(self, scope: Construct, construct_id: str, *, stage_name: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)
    self._stage_name = stage_name

    # Lesson 3.3: DynamoDB table
    table = dynamodb.Table(self, f"{stage_name}CiCdTestingTable",
                           table_name=f"{stage_name}ci_cd_testing_table",
                           partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
                           removal_policy=RemovalPolicy.DESTROY,
                           )

    # Lesson 3.4: API Gateway
    weather_api = apigw.RestApi(
      self, "weather_rest_api",
      rest_api_name=f"{stage_name} Weather Rest Api",
      description="This service saves weather data.",
    )

    # Lesson 3.5: Lambda functions
    def make_fn(construct_id: str, name: str, module: str) -> _lambda.Function:
      return _lambda.Function(
        self, construct_id,
        function_name=f"{stage_name}-cdk-python-{name}",
        runtime=_lambda.Runtime.PYTHON_3_12,   # course: NODEJS_14_X
        handler=f"{module}.lambda_handler",    # course: createWeather.lambdaHandler
        code=_lambda.Code.from_asset("src"),
        environment={"TABLE_NAME": table.table_name, "STAGE_NAME": stage_name},
      )

    create_fn = make_fn("CreateWeatherLambdaFunction", "create", "create_weather")
    get_fn    = make_fn("GetWeatherLambdaFunction",    "get",    "get_weather")
    list_fn   = make_fn("ListWeathersLambdaFunction",  "list",   "list_weathers")
    update_fn = make_fn("UpdateWeatherLambdaFunction", "update", "update_weather")
    delete_fn = make_fn("DeleteWeatherLambdaFunction", "delete", "delete_weather")

    # Give the lambda functions permissions on the table
    table.grant_write_data(create_fn)
    table.grant_read_data(get_fn)
    table.grant_read_data(list_fn)
    table.grant_read_write_data(update_fn)
    table.grant_read_write_data(delete_fn)

    # Lesson 3.6: API endpoints
    weather_api.root.add_resource("create-weather").add_method(
      "POST", apigw.LambdaIntegration(create_fn))
    weather_api.root.add_resource("weathers").add_method(
      "GET", apigw.LambdaIntegration(list_fn))
    item = weather_api.root.add_resource("weather").add_resource("{id}")
    item.add_method("GET",    apigw.LambdaIntegration(get_fn))
    item.add_method("PUT",    apigw.LambdaIntegration(update_fn))
    item.add_method("DELETE", apigw.LambdaIntegration(delete_fn))
