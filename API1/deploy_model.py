import sagemaker as sage

role = sage.get_execution_role()
sess = sage.Session()
account = sess.boto_session.client('sts').get_caller_identity()['Account']
region = sess.boto_session.region_name
image = '{}.dkr.ecr.{}.amazonaws.com/quiltdata/sagemaker-demo'.format(account, region)

clf = Model( 
    model_data='s3://quilt-example/quilt/quilt_sagemaker_demo/model/sagemaker-demo-sdc-clou/output/model.tar.gz', image=image, role=role, sagemaker_session=sess
)

predictor = clf.deploy(1, 'ml.c4.2xlarge')

predictor = sage.predictor.RealTimePredictor(
    'sagemaker-demo-sdc-clou', sagemaker_session=sess, content_type="text/csv"
)