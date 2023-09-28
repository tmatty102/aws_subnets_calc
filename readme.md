# AWS Subnet Calculator

This Python script calculates subnet CIDRs based on a given IPv4 supernet, AWS region, and the number of available Availability Zones (AZs). It assumes a role and retrieves the available AZs in the specified AWS region.

## Prerequisites

- Python 3.x
- Boto3 library (`pip install boto3`)

## Usage

1. Assume role to AWS
2. Run the following scrip
```bash
python aws_subnet_cal.py <supernet> <region> <num_azs> <subnet_cidr_size>
```

- `<supernet>`: IPv4 supernet in CIDR format (e.g., 10.0.0.0/24).
- `<region>`: AWS region where the subnets will be calculated.
- `<num_azs>`: Number of available AZs in the region.
- `<subnet_cidr_size>`: CIDR size for subnets.

## Example

### Test Case 1

```bash
python aws_subnet_cal.py 10.118.0.0/24 us-east-1 3 26
```

### Test Case 2

```bash
python aws_subnet_cal.py 10.216.0.0/21 us-west-2 4 24
```

## Output

The script will print the available AZs in the specified region and the calculated subnets.

Note: The script will exit with an error message if there are not enough CIDRs for the requested number of AZs or if the requested number of AZs exceeds the actual number of AZs in the region.

```
❯ python3 aws_subnet_cal.py 10.0.0.0/23 eu-central-1 3 26

Available AZs in eu-central-1: ['eu-central-1a', 'eu-central-1b', 'eu-central-1c']

Region: eu-central-1
VPC CIDR: 10.0.0.0/23
Number of AZ: 3

Calculated Subnets:
Subnet 1: 10.0.0.0/26
Subnet 2: 10.0.0.64/26
Subnet 3: 10.0.0.128/26
remaining subnets 4: 10.0.0.192/26
remaining subnets 5: 10.0.1.0/26
remaining subnets 6: 10.0.1.64/26
remaining subnets 7: 10.0.1.128/26
remaining subnets 8: 10.0.1.192/26
```

```
❯ python3 aws_subnet_cal.py 10.0.0.0/16 us-east-1 7 21

Available AZs in us-east-1: ['us-east-1a', 'us-east-1b', 'us-east-1c', 'us-east-1d', 'us-east-1e', 'us-east-1f']
Error: Requested 7 AZs, but only 6 AZs are available.
```
```
❯ python3 aws_subnet_cal.py 10.0.0.0/16 us-east-1 5 17

Available AZs in us-east-1: ['us-east-1a', 'us-east-1b', 'us-east-1c', 'us-east-1d', 'us-east-1e', 'us-east-1f']
Error: Not enough CIDRs for the requested number of AZs.
```