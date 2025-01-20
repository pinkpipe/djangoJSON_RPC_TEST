import json
import socket
import ssl
from urllib.parse import urlparse
from http.client import HTTPConnection, HTTPSConnection, HTTPException

from django.conf import settings



class JSONRPCException(Exception):
    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data

    def __str__(self):
        return f"JSONRPC Error {self.code}: {self.message}"


class JSONRPCClient:
    def __init__(self, endpoint, cert, key):
        self.endpoint = endpoint
        self.cert = cert
        self.key = key
        self.parsed_url = urlparse(endpoint)

    def _create_ssl_context(self):
        import os
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True

        cert_path = os.path.join(settings.BASE_DIR, 'json_rpc', 'path', 'ssl', 'testx1.crt')
        context.load_verify_locations(cafile=cert_path)

        temp_cert_file = 'temp_cert.pem'
        temp_key_file = 'temp_key.pem'
        with open(temp_cert_file, 'w') as f:
            f.write(self.cert)
        with open(temp_key_file, 'w') as f:
            f.write(self.key)

        context.load_cert_chain(certfile=temp_cert_file, keyfile=temp_key_file)

        # Удаляем временные файлы
        import os
        os.remove(temp_cert_file)
        os.remove(temp_key_file)



        return context

    def call(self, method, params=None):
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": 1
        }

        try:
            if self.parsed_url.scheme == "https":
                context = self._create_ssl_context()
                conn = HTTPSConnection(self.parsed_url.netloc, context=context, timeout=5)

            else:
                conn = HTTPConnection(self.parsed_url.netloc, timeout=5)

            conn.request("POST", self.parsed_url.path, json.dumps(payload), headers)
            response = conn.getresponse()
            data = response.read().decode()
            conn.close()

            result = json.loads(data)

            if "error" in result:
                raise JSONRPCException(result["error"]["code"], result["error"]["message"], result["error"].get("data"))

            return result.get("result")

        except (HTTPException, socket.timeout, ConnectionRefusedError, ssl.SSLError) as e:
            raise JSONRPCException(-32000, f"Server error: {e}")
        except json.JSONDecodeError:
            raise JSONRPCException(-32700, "Parse error")
        except Exception as e:
            raise JSONRPCException(-32000, f"Client Error: {e}")