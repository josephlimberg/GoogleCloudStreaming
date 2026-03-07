import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json

# 1. Definición de la lógica de transformación (DoFn)
class ParseSensorData(beam.DoFn):
    def process(self, element):
        try:
            # El elemento llega como un string de JSON desde Pub/Sub
            data = json.loads(element)
            
            # Validación de campos obligatorios
            if "sensor_id" in data and "temperatura" in data and "humedad" in data:
                yield {
                    "sensor_id": data["sensor_id"],
                    "temperatura": float(data["temperatura"]),
                    "humedad": float(data["humedad"]),
                    "timestamp": data["timestamp"]
                }
        except Exception as e:
            # En producción, considera loggear el error o enviar a una "Dead Letter Queue"
            pass

# 2. Configuración de opciones del Pipeline (GCP Dataflow)
options = PipelineOptions(
    project="josepgbigquery",
    region="us-central1",
    streaming=True,
    temp_location="gs://dataflow_t1/temp/"
)

# 3. Construcción del Pipeline
with beam.Pipeline(options=options) as p:
    (
        p 
        | "Leer mensajes de Pub/Sub" >> beam.io.ReadFromPubSub(
            topic="projects/josepgbigquery/topics/topic1"
        )
        | "Parsear JSON" >> beam.ParDo(ParseSensorData())
        | "Filtrar datos invalidos" >> beam.Filter(
            lambda x: 0 <= x["temperatura"] <= 100
        )
        | "Guardar en BigQuery" >> beam.io.WriteToBigQuery(
            table="josepgbigquery.iot_data.sensores",
            schema="sensor_id:STRING, temperatura:FLOAT, humedad:FLOAT, timestamp:TIMESTAMP",
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
        )
    )