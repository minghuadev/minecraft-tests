#!/usr/bin/env python
# 2024-5-15
#
# github.com
#   awsdocs aws-doc-sdk-examples
#   /blob/main/python/example_code/cloudwatch/cloudwatch_basics.py
#
# fail at: metric.put_alarm(),  need  cloudwatch:PutMetricAlarm
#   fix: add the CloudWatchServerAgent
# fail at: alarm.alarm_arn,  need  DescribeAlarms
# fail at: metric.get_statistics(),  need  GetMetricStatistics
# fail at: for alarm in alarms,  need  DescribeAlarmsForMetric
# fail at: metric.alarms.delete(),  need  DeleteAlarms


# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose

Shows how to use the AWS SDK for Python (Boto3) with Amazon CloudWatch to create
and manage custom metrics and alarms.
"""

# snippet-start:[python.example_code.cloudwatch.imports]
from datetime import datetime, timedelta
import logging
from pprint import pprint
import random
import time
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

# snippet-end:[python.example_code.cloudwatch.imports]


g_config_use_dimension = True


# snippet-start:[python.example_code.cloudwatch.CloudWatchWrapper]
class CloudWatchWrapper:
    """Encapsulates Amazon CloudWatch functions."""

    def __init__(self, cloudwatch_resource):
        """
        :param cloudwatch_resource: A Boto3 CloudWatch resource.
        """
        self.cloudwatch_resource = cloudwatch_resource

    # snippet-end:[python.example_code.cloudwatch.CloudWatchWrapper]

    # snippet-start:[python.example_code.cloudwatch.ListMetrics]
    def list_metrics(self, namespace, name, recent=False):
        """
        Gets the metrics within a namespace that have the specified name.
        If the metric has no dimensions, a single metric is returned.
        Otherwise, metrics for all dimensions are returned.

        :param namespace: The namespace of the metric.
        :param name: The name of the metric.
        :param recent: When True, only metrics that have been active in the last
                       three hours are returned.
        :return: An iterator that yields the retrieved metrics.
        """
        try:
            kwargs = {"Namespace": namespace, "MetricName": name}
            if recent:
                kwargs["RecentlyActive"] = "PT3H"  # List past 3 hours only
            metric_iter = self.cloudwatch_resource.metrics.filter(**kwargs)
            logger.info("Got metrics for %s.%s.", namespace, name)
        except ClientError:
            logger.exception("Couldn't get metrics for %s.%s.", namespace, name)
            raise
        else:
            return metric_iter

    # snippet-end:[python.example_code.cloudwatch.ListMetrics]

    # snippet-start:[python.example_code.cloudwatch.PutMetricData]
    def put_metric_data(self, namespace, name, value, unit):
        """
        Sends a single data value to CloudWatch for a metric. This metric is given
        a timestamp of the current UTC time.

        :param namespace: The namespace of the metric.
        :param name: The name of the metric.
        :param value: The value of the metric.
        :param unit: The unit of the metric.
        """
        try:
            metric = self.cloudwatch_resource.Metric(namespace, name)
            if g_config_use_dimension: # new using dimension
                metric.put_data(
                    Namespace=namespace,
                    MetricData=[{"MetricName": name,
                                 "Dimensions": [
                                     {
                                         "Name": "dim1",
                                         "Value": "inst1"
                                     },
                                 ],
                                 "Value": value, "Unit": unit}],
                )
                logger.info("Put data for metric %s.%s dimension.", namespace, name)
            else:
                metric.put_data(
                    Namespace=namespace,
                    MetricData=[{"MetricName": name, "Value": value, "Unit": unit}],
                )
                logger.info("Put data for metric %s.%s", namespace, name)
        except ClientError:
            logger.exception("Couldn't put data for metric %s.%s", namespace, name)
            raise

    # snippet-end:[python.example_code.cloudwatch.PutMetricData]

    # snippet-start:[python.example_code.cloudwatch.PutMetricData_DataSet]
    def put_metric_data_set(self, namespace, name, timestamp, unit, data_set):
        """
        Sends a set of data to CloudWatch for a metric. All of the data in the set
        have the same timestamp and unit.

        :param namespace: The namespace of the metric.
        :param name: The name of the metric.
        :param timestamp: The UTC timestamp for the metric.
        :param unit: The unit of the metric.
        :param data_set: The set of data to send. This set is a dictionary that
                         contains a list of values and a list of corresponding counts.
                         The value and count lists must be the same length.
        """
        try:
            metric = self.cloudwatch_resource.Metric(namespace, name)
            if g_config_use_dimension: # new using dimension
                metric.put_data(
                    Namespace=namespace,
                    MetricData=[
                        {
                            "MetricName": name,
                            "Timestamp": timestamp,
                            "Dimensions": [
                                {
                                    "Name": "dim1",
                                    "Value": "inst1"
                                },
                            ],
                            "Values": data_set["values"],
                            "Counts": data_set["counts"],
                            "Unit": unit,
                        }
                    ],
                )
                logger.info("Put data set for metric %s.%s dimension.", namespace, name)
            else:
                metric.put_data(
                    Namespace=namespace,
                    MetricData=[
                        {
                            "MetricName": name,
                            "Timestamp": timestamp,
                            "Values": data_set["values"],
                            "Counts": data_set["counts"],
                            "Unit": unit,
                        }
                    ],
                )
                logger.info("Put data set for metric %s.%s.", namespace, name)
        except ClientError:
            logger.exception("Couldn't put data set for metric %s.%s.", namespace, name)
            raise

    # snippet-end:[python.example_code.cloudwatch.PutMetricData_DataSet]

    # snippet-start:[python.example_code.cloudwatch.GetMetricStatistics]
    def get_metric_statistics(self, namespace, name, start, end, period, stat_types):
        """
        Gets statistics for a metric within a specified time span. Metrics are grouped
        into the specified period.

        :param namespace: The namespace of the metric.
        :param name: The name of the metric.
        :param start: The UTC start time of the time span to retrieve.
        :param end: The UTC end time of the time span to retrieve.
        :param period: The period, in seconds, in which to group metrics. The period
                       must match the granularity of the metric, which depends on
                       the metric's age. For example, metrics that are older than
                       three hours have a one-minute granularity, so the period must
                       be at least 60 and must be a multiple of 60.
        :param stat_types: The type of statistics to retrieve, such as average value
                           or maximum value.
        :return: The retrieved statistics for the metric.
        """
        try:
            metric = self.cloudwatch_resource.Metric(namespace, name)
            if g_config_use_dimension: # new using dimension
                stats = metric.get_statistics(
                    StartTime=start, EndTime=end, Period=period,
                    Dimensions=[
                        {
                            "Name": "dim1",
                            "Value": "inst1"
                        },
                    ],
                    Statistics=stat_types
                )
                logger.info(
                    "Got %s statistics for %s dimension.", len(stats["Datapoints"]), stats["Label"]
                )
            else:
                stats = metric.get_statistics(
                    StartTime=start, EndTime=end, Period=period, Statistics=stat_types
                )
                logger.info(
                    "Got %s statistics for %s.", len(stats["Datapoints"]), stats["Label"]
                )
        except ClientError:
            logger.exception("Couldn't get statistics for %s.%s.", namespace, name)
            raise
        else:
            return stats

    # snippet-end:[python.example_code.cloudwatch.GetMetricStatistics]

    # snippet-start:[python.example_code.cloudwatch.PutMetricAlarm]
    def create_metric_alarm(
        self,
        metric_namespace,
        metric_name,
        alarm_name,
        stat_type,
        period,
        eval_periods,
        threshold,
        comparison_op,
    ):
        """
        Creates an alarm that watches a metric.

        :param metric_namespace: The namespace of the metric.
        :param metric_name: The name of the metric.
        :param alarm_name: The name of the alarm.
        :param stat_type: The type of statistic the alarm watches.
        :param period: The period in which metric data are grouped to calculate
                       statistics.
        :param eval_periods: The number of periods that the metric must be over the
                             alarm threshold before the alarm is set into an alarmed
                             state.
        :param threshold: The threshold value to compare against the metric statistic.
        :param comparison_op: The comparison operation used to compare the threshold
                              against the metric.
        :return: The newly created alarm.
        """
        try:
            metric = self.cloudwatch_resource.Metric(metric_namespace, metric_name)
            if g_config_use_dimension: # new using dimension
                alarm = metric.put_alarm(
                    AlarmName=alarm_name,
                    Statistic=stat_type,
                    Period=period,
                    Dimensions=[
                        {
                            "Name": "dim1",
                            "Value": "inst1"
                        },
                    ],
                    EvaluationPeriods=eval_periods,
                    Threshold=threshold,
                    ComparisonOperator=comparison_op,
                )
                logger.info(
                    "Added alarm %s to track metric %s.%s dimension.",
                    alarm_name,
                    metric_namespace,
                    metric_name,
                )
            else:
                alarm = metric.put_alarm(
                    AlarmName=alarm_name,
                    Statistic=stat_type,
                    Period=period,
                    EvaluationPeriods=eval_periods,
                    Threshold=threshold,
                    ComparisonOperator=comparison_op,
                )
                logger.info(
                    "Added alarm %s to track metric %s.%s.",
                    alarm_name,
                    metric_namespace,
                    metric_name,
                )
        except ClientError:
            logger.exception(
                "Couldn't add alarm %s to metric %s.%s",
                alarm_name,
                metric_namespace,
                metric_name,
            )
            raise
        else:
            return alarm

    # snippet-end:[python.example_code.cloudwatch.PutMetricAlarm]

    # snippet-start:[python.example_code.cloudwatch.DescribeAlarmsForMetric]
    def get_metric_alarms(self, metric_namespace, metric_name):
        """
        Gets the alarms that are currently watching the specified metric.

        :param metric_namespace: The namespace of the metric.
        :param metric_name: The name of the metric.
        :returns: An iterator that yields the alarms.
        """
        metric = self.cloudwatch_resource.Metric(metric_namespace, metric_name)
        alarm_iter = metric.alarms.all()
        logger.info("Got alarms for metric %s.%s.", metric_namespace, metric_name)
        return alarm_iter

    # snippet-end:[python.example_code.cloudwatch.DescribeAlarmsForMetric]

    # snippet-start:[python.example_code.cloudwatch.EnableAlarmActions.DisableAlarmActions]
    def enable_alarm_actions(self, alarm_name, enable):
        """
        Enables or disables actions on the specified alarm. Alarm actions can be
        used to send notifications or automate responses when an alarm enters a
        particular state.

        :param alarm_name: The name of the alarm.
        :param enable: When True, actions are enabled for the alarm. Otherwise, they
                       disabled.
        """
        try:
            alarm = self.cloudwatch_resource.Alarm(alarm_name)
            if enable:
                alarm.enable_actions()
            else:
                alarm.disable_actions()
            logger.info(
                "%s actions for alarm %s.",
                "Enabled" if enable else "Disabled",
                alarm_name,
            )
        except ClientError:
            logger.exception(
                "Couldn't %s actions alarm %s.",
                "enable" if enable else "disable",
                alarm_name,
            )
            raise

    # snippet-end:[python.example_code.cloudwatch.EnableAlarmActions.DisableAlarmActions]

    # snippet-start:[python.example_code.cloudwatch.DeleteAlarms]
    def delete_metric_alarms(self, metric_namespace, metric_name):
        """
        Deletes all of the alarms that are currently watching the specified metric.

        :param metric_namespace: The namespace of the metric.
        :param metric_name: The name of the metric.
        """
        try:
            metric = self.cloudwatch_resource.Metric(metric_namespace, metric_name)
            metric.alarms.delete()
            logger.info(
                "Deleted alarms for metric %s.%s.", metric_namespace, metric_name
            )
        except ClientError:
            logger.exception(
                "Couldn't delete alarms for metric %s.%s.",
                metric_namespace,
                metric_name,
            )
            raise


# snippet-end:[python.example_code.cloudwatch.DeleteAlarms]


# snippet-start:[python.example_code.cloudwatch.Usage_MetricsAlarms]
def usage_demo(user_access_key_id, user_secret_access_key, user_region):
    print("-" * 88)
    print("Welcome to the Amazon CloudWatch metrics and alarms demo!")
    print("-" * 88)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    cw_session = boto3.Session(
                    aws_access_key_id=user_access_key_id,
                    aws_secret_access_key=user_secret_access_key,
                )
    cw_resource = cw_session.resource("cloudwatch", region_name=user_region)
    #cw_wrapper = CloudWatchWrapper(boto3.resource("cloudwatch"))
    cw_wrapper = CloudWatchWrapper(cw_resource)

    minutes = 20
    metric_namespace = "doc-example-metric"
    metric_name = "page_views"
    start = datetime.utcnow() - timedelta(minutes=minutes)
    print(
        f"Putting data into metric {metric_namespace}.{metric_name} spanning the "
        f"last {minutes} minutes."
    )
    for offset in range(0, minutes):
        stamp = start + timedelta(minutes=offset)
        values = [
            random.randint(bound, bound * 2)
            for bound in range(offset + 1, offset + 11)
        ]
        counts = [random.randint(1, offset + 1) for _ in range(10)]
        cw_wrapper.put_metric_data_set(
            metric_namespace,
            metric_name,
            stamp,
            "Count",
            {
                "values": values,
                "counts": counts,
            },
        )
        print("  data set: ", "  values ", values, "  counts ", counts)

    alarm_name = "high_page_views"
    if g_config_use_dimension:  # new using dimension
        alarm_name = alarm_name + "_dim1_inst1"
    period = 60
    eval_periods = 2
    print(f"Creating alarm {alarm_name} for metric {metric_name}.")
    alarm = cw_wrapper.create_metric_alarm(
        metric_namespace,
        metric_name,
        alarm_name,
        "Maximum",
        period,
        eval_periods,
        100,
        "GreaterThanThreshold",
    )
    print(f"Alarm ARN is {alarm.alarm_arn}.")
    print(f"Current alarm state is: {alarm.state_value}.")

    print(
        f"Sending data to trigger the alarm. This requires data over the threshold "
        f"for {eval_periods} periods of {period} seconds each."
    )
    while alarm.state_value == "INSUFFICIENT_DATA":
        print("Sending data for the metric.")
        the_value = random.randint(100, 200)
        cw_wrapper.put_metric_data(
            metric_namespace, metric_name, the_value, "Count"
        )
        print("  data: ", "  value ", the_value)
        alarm.load()
        print(f"Current alarm state is: {alarm.state_value}.")
        if alarm.state_value == "INSUFFICIENT_DATA":
            print(f"Waiting for {period} seconds...")
            time.sleep(period)
        else:
            print("Wait for a minute for eventual consistency of metric data.")
            time.sleep(period)
            if alarm.state_value == "OK":
                alarm.load()
                print(f"Current alarm state is: {alarm.state_value}.")

    print(
        f"Getting data for metric {metric_namespace}.{metric_name} during timespan "
        f"of {start} to {datetime.utcnow()} (times are UTC)."
    )
    stats = cw_wrapper.get_metric_statistics(
        metric_namespace,
        metric_name,
        start,
        datetime.utcnow(),
        60,
        #docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Statistics-definitions.html
        # must be in the set [SampleCount, Average, Sum, Minimum, Maximum]
        ["Average", "Minimum", "Maximum", "SampleCount"],
    )
    print(
        f"Got {len(stats['Datapoints'])} data points for metric "
        f"{metric_namespace}.{metric_name}."
    )
    pprint(sorted(stats["Datapoints"], key=lambda x: x["Timestamp"]))

    if g_config_use_dimension:  # new using dimension
        # I can't tell how to get an alarm for a dimensioned metric.
        # just reuse the previous alarm object
        alarm.load()
        print(f"Alarm {alarm.name} is currently in state {alarm.state_value}.")
    else:
        print(f"Getting alarms for metric {metric_name}.")
        alarms = cw_wrapper.get_metric_alarms(metric_namespace, metric_name)
        for alarm in alarms:
            print(f"Alarm {alarm.name} is currently in state {alarm.state_value}.")

    #print(f"Deleting alarms for metric {metric_name}.")
    #cw_wrapper.delete_metric_alarms(metric_namespace, metric_name)

    print("Thanks for watching!")
    print("-" * 88)


# snippet-end:[python.example_code.cloudwatch.Usage_MetricsAlarms]


'''
boto3.amazonaws.com
/v1/documentation/api/latest/reference/services/cloudwatch/client/put_metric_data.html

request syntax: 
response = client.put_metric_data(
    Namespace='string',
    MetricData=[
        {
            'MetricName': 'string',
            'Dimensions': [
                {
                    'Name': 'string',
                    'Value': 'string'
                },
            ],
            'Timestamp': datetime(2015, 1, 1),
            'Value': 123.0,
            'StatisticValues': {
                'SampleCount': 123.0,
                'Sum': 123.0,
                'Minimum': 123.0,
                'Maximum': 123.0
            },
            'Values': [
                123.0,
            ],
            'Counts': [
                123.0,
            ],
            'Unit': 'Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None',
            'StorageResolution': 123
        },
    ]
)
'''


if __name__ == "__main__":
    import os
    osenv = os.environ
    user_access_key_id = osenv.get("AWS_ACCESS_PUBLIC_KEY", None)
    user_secret_access_key = osenv.get("AWS_ACCESS_SECRET_KEY", None)
    user_region = "us-east-2"

    usage_demo(user_access_key_id, user_secret_access_key, user_region)

