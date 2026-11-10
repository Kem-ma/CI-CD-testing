from aws_cdk import Stack
from constructs import Construct

class LambdaStack(Stack):
  def __init__(self, scope: Construct, construct_id: str, *, stage_name: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)
    self._stage_name = stage_name