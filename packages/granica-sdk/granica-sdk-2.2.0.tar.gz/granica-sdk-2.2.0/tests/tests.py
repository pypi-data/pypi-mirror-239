import granica
import boto3
import time 

def client_tests():
    # Test signing for s3
    s3_boto = boto3.client('s3')
    s3_granica = granica.client('s3')

    lboto = s3_boto.list_buckets()
    lgranica = s3_granica.list_buckets()

    assert (lboto != lgranica)

    # Test that other services remain un-affected
    assert(boto3.client('sts').get_caller_identity()['Arn'] == granica.client('sts').get_caller_identity()['Arn'])

def test_refresh():
    s3_granica = granica.client('s3')

    # let some refreshes happen
    time.sleep(90)

def session_tests():
    # Test signing for s3
    session_boto = boto3.Session()
    session_bolt = granica.Session()

    s3_boto = session_boto.client('s3')
    s3_granica = session_bolt.client('s3')

    lboto = s3_boto.list_buckets()
    lgranica = s3_granica.list_buckets()

    assert (lboto != lgranica)

    # Test that other services remain un-affected
    assert(session_boto.client('sts').get_caller_identity()['Arn'] == session_bolt.client('sts').get_caller_identity()['Arn'])


client_tests()
session_tests()
# test_refresh()