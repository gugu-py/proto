import uuid
import socket
import json
import threading
from typing import Optional, Dict

class ProxyKey:
    def __init__(self, handler_id: uuid.UUID, requester_id: uuid.UUID, receiver_id: uuid.UUID):
        self.handler_id = handler_id
        self.requester_id = requester_id
        self.receiver_id = receiver_id
        self.key = uuid.uuid4()
        self.is_expired = False
    
    def get_key(self) -> uuid.UUID:
        return self.key

    def expire(self):
        """ Mark the proxy key as expired """
        self.is_expired = True

    def is_valid_for(self, handler_id: uuid.UUID, requester_id: uuid.UUID, receiver_id: uuid.UUID) -> bool:
        """ Validate the ProxyKey """
        return (not self.is_expired and
                self.handler_id == handler_id and
                self.requester_id == requester_id and
                self.receiver_id == receiver_id)

class Element:
    def __init__(self, name: str, port: int):
        self.name = name
        self.id = uuid.uuid4()
        self.allow_direct_request: bool = False
        self.allow_indirect_request: bool = True
        self.allow_proxy_requests: bool = True
        self.connections: Dict[uuid.UUID, uuid.UUID] = {}
        self.pending_received_requests: Dict[uuid.UUID, uuid.UUID] = {}
        self.pending_sent_requests: Dict[uuid.UUID, uuid.UUID] = {}
        self.awaiting_approvals: Dict[uuid.UUID, uuid.UUID] = {}
        self.proxy_keys: Dict[tuple, ProxyKey] = {}

        # Networking attributes
        self.host = '127.0.0.1'  # Localhost for LAN
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

        # Start listening for incoming connections in a separate thread
        threading.Thread(target=self.listen_for_requests, daemon=True).start()

    def get_id(self) -> uuid.UUID:
        return self.id

    def listen_for_requests(self):
        """ Continuously listen for incoming network requests """
        print(f"[{self.name}] Listening on {self.host}:{self.port}")
        while True:
            client_socket, address = self.socket.accept()
            threading.Thread(target=self.handle_request, args=(client_socket,), daemon=True).start()

    def handle_request(self, client_socket: socket.socket):
        """ Handle incoming requests from other elements """
        with client_socket:
            data = client_socket.recv(1024).decode('utf-8')
            request = json.loads(data)
            action = request.get("action")

            # Map network actions to Element methods
            if action == "initiate_connection":
                requester_id = uuid.UUID(request.get("requester_id"))
                proxy_id = uuid.UUID(request.get("proxy_id")) if request.get("proxy_id") else None
                connection_key = uuid.UUID(request.get("connection_key"))
                self.receive_connection_request(Element.get_element_by_id(requester_id), connection_key, proxy_id)
            elif action == "approve_connection":
                requester_id = uuid.UUID(request.get("requester_id"))
                self.approve_connection(Element.get_element_by_id(requester_id))
            elif action == "send_message":
                sender_id = uuid.UUID(request.get("sender_id"))
                message = request.get("message")
                self.receive_message(Element.get_element_by_id(sender_id), message)

    def send_request(self, target: 'Element', data: dict):
        """ Send JSON data to a target element over a socket """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target.host, target.port))
            s.sendall(json.dumps(data).encode('utf-8'))

    def initiate_connection(self, target: 'Element', proxy: Optional['Element'] = None):
        connection_key = uuid.uuid4()
        self.pending_sent_requests[target.get_id()] = connection_key
        data = {
            "action": "initiate_connection",
            "requester_id": str(self.get_id()),
            "proxy_id": str(proxy.get_id()) if proxy else None,
            "connection_key": str(connection_key)
        }
        self.send_request(target, data)
        print(f"[{self.name}] Sent request to {target.name} through {proxy.name if proxy else 'direct connection'}")

    def approve_connection(self, requester: 'Element'):
        if requester.get_id() in self.pending_received_requests:
            connection_key = self.pending_received_requests.pop(requester.get_id())
            self.awaiting_approvals[requester.get_id()] = connection_key
            proxy_key = self.proxy_keys.pop((requester.get_id(), self.get_id()), None)
            if proxy_key:
                proxy_key.expire()
            data = {
                "action": "approve_connection",
                "requester_id": str(requester.get_id())
            }
            self.send_request(requester, data)
            print(f"[{self.name}] Sent approval to {requester.name}")

    def receive_connection_request(self, requester: 'Element', connection_key: uuid.UUID, proxy: Optional[uuid.UUID] = None):
        if proxy is None:
            if self.allow_direct_request:
                self.pending_received_requests[requester.get_id()] = connection_key
                print(f"[{self.name}] Received direct connection request from {requester.name}")
            else:
                print(f"[{self.name}] Blocked direct connection request from {requester.name}")
        else:
            proxy_key = self.proxy_keys.get((proxy, requester.get_id()))
            if proxy_key and proxy_key.is_valid_for(proxy, requester.get_id(), self.get_id()):
                self.pending_received_requests[requester.get_id()] = connection_key
                print(f"[{self.name}] Received proxied connection request from {requester.name} through {proxy}")
            else:
                print(f"[{self.name}] Blocked proxied request from {requester.name} through untrusted proxy")

    def send_message(self, target: 'Element', message: str):
        data = {
            "action": "send_message",
            "sender_id": str(self.get_id()),
            "message": message
        }
        self.send_request(target, data)
        print(f"[{self.name}] Sent message to {target.name}: '{message}'")

    def receive_message(self, sender: 'Element', message: str):
        if sender.get_id() in self.connections:
            print(f"[{self.name}] Received message from {sender.name}: '{message}'")
        else:
            print(f"[{self.name}] Cannot receive message. No active connection with {sender.name}")
