# Amazon Connect with BankID authentication - Demo
Securely identifying customers during an inbound call can be a legal requirement for many contact centers, especially in the financial industry. BankID is by far the largest electronic identification system in Sweden, with a current usage rate of 94% among smartphone users. With BankID, you get a stable and secure solution that the vast majority of your customers already use and trust.
With Amazon Connect, you can build high-quality omnichannel voice and interactive chat experiences to support your customers from anywhere.

This code will set up a contact flow/IVR for real time authentication with Mobile BankID and can be deployed in minutes.

![contact flow](images/contact-flow.png)

Important: this application uses various AWS services and there are costs associated with these services after the Free Tier usage - please see the [AWS Pricing page](https://aws.amazon.com/pricing/) for details. You are responsible for any AWS costs incurred. No warranty is implied in this example.

### Services used
* [Amazon Connect](https://aws.amazon.com/connect/)
* [AWS Lambda](https://aws.amazon.com/connect/)

![architecture](images/architecture.png)

### Requirements for deployment
* An [Amazon account](https://aws.amazon.com/console/)
* An [Amazon Connect](https://docs.aws.amazon.com/connect/latest/adminguide/amazon-connect-get-started.html)
    * With a [claimed phone number](https://docs.aws.amazon.com/connect/latest/adminguide/claim-phone-number.html)
* Setup with [Test BankID](https://www.bankid.com/en/utvecklare/test)
* [AWS CLI](https://aws.amazon.com/cli/)
* [AWS SAM CLI v1.31.0+](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

### Setup for Test BankID
1. Install test version of Security app to mobile device which is available in the [Test Documentation](https://www.bankid.com/en/utvecklare/test).
1. Order a personal code for the test server at [demo.bankid.com](https://demo.bankid.com/).
1. Login with code from the email.
1. Follow instructions at [demo.bankid.com](https://demo.bankid.com/) to issue your BankID for testing.
1. Review the latest [BankID Relying Party Guidelines](https://www.bankid.com/assets/bankid/rp/bankid-relying-party-guidelines-v3.6.pdf) to review the latest SSL Certificate information and passcode or to request custom production certificates.
1. _(optional)_ To update the certificates for your backend code you can find the latest download link in the [testing documentation](https://www.bankid.com/en/utvecklare/test).

_For more information on BankID integration, please review their documentation [here](https://www.bankid.com/en/utvecklare/guider)._

### Deployment
The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications.

```bash
# Optional
# !!!! FOR BANK ID TESTING ENV ONLY !!!
# This command only needs run once. Once the pem files have been generated there's no need to run this again.
# This step is not required if using new or private certificates with BankID
./get-latest-bankid-certificates.sh

# You will be then requested to input the BankID Passphrase from
# https://www.bankid.com/assets/bankid/rp/bankid-relying-party-guidelines-v3.6.pdf
> Please enter the BankID Passphase:

# It is not recommended to use a password as an argument in a bash script. However since the password is already on the public internet the scipt has been provided for convenience. Please use with caution and delete when progressing to personal or production certs.
```

In the terminal, use the SAM CLI guided deployment the first time you deploy.
```bash
sam build
sam deploy --guided
```

Before testing, you will need to configure the new contact flow/IVR to your claimed phone number. If you need to claim a new phone number follow these [instructions](https://docs.aws.amazon.com/connect/latest/adminguide/claim-phone-number.html). You can then associate your new `0000 BankID Authentication` to your claimed number by following these [instructions](https://docs.aws.amazon.com/connect/latest/adminguide/associate-phone-number.html).
Now your new contact flow is ready to try out!


#### Choose options
You can choose the default options, however remember to pass in the Arn for your Amazon Connect instance or the deployment will not be sucessful.

```bash
## The name of the CloudFormation stack
Stack Name [sam-app]:

## The region you want to deploy in
AWS Region [eu-north-1]:

## The Arn of your existing Amazon Connect Instance
Parameter ConnectArn []:

## Shows you resources changes to be deployed and requires a 'Y' to initiate deploy
Confirm changes before deploy [y/N]:

## SAM needs permission to be able to create roles to connect to the resources in your template
Allow SAM CLI IAM role creation [Y/n]:

## Save your choice for later deployments
Save arguments to samconfig.toml [Y/n]:
```

SAM will then deploy the AWS CloudFormation stack to your AWS account.

### Call and test
Call your claimed number that you set up for the contact flow and follow instructions on the call.

You will be asked:
1. To enter your personal number. **This has to be a personal number you setup for Test BankID**
2. Open up your Test BankID app to identify yourself.
3. Congratulations! You have now authenticated yourself via BankID and will be greeted by your name.

## Cleanup
```bash
## Delete the stack via the SAM CLI
sam delete
```

## Recommendation for Production credentials
In this example we bundled the pem keys in with the lambda function for test and demo purposes. For a workload like this to be production ready it is **strongly** recommended to use a Secrets Manager to securely store your keys. Please review the resources below to implement a solution using AWS Secrets Manager:

* [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) helps you protect secrets needed to access your applications, services, and IT resources.
* [How to use AWS Secrets Manager to securely store and rotate SSH key pairs](https://aws.amazon.com/blogs/security/how-to-use-aws-secrets-manager-securely-store-rotate-ssh-key-pairs/)
* [How to securely provide database credentials to Lambda functions by using AWS Secrets Manager](https://aws.amazon.com/blogs/security/how-to-securely-provide-database-credentials-to-lambda-functions-by-using-aws-secrets-manager/)

## License
This library is licensed under the MIT-0 License. See the LICENSE file.