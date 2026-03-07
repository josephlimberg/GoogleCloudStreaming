import os
import json
from google.cloud import pubsub_v1

# Configuración de credenciales
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keypub.json"

# Configuración del proyecto y tópico
project_id = "josepgbigquery"
topic_id = "topic1"

# Inicializar el cliente de Publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Estructura del mensaje (Datos del sensor)
mensaje = {
    "sensor_id": "sensor-01",
    "temperatura": 28.4,
    "humedad": 65.2,
    "timestamp": "2025-10-22T20:00:00Z"
}

# Publicar como JSON (sin Avro)
# 1. Convertimos el diccionario a una cadena JSON y luego a bytes (utf-8)
data = json.dumps(mensaje).encode("utf-8")

# 2. Publicamos el mensaje
future = publisher.publish(topic_path, data)

# 3. Resultado de la publicación
print(f"Publicado con ID: {future.result()}")