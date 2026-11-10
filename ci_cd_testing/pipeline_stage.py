from aws_cdk import Stage
from constructs import Construct
from ci_cd_testing.lambda_stack import LambdaStack

class PipelineStage(Stage):
  def __init__(self, scope: Construct, construct_id: str,
               *, stage_name: str, **kwargs) -> None:
          super().__init__(scope, construct_id, stage_name=stage_name, **kwargs)

          LambdaStack(self, "lambdaStack", stage_name=stage_name)
