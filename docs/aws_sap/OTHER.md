---
layout: technical
title: Other
category: AWS SAP
difficulty: Advanced
show_back_link: true
---

## Other Services

### AWS Config
AWS Config is a service that enables you to assess, audit, and evaluate the configurations of your AWS resources. It helps you monitor and record your AWS resource configurations and allows you to automate the evaluation of recorded configurations against desired configurations

Conformance packs are a collection of AWS Config rules and remediation actions that can be easily deployed in an account and region which are considered best practices

### App Stream
- Desktop app streaming service, i.e. it's a service that streams to us desktop applications
- Deliver a specific application to any computer without provisioning infrastructure
- Application delivered from within a web browser

### AWS Device Farm
- App testing service for mobile and web apps
- Test across real browsers and real phones
- Fully automated using framework
- Can remotely login to devices for debugging to figure out why it works on one OS and not the other!

### CICD
Done in Code Pipeline / CodeBuild / CodeDeploy CICD

- Continuous Integration:
    - As new code is pushed, testing is automatically done via testing / build servers
    - Helps us to check code for errors or things that "worked on developers laptop"
    - Developer gets feedback quickly
- Continuous Delivery:
    - Ensure software can be released reliably whenever needed
    - Ensure deployment happens often and are quick
    - As build servers run in Continuous Integration, it can be released to a Deployment Server with specific tags and versions
- ***Code***: Github
- ***Build***: Github, Jenkins, AWS CodeBuild
- ***Test***: Github, AWS CodeBuild
- ***Deploy***: Many things here, all depends on where packages need to end up
    - AWS Beanstalk
    - Github
    - AWS CodeDeploy
- ***Provision***: EC2 Fleet, Spark cluster, K8's cluster, etc...
- ***Orchestrator***: Github Workflows, AWS CodePipeline

CodePipeline and GitHub have some integrations as well, usually use GitHub WebHooks into CodePipeline or a CodeStar pipeline to sync GitHub and CodePipeline

CodePipeline is used for orchestrating the CICD process, and CodeBuild is used for building and testing code
    - Codepipeline has stages, and each stage can have multiple actions
        - Actions can be things like source, build, test, deploy, etc...
        - The results can go to S3, Beanstalk, lambda, ECS, etc...
    - CodeBuild is used to run the actual build and test commands
        - This is for when we need to do `gradle build`, ``mvn package`, `npm install`, etc...
        - CodeBuild is a step in CodePipeline

### CodeGuru
- ML powered services for code reviews and app performance recommendations
    - ***CodeGuru Reviewer***: Automated code reviews for static code analysis (development)
    - ***CodeGuru Profilier***: Visibility / recommendations about application performance during runtime (production)
- Supports Java and Python
- Integrates with GitHub and CodePipeline as a whole

### Macie
- Data security and data privacy service
- Helped to identify and alert you to sensitive PII data
- Analyzes data in S3, and notifies Amazon EventBridge

### Cloud9
- Cloud based IDE
- Write, run, and debug code with just a browser
- Can commit code directly to CodeCommit repos, which then integrate with CodePipeline
- Comes with terminal with AWS CLI pre-installed and configured
- Prepackaged with essential tools for popular programming languages
- Collaborate with others in real-time
- Integrates with some core AWS Services for code deployment
    - Lambda, CodeCommit, CodePipeline, Beanstalk, etc...

### SES
- Simple Email Service
- API or SMTP server
- Outbound and Inbound (can receive replies)
- Provides stats like deliveries, bounces, feedback loop, email opened, etc...
- Supports DomainKeys Identified Mail and Sender Policy Frameworks
- Flexible IP deployment: shared, dedicated, and customer-owned IP's
- Send emails using your app using Console, API's, or SMTP
- Good for mass mail marketing, integrating with Personalize and EventBridge
- Configuration Sets:
    - Customize and analyze your email send events
    - Event destinations:
        - Kinesis Data Firehose: Receives metrics for each email (bounces, clicks, opens, etc)
            - Write into Data Analytics ot S3 (Athena can query S3 then)
        - SNS: For immediate feedback on bounce and complaint information
    - IP Pool Management: Use IP pools to send particular types of emails

### Pinpoint
- Scalable, 2-way (inbound and outbound) marketing communication service
- Supports emails, SMS, push, voice, and in-app messaging
- Billions of messages per day
- Use cases:
    - Running marketing campaigns by sending marketing, bulk, or transactional SMS messages

- How to use this compared to SNS vs SES?
    - SNS and SES you must manage all end users and content
    - Pinpoing allows us to do templating, delivery schedules, targeted segments, etc so it's just a specific implementation on top of these tools

### EC2 Image Builder
- Helps to automate creation of VM's or container images
- Automate creation, maintenance, and validation of EC2 AMI's
    - Can spin up an EC2 and automatically run specific tests if desired
- Can publish these AMI's to multiple regions and accounts
- Run on a schedule
- Builds and packages up everything onto an AMI
- CICD Flow (CodePipeline):
    - Build Code:
        - Github / Something
        - AWS CodeBuild
    - Build AMI
        - AWS CloudFormation
        - EC2 Image Builder
        - AMI!
    - Rollout
        - AWS CloudFormation

### IoT Core
- Internet of Things
- Network of internet connected devices that are able to collect and transfer data
- AWS IoT Core allows you to easily connect IOT devices to AWS cloud
- Serverless & secure
- Scales to billions of devices and trillions of messages
- Integrates with multiple AWS services
    - Lambda, Sagemaker, S3, Kinesis, etc
    - IoT Topics:
        - Ingest via MQTT protocol
        - Filter down with IoT Rules
        - Act with IoT Rules Actions
    - Integrate
        - Lots of them, focus on:
        - Kinesis Data Firehose
            - IoT Core sends MQTT, which is sent to Kinesis Firehose by way of IoT Core Rules Actions
            - Can use this to transform and send downstream for aggregation and analysis
- Build IoT apps that gather, process, analyze, and act upon data