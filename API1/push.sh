# construct the ECR name.
account=$(aws sts get-caller-identity --query Account --output text)
region=$(aws configure get region)
fullname="${account}.dkr.ecr.${region}.amazonaws.com/quiltdata/sagemaker-demo:latest"

# create the repository in ECR.
aws ecr create-repository --repository-name "quiltdata/sagemaker-demo" > /dev/null

# Get the login command from ECR and execute it directly
$(aws ecr get-login --region ${region} --no-include-email)

# Build the docker image, tag it with the full name, and push it to ECR
docker build  -t "quiltdata/sagemaker-demo" quilt-sagemaker-demo/
docker tag "quiltdata/sagemaker-demo" ${fullname}

docker push ${fullname}