# INFO

**Español:** Este proyecto y/o repositorio, al igual que todos los demás, está liberado bajo la licencia AGPL. Para más información, visita este enlace: [README](https://github.com/LlibertadApp/.github/blob/main/profile/README.md).

**English** This project and/or repository, like all others, is released under the AGPL license. For more information, please visit this link: [README](https://github.com/LlibertadApp/.github/blob/main/profile/README.md).





# s3-data-processing

### Deployment

Install dependencies with:

```
npm install
```

Then deploy:

```
serverless deploy
```

After running deploy, you should see output similar to:

```bash
Deploying aws-python-sqs-worker-project to stage dev (us-east-1)

✔ Service deployed to stack aws-python-sqs-worker-project-dev (175s)

endpoint: POST - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/produce
functions:
  producer: aws-python-sqs-worker-project-dev-producer (167 kB)
  jobsWorker: aws-python-sqs-worker-project-dev-jobsWorker (167 kB)
jobs: https://sqs.us-east-1.amazonaws.com/000000000000/aws-python-sqs-worker-project-dev-jobs
```

_Note_: In current form, after deployment, your API is public and can be invoked by anyone. For production deployments, you might want to configure an authorizer. For details on how to do that, refer to [http event docs](https://www.serverless.com/framework/docs/providers/aws/events/apigateway/).

### Invocation

After successful deployment, you can now call the created API endpoint with `POST` request to invoke `producer` function:

```bash
curl --request POST 'https://xxxxxx.execute-api.us-east-1.amazonaws.com/produce' --header 'Content-Type: application/json' --data-raw '{"name": "John"}'
```

In response, you should see output similar to:

```bash
{"message": "Message accepted!"}
```

### Bundling dependencies

In case you would like to include 3rd party dependencies, you will need to use a plugin called `serverless-python-requirements`. You can set it up by running the following command:

```bash
serverless plugin install -n serverless-python-requirements
```

Running the above will automatically add `serverless-python-requirements` to `plugins` section in your `serverless.yml` file and add it as a `devDependency` to `package.json` file. The `package.json` file will be automatically created if it doesn't exist beforehand. Now you will be able to add your dependencies to `requirements.txt` file (`Pipfile` and `pyproject.toml` is also supported but requires additional configuration) and they will be automatically injected to Lambda package during build process. For more details about the plugin's configuration, please refer to [official documentation](https://github.com/UnitedIncome/serverless-python-requirements).


# SQS Policy and Event
To enable S3 events to use the Queue as a target, the access policy provided below must be added to the Queue.  
This solution was provided by [Shilp Thapak](https://stackoverflow.com/users/15030095/shilp-thapak) on [stackoverflow](https://stackoverflow.com/a/68406363).  
Note: the bucket event configuration and the policy were manually created.
```
{
  "Version": "2012-10-17",
  "Id": "<example-ID>",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Action": [
        "SQS:SendMessage"
      ],
      "Resource": "arn:aws:sqs:<region>:<account-id>:<queue-name>",
      "Condition": {
        "ArnLike": {
          "aws:SourceArn": "arn:aws:s3:::<my-bucket-name>"
        },
        "StringEquals": {
          "aws:SourceAccount": "<bucket-owner-account-id>"
        }
      }
    }
  ]
}
```
