Floresta - VPC automation tool
==============================

Installing
----------

.. code:: sh

    pip install floresta

Creating the whole VPC
----------------------

it takes around 10 minutes to create a brand new VPC from scratch: all
the security groups, subnets, route tables, ec2 instances, internet
gateway, stitch them together and run their ansible playbooks, if you
want to.

.. code:: sh

    # supposing that you keep your vpc yaml files inside of ./vpcs/

    floresta vpcs/myvpc.yml

Amazon Policy
=============

When running boteco with ``--ensure-vpc`` your user will need the
following policy

.. code:: json

    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": [
            "ec2:CreateTags",
            "ec2:CreateVpc",
            "ec2:CreateSubnet",
            "ec2:DescribeAvailabilityZones",
            "ec2:CreateRouteTable",
            "ec2:CreateRoute",
            "ec2:CreateInternetGateway",
            "ec2:AttachInternetGateway",
            "ec2:AssociateRouteTable",
            "ec2:ModifyVpcAttribute",
            "ec2:DescribeInternetGateways",
            "ec2:DescribeVpcs",
            "ec2:DescribeSubnets",
            "ec2:DescribeRouteTables",
            "ec2:DescribeAddresses",
            "ec2:DescribeSecurityGroups",
            "ec2:DescribeNetworkAcls",
            "ec2:DescribeDhcpOptions",
            "ec2:DescribeTags",
            "ec2:DescribeInstances",
            "ec2:DescribeInstanceStatus",
            "ec2:DeleteRoute",
            "route53:GetHostedZone",
            "route53:ListResourceRecordSets",
            "route53:ChangeResourceRecordSets",
            "ec2:AttachVolume",
            "ec2:AuthorizeSecurityGroupEgress",
            "ec2:AuthorizeSecurityGroupIngress",
            "ec2:RevokeSecurityGroupEgress",
            "ec2:RevokeSecurityGroupIngress",
            "ec2:RunInstances",
            "ec2:StartInstances",
            "ec2:CreateVpcPeeringConnection",
            "ec2:AcceptVpcPeeringConnection",
            "ec2:CreateSecurityGroup",
            "ec2:ModifyInstanceAttribute"
          ],
          "Resource": "*",
          "Effect": "Allow"
        }
      ]
    }

