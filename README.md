
# Google Cloud Streaming Project

This repository holds an end-to-end data pipeline built on Google Cloud Platform. It allows publishing sensor data to Pub/Sub, processing it with Apache Beam/Dataflow, and storing it in BigQuery.
 
## Components

- **`pubsub.py`**: Python script that sends a JSON message containing `sensor_id`, `temperature`, `humidity`, and `timestamp` to a Pub/Sub topic.
- **`dataflow.py`**: defines an Apache Beam pipeline executed on Dataflow (streaming mode). It reads messages from the topic, parses JSON, validates and filters temperature values, and writes them to BigQuery.
- **`keypub.json`**: service account credentials for authenticating with Google Cloud (do not upload this to a public repo).
- **`pyproject.toml`**: project configuration and dependencies.

## Architecture
<img width="495" height="134" alt="Captura de pantalla 2026-03-07 015236" src="https://github.com/user-attachments/assets/5049be4d-2b10-4551-af85-091eeca452cc" />


## Requirements

1. Python >= 3.13
2. Google Cloud account with Pub/Sub, Dataflow, and BigQuery enabled.
3. Cloud Storage bucket for `temp_location` and `staging_location`.
4. Environment variables or credentials file (`keypub.json`).
5. Install dependencies using the `uv` package manager (the project does not use `pip`):

```bash
# with uv the dependencies declared in pyproject.toml will be installed
uv install
```

python dataflow.py \
  --runner DataflowRunner \
  --project YOUR_PROJECT_ID \
  --region YOUR_REGION \
  --temp_location gs://YOUR_BUCKET/temp/ \
  --staging_location gs://YOUR_BUCKET/staging/ \
  --job_name=sensores-streaming-$(date +%Y%m%d-%H%M%S) \
  --streaming \
  --service_account_email YOUR_SA_EMAIL

## Usage

1. Start the Dataflow pipeline.
2. Run `pubsub.py` to send test data.
3. Verify that records appear in the BigQuery table `iot_data.sensores`.

## Pub/Sub
<img width="1145" height="182" alt="Captura de pantalla 2026-03-06 205223" src="https://github.com/user-attachments/assets/58e4d64a-0534-49ad-b162-036953a215bd" />

## DataFlow
<img width="1346" height="768" alt="Captura de pantalla 2026-03-06 211604" src="https://github.com/user-attachments/assets/94eb8497-b994-4f3e-a717-f83e6f994f93" />
<img width="1080" height="252" alt="Captura de pantalla 2026-03-06 211623" src="https://github.com/user-attachments/assets/f5fbdf58-2d1c-4c64-bd3f-89e427195adc" />

## BigQuery
<img width="996" height="355" alt="Captura de pantalla 2026-03-06 211539" src="https://github.com/user-attachments/assets/ea84962d-3d64-4bea-9ae9-dc8dcf39ad43" />
