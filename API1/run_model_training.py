import sagemaker as sage

role = sage.get_execution_role()

sess = sage.Session()
account = sess.boto_session.client('sts').get_caller_identtity()['Account']
region = session.boto_session.region_name
image = '${}.dkr.ecr.{}.amazonaws.com/quiltdata/sagemaker-demo'.format(
    account, region)
clf = sage.estimator.Estimatort(
    image, role, 1, 'ml.c4.2xlarge', output_path="s3://quilt-exemple/quilt/quilt")
