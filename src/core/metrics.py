class Metrics:
    def __init__(self, cloudwatch):
        self.cloudwatch = cloudwatch

    def put_metric(self, namespace, operation, is_exception=True):
        self.cloudwatch.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    "MetricName": f"{operation}"
                    if not is_exception
                    else f"{operation}-exception",
                    "Values": [
                        1,
                    ],
                    "Unit": "None",
                },
            ],
        )
