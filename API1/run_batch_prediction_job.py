import sagemaker as sage
sess = sage.Session()
transformer = sagemaker.transformer.Transformer(
    base_transform_job_name='Batch-Transform',
    model_name='sagemaker-demo-sdc-clou',  # insert model name here
    instance_count=1,
    instance_type='ml.c4.xlarge',
    output_path='s3://quilt-example/quilt_sagemaker_demo/outputs',
    sagemaker_session=sess
)
transformer.transform(
    's3://quilt-example/quilt/race_mnist/race-mnist_train.csv', 
    content_type='text/csv', 
    split_type='Line'
)
transformer.wait()
import boto3
s3_client = boto3.resource('s3')
s3_client.download_file('s3://quilt-example/', 'quilt_sagemaker_demo/model/sdc-clou')