from aws_cdk import Stack
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from constructs import Construct

class CiCdTestingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.pipeline = CodePipeline(
            self, "Pipeline",
            synth=ShellStep("synth", input=CodePipelineSource.git_hub(
                "Kem-ma/CI-CD-testing", "main"),
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt -r requirements-dev.txt",
                    "pytest",
                    "cdk synth",
                ]
            ),
        )
