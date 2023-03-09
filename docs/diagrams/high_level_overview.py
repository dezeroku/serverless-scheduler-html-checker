from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.engagement import SES
from diagrams.aws.integration import SNS, SQS
from diagrams.aws.storage import S3
from diagrams.generic.compute import Rack

with Diagram("High Level Overview", show=False, outformat=["png"]):
    with Cluster("Serverless Scheduler"):
        distribution_sns = SNS("Distribution")

    with Cluster("Plugin Scope"):
        bucket = S3("Temp State")
        handler_sqs = SQS("(optional) Buffer")
        handler_lambda = Lambda("HTMLMonitorJobHandler")
        output = SES("Output")

    external_website = Rack("example.com")

    distribution_sns >> Edge(label="HTMLMonitorJob") >> handler_sqs >> handler_lambda
    # distribution_sns >> handler_lambda
    handler_lambda >> Edge(label="uses") >> bucket
    handler_lambda >> Edge(label="on change") >> output
    handler_lambda >> Edge(label="checks") >> external_website
