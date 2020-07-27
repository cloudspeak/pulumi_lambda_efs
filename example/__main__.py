"""Creates a Lambda and an EFS in a VPC"""

import pulumi
from filebase64sha256 import filebase64sha256
from pulumi import ResourceOptions
from pulumi_aws import apigateway, cloudwatch, iam, lambda_
from pulumi_lambda_efs import DevelopmentEnvironment, get_environment_function_args

environment = DevelopmentEnvironment(
    "ExamplePOC",
    github_repo_name="https://github.com/cloudspeak/brew-install-efs-poc.git",
    github_version_name="codebuild",
)


# Lambda function

example_role = iam.Role(
    "ExampleFunctionRole",
    assume_role_policy="""{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
    }""",
)

iam.RolePolicyAttachment(
    "VpcAccessPolicyAttach",
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole",
    role=example_role.name,
)

iam.RolePolicyAttachment(
    "CloudwatchPolicyAttach",
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    role=example_role.name,
)

example_function = lambda_.Function(
    "exampleFunction2",
    # code="lambda.zip",
    code="lambda_no_deps.zip",
    source_code_hash=filebase64sha256("lambda_no_deps.zip"),
    handler="handler.lambda_handler",
    role=example_role.arn,
    runtime="python3.8",
    timeout=30,
    opts=ResourceOptions(depends_on=[environment]),
    **get_environment_function_args(environment),
)

logs = cloudwatch.LogGroup(
    "exampleLogGroup",
    name=example_function.name.apply(lambda name: f"/aws/lambda/{name}"),
)


# API Gateway

gateway = apigateway.RestApi("exampleApi")

resource = apigateway.Resource(
    "exampleResource",
    parent_id=gateway.root_resource_id,
    path_part="{proxy+}",
    rest_api=gateway.id,
)

resources = [resource.id, gateway.root_resource_id]
methods = []
integrations = []

for i, resource_id in enumerate(resources):

    method = apigateway.Method(
        f"exampleMethod{i}",
        http_method="ANY",
        resource_id=resource_id,
        api_key_required=False,
        request_parameters={},
        authorization="NONE",
        rest_api=gateway.id,
    )

    integration = apigateway.Integration(
        f"exampleIntegration{i}",
        rest_api=gateway.id,
        resource_id=resource_id,
        http_method=method.http_method,
        integration_http_method="POST",
        type="AWS_PROXY",
        uri=example_function.arn.apply(
            lambda arn: f"arn:aws:apigateway:eu-west-1:lambda:path/2015-03-31/functions/{arn}/invocations"
        ),
    )

    methods.append(method)
    integrations.append(integration)

deployment = apigateway.Deployment(
    "exampleDeployment",
    rest_api=gateway.id,
    opts=ResourceOptions(depends_on=[*methods, *integrations]),
)

stage = apigateway.Stage(
    "exampleStage", deployment=deployment.id, rest_api=gateway.id, stage_name="dev"
)

lambda_permission = lambda_.Permission(
    "lambdaPermission",
    action="lambda:InvokeFunction",
    function=example_function.name,
    principal="apigateway.amazonaws.com",
    source_arn=gateway.execution_arn.apply(
        lambda execution_arn: f"{execution_arn}/*/*/*"
    ),
    opts=ResourceOptions(depends_on=[example_function, deployment]),
)

pulumi.export("file_system_id", environment.file_system_id)
pulumi.export("vpc_id", environment.vpc_id)
pulumi.export("public_subnets", environment.public_subnet_ids)
pulumi.export("private_subnet", environment.private_subnet_id)
pulumi.export("security_group_id", environment.security_group_id)
pulumi.export("pulumi_access_token_parameter_name", environment.pulumi_token_param_name)
pulumi.export(
    "api_endpoint",
    gateway.id.apply(
        lambda id: f"https://{id}.execute-api.eu-west-1.amazonaws.com/dev/"
    ),
)
