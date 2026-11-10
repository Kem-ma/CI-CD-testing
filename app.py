#!/usr/bin/env python3
import os

import aws_cdk as cdk

from ci_cd_testing.ci_cd_testing_stack import CiCdTestingStack


app = cdk.App()
CiCdTestingStack(app, "CiCdTestingStack",
                 env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"),
                                     region=os.getenv("CDK_DEFAULT_REGION"))
    )

app.synth()
