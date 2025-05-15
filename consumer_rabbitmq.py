import json
import pika
from config import QUEUE_USER, QUEUE_PASSWORD
import ssl

class RabbitMQConsumer:
    def __init__(self, rabbitmq_host: str, rabbitmq_port: str, rabbitmq_queue: str, normalizer):
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port
        self.rabbitmq_queue = rabbitmq_queue
        self.normalizer = normalizer
        self.connection = None
        self.channel = None
        self._running = False

    def connect(self):
        """Установка соединения с RabbitMQ"""
        ssl_context = ssl.create_default_context(cafile="certs/server.crt")
        ssl_context.check_hostname = False 
        ssl_context.verify_mode = ssl.CERT_REQUIRED  # Требует валидный сертификат
        ssl_context.load_verify_locations(cafile="./certs/server.crt")  # Путь к доверенному CA

        credentials = pika.PlainCredentials(QUEUE_USER, QUEUE_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=self.rabbitmq_host,
            port=self.rabbitmq_port,
            ssl_options=pika.SSLOptions(ssl_context),
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.rabbitmq_queue, durable=True)
        print(f"Connected to RabbitMQ at {self.rabbitmq_host}:{self.rabbitmq_port}")

    def callback(self, ch, method, properties, body):
        """Обработка полученного сообщения"""
        if not self._running:
            return
            
        try:
            message = json.loads(body.decode('utf-8'))
            print(f"Received message: {message}")
            
            self.normalizer.process_message(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print("Message processed successfully")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            print(f"Message processing failed: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start_consuming(self):
        """Запуск потребителя"""
        self._running = True
        try:
            self.connect()
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(
                queue=self.rabbitmq_queue,
                on_message_callback=self.callback,
                auto_ack=False
            )
            print(f"Waiting for messages in '{self.rabbitmq_queue}'")
            
            while self._running:
                self.connection.process_data_events(time_limit=1)  # Неблокирующее ожидание
                
        except Exception as e:
            print(f"Error in consumer: {e}")
        finally:
            self.stop()

    def stop(self):
        """Корректное завершение работы"""
        self._running = False
        if hasattr(self, 'channel') and self.channel:
            try:
                self.channel.stop_consuming()
            except Exception as e:
                print(f"Error stopping consumer: {e}")
                
        if hasattr(self, 'connection') and self.connection and self.connection.is_open:
            try:
                self.connection.close()
            except Exception as e:
                print(f"Error closing connection: {e}")
                
        print("RabbitMQ consumer stopped")