import socket
import json

class SocketDataClient():
    def __init__(self, host, port=5555, normalizer=None):
        self.host = host
        self.port = port
        self.normalizer = normalizer
        self._running = False
        self._socket = None
    
    def start_consuming(self):
        self._running = True
        try:
            print(type(self.port))
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self.host, self.port))
            print(f"Подключено к серверу {self.host}:{self.port}")
            
            while self._running:
                data = self._socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                try:
                    row = json.loads(data)
                    self.normalizer.process_message(row)
                    self._socket.send(b'ACK')
                except json.JSONDecodeError:
                    print(f"Ошибка декодирования: {data}")
                    self._socket.send(b'ERROR')
                except Exception as e:
                    print(f"Ошибка обработки: {e}")
                    self._socket.send(b'ERROR')
        
        except Exception as e:
            print(f"Ошибка соединения: {e}")
        finally:
            if self._socket:
                self._socket.close()
    
    def stop(self):
        self._running = False
        if self._socket:
            self._socket.close()