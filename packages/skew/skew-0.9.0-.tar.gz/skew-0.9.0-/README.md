skew
====

[![Build Status](https://travis-ci.org/scopely-devops/skew.svg?branch=develop)](https://travis-ci.org/scopely-devops/skew)

**Skew** is a package for identifying and enumerating cloud resources.
The name is a homonym for SKU (Stock Keeping Unit).  Skew allows you to
define different SKU ``schemes`` which are a particular encoding of a
SKU.  Skew then allows you to use this scheme pattern and regular expressions
based on the scheme pattern to identify and enumerate a resource or set
of resources.

At the moment, the the only available ``scheme`` is the ``ARN`` scheme.
The ``ARN`` scheme uses the basic structure of
[Amazon Resource Names](http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html) (ARNs) to assign a unique identifier to every AWS
resource.

An example ARN pattern would be:

    arn:aws:ec2:us-west-2:123456789012:instance/i-12345678

This pattern identifies a specific EC2 instance running in the ``us-west-2``
region under the account ID ``123456789012``.  The account ID is the 12-digit
unique identifier for a specific AWS account as described
[here](http://docs.aws.amazon.com/general/latest/gr/acct-identifiers.html).
To allow **skew** to find your account number, you need to add it to your
botocore/AWSCLI config file.  For example:

    [profile prod]
    aws_access_key_id = <my access key>
    aws_secret_access_key = <my secret key>
    region = us-west-2
    account_id = 123456789012

Skew will look through all of the profiles defined in your config file and
keep track of all of the ones that have an ``account_id`` associated with
them.

The main point of skew is to identify AWS resources or sets of resources and
to quickly and easily return the data associated with those resources.
For example, if you wanted to return the data associated with the example
ARN above:

    from skew import scan

	arn = scan('arn:aws:ec2:us-west-2:123456789012:instance/i-12345678')
	for resource in arn:
	    print(resource.data)

The call to ``scan`` returns an ARN object which implements the
[iterator pattern](https://docs.python.org/2/library/stdtypes.html#iterator-types)
and returns a ``Resource`` object for each AWS resource that matches the
ARN pattern provided.  The ``Resource`` object contains all of the data
associated with the AWS resource in dictionary under the ``data`` attribute.

Any of the elements of the ARN can be replaced with a regular expression.
The simplest regular expression is ``*`` which means all available choices.
So, for example:

    arn = scan('arn:aws:ec2:us-east-1:*:instance/*')

would return an iterator for all EC2 instances in the ``us-east-1`` region
found in all accounts defined in the config file.

To find all DynamoDB tables in all US regions for the account ID 234567890123
you would use:

    arn = scan('arn:aws:dynamodb:us-.*:234567890123:table/*')

CloudWatch Metrics
------------------

In addition to making the metadata about a particular AWS resource available
to you, ``skew`` also tries to make it easy to access the available CloudWatch
metrics for a given resource.

For example, assume that you had did a ``scan`` on the original ARN above
and had the resource associated with that instance available as the variable
``instance``.  You could do the following:

    >>> instance.metric_names
	['CPUUtilization',
     'NetworkOut',
     'StatusCheckFailed',
     'StatusCheckFailed_System',
     'NetworkIn',
     'DiskWriteOps',
     'DiskReadBytes',
     'DiskReadOps',
     'StatusCheckFailed_Instance',
     'DiskWriteBytes']
	 >>>

The ``metric_names`` attribute returns the list of available CloudWatch metrics
for this resource.  The retrieve the metric data for one of these:

    >>> instance.get_metric_data('CPUUtilization')
	[{u'Average': 0.134, u'Timestamp': '2014-09-29T14:04:00Z', u'Unit': 'Percent'},
     {u'Average': 0.066, u'Timestamp': '2014-09-29T13:54:00Z', u'Unit': 'Percent'},
     {u'Average': 0.066, u'Timestamp': '2014-09-29T14:09:00Z', u'Unit': 'Percent'},
     {u'Average': 0.134, u'Timestamp': '2014-09-29T13:34:00Z', u'Unit': 'Percent'},
     {u'Average': 0.066, u'Timestamp': '2014-09-29T14:19:00Z', u'Unit': 'Percent'},
     {u'Average': 0.068, u'Timestamp': '2014-09-29T13:44:00Z', u'Unit': 'Percent'},
     {u'Average': 0.134, u'Timestamp': '2014-09-29T14:14:00Z', u'Unit': 'Percent'},
     {u'Average': 0.066, u'Timestamp': '2014-09-29T13:29:00Z', u'Unit': 'Percent'},
     {u'Average': 0.132, u'Timestamp': '2014-09-29T13:59:00Z', u'Unit': 'Percent'},
     {u'Average': 0.134, u'Timestamp': '2014-09-29T13:49:00Z', u'Unit': 'Percent'},
     {u'Average': 0.134, u'Timestamp': '2014-09-29T13:39:00Z', u'Unit': 'Percent'}]
    >>>

You can also customize the data returned rather than using the default settings:

    >>> instance.get_metric_data('CPUUtilization', hours=8, statistics=['Average', 'Minimum', 'Maximum'])
	[{u'Average': 0.132,
      u'Maximum': 0.33,
      u'Minimum': 0.0,
      u'Timestamp': '2014-09-29T10:54:00Z',
      u'Unit': 'Percent'},
     {u'Average': 0.134,
      u'Maximum': 0.34,
      u'Minimum': 0.0,
      u'Timestamp': '2014-09-29T14:04:00Z',
      u'Unit': 'Percent'},
	  ...,
     {u'Average': 0.066,
      u'Maximum': 0.33,
      u'Minimum': 0.0,
      u'Timestamp': '2014-09-29T08:34:00Z',
      u'Unit': 'Percent'},
     {u'Average': 0.134,
      u'Maximum': 0.34,
      u'Minimum': 0.0,
      u'Timestamp': '2014-09-29T08:04:00Z',
      u'Unit': 'Percent'}]
    >>>
	  
	  
