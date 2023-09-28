import argparse
import ipaddress
import boto3
from botocore.exceptions import NoCredentialsError

'''
def assume_role(aws_region, role_arn):
    sts_client = boto3.client('sts', region_name=aws_region)

    try:
        assumed_role = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName='AssumedRoleSession'
        )

        credentials = assumed_role['Credentials']
        return {
            'aws_access_key_id': credentials['AccessKeyId'],
            'aws_secret_access_key': credentials['SecretAccessKey'],
            'aws_session_token': credentials['SessionToken']
        }

    except NoCredentialsError as e:
        print(f"Error assuming role: {e}")
        return None
'''

def calculate_subnets(supernet, num_azs, subnet_cidr_size):
    # Calculate subnets based on the supernet and specified CIDR size
    # subnet_prefix_length = supernet.prefixlen + subnet_cidr_size

    subnets = list(supernet.subnets(new_prefix=subnet_cidr_size))

    # Check if there are enough CIDRs for the requested number of AZs    
    if len(subnets) < num_azs:
        return None, "Error: Not enough CIDRs for the requested number of AZs."
    return subnets, None

def main():
    parser = argparse.ArgumentParser(description='Calculate subnets for an AWS region.')
    parser.add_argument('supernet', type=str, help='IPv4 supernet in CIDR format')
    parser.add_argument('region', type=str, help='AWS region')
    parser.add_argument('num_azs', type=int, help='Number of available AZs in the region')
    parser.add_argument('subnet_cidr_size', type=int, help='CIDR size for subnets')
    #parser.add_argument('role_arn', type=str, help='ARN of the role to assume')

    args = parser.parse_args()

    # Parse arguments
    supernet = ipaddress.IPv4Network(args.supernet)
    aws_region = args.region
    num_azs = args.num_azs
    subnet_cidr_size = args.subnet_cidr_size
    #role_arn = args.role_arn

    # Create AWS client using assumed credentials
    aws_client = boto3.client(
        'ec2',
        region_name=aws_region,
        # **assumed_credentials
    )

    # Get availability zones in the specified region
    try:
        response = aws_client.describe_availability_zones()
        az_names = [zone['ZoneName'] for zone in response['AvailabilityZones']]
    except Exception as e:
        print(f"Error getting availability zones: {e}")
        return

    print(f"Available AZs in {aws_region}: {az_names}")
    
    if num_azs > len(az_names):
        print(f"Error: Requested {num_azs} AZs, but only {len(az_names)} AZs are available.")
        return
    
    # Calculate subnets
    subnets, error_message = calculate_subnets(supernet, num_azs, subnet_cidr_size)

    if error_message:
        print(error_message)
        return
    print(f"\nRegion: {aws_region}")
    print(f"VPC CIDR: {supernet}")
    print(f'Number of AZ: {num_azs}')
    print("\nCalculated Subnets:")
    for i, subnet in enumerate(subnets):
        if i >= num_azs:
            print(f"remaining subnets {i + 1}: {subnet}")
        else:
            print(f"Subnet {i + 1}: {subnet}")

if __name__ == '__main__':
    main()