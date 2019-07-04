# construct the ECR name.
account=$(aws sts get-caller-identity --query Account --output text)
region=$(aws configure get region)
fullname="${account}.dkr.ecr.${region}.amazonaws.com/quiltdata/sagemaker-demo:latest"
REPO_NAME="quiltdata/sagemaker-demo"
echo "\nje suis la 1\n"
# create the repository in ECR.
# aws ecr create-repository --repository-name > /dev/null
aws ecr describe-repositories --repository-names ${REPO_NAME} 2>&1 > /dev/null || aws ecr create-repository --repository-name ${REPO_NAME} 2>&1 > /dev/null
echo "\nj'y suis après\n"
# Get the login command from ECR and execute it directly
$(aws ecr get-login --region ${region} --no-include-email)
echo "\n bah en faite je suis après\n"

# Build the docker image, tag it with the full name, and push it to ECR
docker build  -t ${REPO_NAME} .
docker tag ${REPO_NAME} ${fullname}

docker push ${fullname}