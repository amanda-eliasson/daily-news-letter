# Daily Newsletter
The daily newsletter project consists of a lambda function on aws that runs once every night. 
The lambda function does 3 things: 
1. scrape omni.se for the latest news of the day
2. uses gpt-40 to summarise the news into 4 minor articles and translates them to german (including creating 10 daily vocabulary words)
3. creates and HTML template and sends an email with the news articles to the email-recipients

## Deploy email sender
### Prerequisites
AWS account is setup and the AWS cli is installed

#### Environment variables
- `AWS_ACCOUNT_NBR`=Your aws account id
- `AWS_PROFILE`=Your aws profile name

### Setup infra and deploy docker
2. `cd infra` && `./create-update-stack.sh news-letter-ecr-stack stack-template.yaml $AWS_PROFILE`
3. `cd ../` && run `./build-and-push-docker.sh`
4. `cd infra` && `./create-update-stack.sh news-letter-lambda-stack stack-template-lambda.yaml $AWS_PROFILE $ECR_REPOSITORY_URL` (Disclaimer: You cannot build lambda if no container is pushed to the ecr, ecr repository URL is created in step 2)

### Update environemnt variables lambda function
The following variables are necessary for the lambda function to run, add them to the lambda function in the aws conosle
- `SENDER_EMAIL`=gmail to send email from
- `SENDER_PASSWORD`=gmail email password
- `EMAIL_RECIPIENTS`=list of recipient emails
 

