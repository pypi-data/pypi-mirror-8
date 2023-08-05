# Copyright (c) 2014 Scopely, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import logging
import datetime
from collections import namedtuple

import jmespath
import botocore.session

from skew.resources import find_resource_class
from skew.resources.resource import Resource
from skew.arn.endpoint import Endpoint

LOG = logging.getLogger(__name__)


class AWSResource(Resource):
    """
    Each Resource class defines a Config variable at the class level.  This
    is a dictionary that gives the specifics about which service the resource
    belongs to and how to enumerate the resource.

    Each entry in the dictionary we define:

    * service - The AWS service in which this resource is defined.
    * enum_spec - The enumeration configuration.  This is a tuple consisting
      of the name of the operation to call to enumerate the resources and
      a jmespath query that will be run against the result of the operation
      to retrieve the list of resources.
    * detail_spec - Some services provide only summary information in the
      list or describe method and require you to make another request to get
      the detailed info for a specific resource.  If that is the case, this
      would contain a tuple consisting of the operation to call for the
      details, the parameter name to pass in to identify the desired
      resource and the jmespath filter to apply to the results to get
      the details.
    * id - The name of the field within the resource data that uniquely
      identifies the resource.
    * dimension - The CloudWatch dimension for this resource.  A value
      of None indicates that this resource is not monitored by CloudWatch.
    * filter_name - By default, the enumerator returns all resources of a
      given type.  But you can also tell it to filter the results by
      passing in a list of id's.  This parameter tells it the name of the
      parameter to use to specify this list of id's.
    """

    class Meta(object):
        type = 'awsresource'

    @classmethod
    def filter(cls, resource_id, data):
        pass

    def __init__(self, endpoint, data):
        self._endpoint = endpoint
        self._region = endpoint.region
        self._account = endpoint.account
        if data is None:
            data = {}
        self.data = data
        if hasattr(self.Meta, 'id') and isinstance(self.data, dict):
            self._id = self.data.get(self.Meta.id, '')
        else:
            self._id = ''
        self._cloudwatch = None
        if hasattr(self.Meta, 'dimension') and self.Meta.dimension:
            cloudwatch = self._endpoint.service.session.get_service(
                'cloudwatch')
            self._cloudwatch = Endpoint(
                cloudwatch, self._region, self._account)
        self._metrics = None
        self._name = None
        self._date = None
        self._tags = None

    def __repr__(self):
        return self.arn

    @property
    def arn(self):
        return 'arn:aws:%s:%s:%s:%s/%s' % (
            self._endpoint.service.endpoint_prefix,
            self._region, self._account, self.resourcetype, self.id)

    @property
    def metrics(self):
        if self._metrics is None:
            if self._cloudwatch:
                data = self._cloudwatch.call(
                    'ListMetrics',
                    dimensions=[{'Name': self.Meta.dimension,
                                 'Value': self._id}])
                self._metrics = jmespath.search('Metrics', data)
            else:
                self._metrics = []
        return self._metrics

    @property
    def tags(self):
        """
        Convert the ugly Tags JSON into a real dictionary and
        memoize the result.
        """
        if self._tags is None:
            self._tags = {}
            if 'Tags' in self.data:
                for kvpair in self.data['Tags']:
                    if kvpair['Key'] in self._tags:
                        if not isinstance(self._tags[kvpair['Key']], list):
                            self._tags[kvpair['Key']] = [self._tags[kvpair['Key']]]
                        self._tags[kvpair['Key'].append(kvpair['Value'])]
                    else:
                        self._tags[kvpair['Key']] = kvpair['Value']
        return self._tags

    def find_metric(self, metric_name):
        for m in self.metrics:
            if m['MetricName'] == metric_name:
                return m
        return None

    def _total_seconds(self, delta):
        # python2.6 does not have timedelta.total_seconds() so we have
        # to calculate this ourselves.  This is straight from the
        # datetime docs.
        return ((delta.microseconds + (delta.seconds + delta.days * 24 * 3600)
                 * 10 ** 6) / 10 ** 6)

    def get_metric_data(self, metric_name=None, metric=None,
                        days=None, hours=1, minutes=None,
                        statistics=None, period=None):
        """
        Get metric data for this resource.  You can specify the time
        frame for the data as either the number of days or number of
        hours.  The maximum window is 14 days.  Based on the time frame
        this method will calculate the correct ``period`` to return
        the maximum number of data points up to the CloudWatch max
        of 1440.

        :type metric_name: str
        :param metric_name: The name of the metric this data will
            pertain to.

        :type days: int
        :param days: The number of days worth of data to return.
            You can specify either ``days`` or ``hours``.  The default
            is one hour.  The maximum value is 14 days.

        :type hours: int
        :param hours: The number of hours worth of data to return.
            You can specify either ``days`` or ``hours``.  The default
            is one hour.  The maximum value is 14 days.

        :type statistics: list of str
        :param statistics: The metric statistics to return.  The default
            value is **Average**.  Possible values are:

            * Average
            * Sum
            * SampleCount
            * Maximum
            * Minimum
        """
        if not statistics:
            statistics = ['Average']
        if days:
            delta = datetime.timedelta(days=days)
        elif hours:
            delta = datetime.timedelta(hours=hours)
        else:
            delta = datetime.timedelta(minutes=minutes)
        if not period:
            period = max(60, self._total_seconds(delta) // 1440)
        if not metric:
            metric = self.find_metric(metric_name)
        if metric and self._cloudwatch:
            end = datetime.datetime.utcnow()
            start = end - delta
            data = self._cloudwatch.call(
                'GetMetricStatistics',
                dimensions=metric['Dimensions'],
                namespace=metric['Namespace'],
                metric_name=metric['MetricName'],
                start_time=start.isoformat(), end_time=end.isoformat(),
                statistics=statistics, period=period)
            return jmespath.search('Datapoints', data)
        else:
            raise ValueError('Metric (%s) not available' % metric_name)


ArnComponents = namedtuple('ArnComponents',
                           ['scheme', 'provider', 'service', 'region',
                            'account', 'resource'])


def resource_from_arn(arn, data):
    session = botocore.session.get_session()
    parts = ArnComponents(*arn.split(':', 6))
    service = session.get_service(parts.service)
    if ':' in parts.resource:
        resource_type, resource_id = parts.resource.split(':')
    elif '/' in parts.resource:
        resource_type, resource_id = parts.resource.split('/')
    else:
        resource_type = parts.resource
    endpoint = Endpoint(service, parts.region, parts.account)
    resource_path = '.'.join(['aws', parts.service, resource_type])
    resource_cls = find_resource_class(resource_path)
    return resource_cls(endpoint, data)
