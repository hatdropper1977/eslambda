# eslambda
An example Chalice package to deploy an API Gateway/ Lambda proxy to the AWS Elasticsearch service.

For an entertaining and detailed tutorial on how to use this please see:

https:/john.soban.ski/deploy_an_advanced_elasticsearch_proxy_with_lambda.html

For the impatient:

```bash
[~]$ virtualenv working
[~]$ cd working
[working]$ source ./bin/activate
(working)[working]$ pip install -U pip
(working)[working]$ pip install awscli boto chalice httpie jsonschema
(working)[working]$ aws configure
AWS Access Key ID [None]: 4F4OJ5BO8YAZSMK75VT6
AWS Secret Access Key [None]: YVNXPN9S0D9GHTCZRC22V1KEP1MKLURVA81UYW4R
Default region name [None]: us-east-1
Default output format [None]:
(working)[working]$ export AWS_ARN_ID=012345678901 #Your AWS Account ID
(working)[working]$ export MY_IP_ADDRESS=8.7.6.5 #The IP address of you dev workstation for GUI
(working)[working]$ aws es create-elasticsearch-domain --domain-name "elastic" --elasticsearch-version "6.0" --elasticsearch-cluster-config InstanceType="t2.small.elasticsearch",InstanceCount=1,DedicatedMasterEnabled=false,ZoneAwarenessEnabled=false --ebs-options EBSEnabled=true,VolumeType="gp2",VolumeSize=10 --access-policies "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"arn:aws:iam::"$AWS_ARN_ID":root\"},\"Action\":\"es:*\",\"Resource\":\"arn:aws:es:us-east-1:"$AWS_ARN_ID":domain/elastic/*\"},{\"Sid\":\"\",\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"*\"},\"Action\":\"es:*\",\"Resource\":\"arn:aws:es:us-east-1:"$AWS_ARN_ID":domain/elastic/*\",\"Condition\":{\"IpAddress\":{\"aws:SourceIp\":[\""$MY_IP_ADDRESS"\"]}}}]}"
(working)[working]$ git clone https://github.com/hatdropper1977/eslambda.git
```
...wait 10 minutes
```bash
(working)[working]$ cd eslambda
(working)[working]$ vim chalicelib/config.py #Set ELASTICSEARCH_ENDPOINT to your new AWS Elasticsearch endpoint
(working)[eslambda]$ chalice deploy --no-autogen-policy
(working)[eslambda]$ http POST <<YOUR API Gateway URL>> agree:=true anumber:=1 textblob='abc sdf' ipaddr='192.168.10.10'
```
