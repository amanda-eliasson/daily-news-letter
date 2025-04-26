#!/bin/bash
echo "logging in to aws"
aws --profile $AWS_PROFILE ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_NBR.dkr.ecr.us-east-1.amazonaws.com

echo "building docker image"
docker build -t news-letter-stack . 

echo "tagging image" 
docker tag news-letter-stack:latest $AWS_ACCOUNT_NBR.dkr.ecr.us-east-1.amazonaws.com/news-letter-stack:latest

echo "pushing to ecr"
docker push $AWS_ACCOUNT_NBR.dkr.ecr.us-east-1.amazonaws.com/news-letter-stack:latest