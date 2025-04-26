# Use AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.11 

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY lambda_handler.py ./
COPY news_report ./news_report

# Command to run the Lambda function
CMD ["lambda_handler.handler"]
