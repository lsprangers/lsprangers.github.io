---
layout: technical
title: Migration
category: AWS SAP
difficulty: Advanced
show_back_link: true
---

## Migration
Migrating to the cloud is an expensive, and hard task - this is the way to do things

Strategies for migrating applications to AWS can be broadly classified into the "7 R's":
- Rehost ("Lift and Shift")
- Replatform ("Lift, Tinker and Shift")
- Repurchase ("Drop and Shop")
- Refactor / Re-architect
- Retire
- Retain
- Relocate

Migration begins with discovery, assessment, and execution. AWS provides tools to help you discover your existing environment, plan your migration, and execute the migration itself - during that migration you can use AWS tooling, or 3rd party tools that integrate with AWS Migration Hub

These can be paired with ORR's (Operational Readiness Reviews) and MTR's (Migration Readiness Assessments) to ensure that your organization is ready for the migration:
- ORR's are focused on the application and workload being migrated
- MTR's are focused on the overall organizational readiness for migration

## AWS Migration Hub
AWS Migration Hub provides a single location to track the progress of application migrations across multiple AWS and partner solutions. You can choose the AWS and partner migration tools that best fit your needs, while gaining visibility into the status of your migrations from a single dashboard

Discovery Tools is a service that helps you plan your migration to the AWS Cloud by collecting usage and configuration data about your on-premises servers to help you better understand your workloads. You can use Discovery Tools to gather data from physical, virtual, and cloud-based environments. Ultimately it does network and server discovery, application dependency mapping, and workload resource utilization.

Agentless Discovery is ideal for large-scale server discovery and application dependency mapping. It uses a lightweight appliance to collect configuration, performance, and dependency data from servers in your data center without requiring you to install agents on each server.

There are multiple tools:
- AWS Application Discovery Service
- AWS Migration Hub
- AWS Server Migration Service (SMS)
- AWS Database Migration Service (DMS)
- AWS Schema Conversion Tool (SCT)
- AWS CloudEndure Migration
- AWS CloudEndure Disaster Recovery
- AWS DataSync
- AWS Transfer Family
- AWS Snow Family (Snowcone, Snowball, Snowmobile)
- AWS Application Migration Service (MGN)
- AWS Mainframe Modernization

## Snow Family
The AWS Snow Family consists of physical devices and capacity points that help customers move large amounts of data into and out of AWS using secure appliances. The Snow Family includes:
- AWS Snowcone: A small, rugged, and portable edge computing and data transfer device.
- AWS Snowball: A larger data transfer device with built-in computing capabilities.
- AWS Snowmobile: An exabyte-scale data transfer solution used to move extremely large amounts of data to AWS.
    - Remember, an exabyte is 1,000 petabytes or one billion gigabytes
    - A petabyte is 1,000 terabytes or one million gigabytes
    - And a GB is 1,000 megabytes