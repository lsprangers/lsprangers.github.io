---
layout: technical
title: Machine Learning
category: AWS SAP
difficulty: Advanced
show_back_link: true
---

## Machine Learning

### Rekognition
Helps us to do segmentation, object detection, and OCR in images and videos

In general helps us to place bounding boxes and label them

Use Cases:
- Labeling
- Content moderation
    - Helpful in detecting harmful cntent which is unwanted or offensive
    - Returns a content threshold with a confidence level
    - This allows us to do Human manual review via ***Amazon Augmented AI (A2I)***
- Text detection
- Face detection and analysis
- Face search and verification
- Celebrity recognition
- Pathing (like sports game analysis)

### Transcribe
Automatically convert speech to text

Uses Automatic Speeech Recognition (ASR), and lets us automatically remove PII with automatic language identification

Use cases:
- Customer service calls
- Automated closed captioning
- Generating metadata for media assets for archiving and search

### Polly
Does the opposite of Transcribe!

Polly takes text and turns it into lifelike speech. Allows us to create applications that can talk

- *Lexicons* help us to altar what text should be read as compared to what it's typed as
- *Speech markup language* allows us to style the kind of speaking that comes out

- Customize pronunciation of words with ***Pronunciation Lexicons***
    - Stylized words "L337" should be pronounced "Leyt"
    - "AWS" -> Amazon Web Services
    - etc
    - Upload them and use in the `SynthesizeSpeech` operation
- Generate speech frmo plain text or from documents marked up with ***Speech Synthesis Markup Language (SSML)***
    - Emphasizing specific words or phrases!
    - Using phönetic pronunciation
    - Including breathing sounds, or ~whispering~
    - Using the *Newscaster* speaking style

### Translate
Allows us to do natural and accurate language translation

- Localize content such as websites and applications
- Also does for international users, and allows us to easily translate large volumes of text efficiently

### Lex
Same thing that powers Amazon Alexa 

Automatic speech recognition that allows us to convert speech into text

- Automated Speech Recognition to convert speech to text
- Natural language understanding to recognize intent of text, callers
- Integrates with ***Amazon Connect***
    - Receive calls, create contact flows, and help establish cloud based customer contact center
    - Can integrate with other CRM systems or AWS Services
    - No upfront payments, and 80% cheaper than traditional contact center solutions

The entire solution of Lex is around automating speech understanding in scenarios, most specifically contact centers or customer service

### Comprehend
- NLP!
- Fully managed and serverless
- Use cases:
    - Language detection
    - Key phrases, places, people, brands, or events
    - Sentiment analysis
    - Analyzes text using tokenization and parts of speceh
    - Organizes and collection of text files by topic
        - Topic modeling

#### Comprehend Medical
- Detects and returns useful information in unstructured clinical text
    - Physicians notes
    - Dischare summaries
    - Test results
    - etc
- Uses NLP to detect Protected Health Information (PHI)
- Upload all documents into S3 and have Comprehend Medical analyze it

### Sagemaker
Fully managed service for developers / data scientists to build ML models

- Helps to create ML Platforms
- Typically difficult to do all processes of typical ML platform in one place while provisioning servers - all of these services are covered:
    - Data
        - Labeling
        - Transformations
        - Feature creation
    - Modeling
        - Training
        - Tuning
    - Deployment
        - New data coming in
        - Feedback loop
        - Inference code

### Kendra
Document Search Service

- Helps us to extract answers from within a document
- Natural language search abilities
    - "Where are the offices" - indexes all of our documents and returns an answers
- Able to manually finetune results

### Personalize
- Fully managed ML service to build apps with real-time personalized recommendations
- Same product used by `amazon.com`
- Read input data from S3, or Amazon Personalize API for real time
- Integrates into existing websites, apps, SMS, email marketing systems, etc
- Implements in days, not months (no need to build, train, and deploy)
- Use cases:
    - Retail store shopping page
    - Media and entertainment landing page
    - etc

### Textract
Extract text, handwriting, and other data from any scanned documents using AI and ML

- Results given back as `data.json` file
- Read and process any type of document (PDF, images, etc)
