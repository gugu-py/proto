import uuid
from typing import Optional, Dict

class ProxyKey:
    def __init__(self, handler_id: uuid.UUID, requester_id: uuid.UUID, receiver_id: uuid.UUID):
        self.handler_id = handler_id      # The proxy handler (the intermediary)
        self.requester_id = requester_id  # The initiator of the connection request
        self.receiver_id = receiver_id    # The intended recipient of the connection request
        self.key = uuid.uuid4()           # Unique proxy key for authentication
    
    def get_key(self) -> uuid.UUID:
        return self.key

    def is_valid_for(self, handler_id: uuid.UUID, requester_id: uuid.UUID, receiver_id: uuid.UUID) -> bool:
        """ Validate the ProxyKey against handler, requester, and receiver IDs """
        return (self.handler_id == handler_id and
                self.requester_id == requester_id and
                self.receiver_id == receiver_id)

class Element:
    def __init__(self, name: str):
        self.name = name
        self.id = uuid.uuid4()
        self.allow_direct_request: bool = False
        self.allow_indirect_request: bool = True
        self.allow_proxy_requests: bool = True  # Allow acting as a proxy
        self.connections: Dict[uuid.UUID, uuid.UUID] = {}  # Active connections with unique keys
        self.pending_received_requests: Dict[uuid.UUID, uuid.UUID] = {}  # Received connection requests
        self.pending_sent_requests: Dict[uuid.UUID, uuid.UUID] = {}  # Sent connection requests
        self.awaiting_approvals: Dict[uuid.UUID, uuid.UUID] = {}  # Approvals sent but not yet confirmed
        self.proxy_keys: Dict[tuple, ProxyKey] = {}  # Store ProxyKey objects for authentication

    def get_id(self) -> uuid.UUID:
        return self.id

    def initiate_connection(self, target: 'Element', proxy: Optional['Element'] = None):
        # Generate a unique key for this connection
        connection_key = uuid.uuid4()
        self.pending_sent_requests[target.get_id()] = connection_key
        
        if proxy:
            print(f"[{self.name}] Sent request to proxy {proxy.name} to connect with {target.name}")
            # Inform the proxy about the intent to connect through it
            proxy.handle_proxy_request(self, target)

            # Retrieve the ProxyKey for validation
            proxy_key = proxy.proxy_keys.get((self.get_id(), target.get_id()))
            if proxy_key and proxy_key.is_valid_for(proxy.get_id(), self.get_id(), target.get_id()):
                proxy_content = {
                    'proxy-id': proxy.get_id(),
                    'proxy-key': proxy_key.get_key()
                }
                target.receive_connection_request(self, connection_key, proxy=proxy_content)
        else:
            print(f"[{self.name}] Sent direct connection request to {target.name}")
            target.receive_connection_request(self, connection_key)

    def handle_proxy_request(self, requester: 'Element', receiver: 'Element'):
        if self.allow_proxy_requests:
            # Generate a ProxyKey instance for the sender-receiver pair
            proxy_key = ProxyKey(self.get_id(), requester.get_id(), receiver.get_id())
            # Store the ProxyKey using a consistent key format
            self.proxy_keys[(requester.get_id(), receiver.get_id())] = proxy_key
            print(f"[{self.name}] Generated proxy connection key for {requester.name} and {receiver.name}")
            # Send the proxy key details to both requester and receiver
            requester.receive_proxy_key(self, receiver, proxy_key)
            receiver.receive_proxy_key(self, requester, proxy_key)
        else:
            print(f"[{self.name}] Proxy requests are not allowed")

    def receive_proxy_key(self, proxy: 'Element', target: 'Element', proxy_key: ProxyKey):
        # Store the ProxyKey for the sender-target pair
        self.proxy_keys[(proxy.get_id(), target.get_id())] = proxy_key
        print(f"[{self.name}] Received proxy key from {proxy.name} for connecting to {target.name}")

    def receive_connection_request(self, requester: 'Element', connection_key: uuid.UUID, proxy: Optional[Dict[str, uuid.UUID]] = None):
        if proxy is None:
            # Direct connection request handling
            if self.allow_direct_request:
                self.pending_received_requests[requester.get_id()] = connection_key
                print(f"[{self.name}] Received direct connection request from {requester.name}")
            else:
                print(f"[{self.name}] Blocked direct connection request from {requester.name}")
        else:
            # Indirect (proxied) request handling
            proxy_key_object = self.proxy_keys.get((proxy['proxy-id'], requester.get_id()))
            if (self.allow_indirect_request and proxy_key_object and
                proxy_key_object.is_valid_for(proxy['proxy-id'], requester.get_id(), self.get_id()) and
                proxy_key_object.get_key() == proxy['proxy-key']):
                self.pending_received_requests[requester.get_id()] = connection_key
                print(f"[{self.name}] Received proxied connection request from {requester.name} through {proxy['proxy-id']}")
            else:
                print(f"[{self.name}] Blocked proxied request from {requester.name} through untrusted proxy")

    def approve_connection(self, requester: 'Element'):
        # Approve the connection if it exists in pending requests
        if requester.get_id() in self.pending_received_requests:
            connection_key = self.pending_received_requests.pop(requester.get_id())
            self.awaiting_approvals[requester.get_id()] = connection_key
            print(f"[{self.name}] Sent approval to {requester.name}")
            requester.receive_approval(self, connection_key)
        else:
            print(f"[{self.name}] No pending request from {requester.name}")

    def receive_approval(self, target: 'Element', connection_key: uuid.UUID):
        # Finalize connection upon receiving approval
        if target.get_id() in self.pending_sent_requests and self.pending_sent_requests[target.get_id()] == connection_key:
            self.awaiting_approvals[target.get_id()] = connection_key
            del self.pending_sent_requests[target.get_id()]
            self.finalize_connection(target)
        else:
            print(f"[{self.name}] Received invalid approval request from {target.name}")

    def finalize_connection(self, target: 'Element'):
        # Complete the connection if approval was received
        if target.get_id() in self.awaiting_approvals:
            connection_key = self.awaiting_approvals.pop(target.get_id())
            self.connections[target.get_id()] = connection_key
            print(f"[{self.name}] Sent finalized connection to {target.name}")
            target.recieve_finalize_connection(self, connection_key)
            print(f"[{self.name}] Connection with {target.name} established with key {connection_key}")
        else:
            print(f"[{self.name}] Invalid finalized connection to {target.name}")

    def recieve_finalize_connection(self, target: 'Element', connection_key: uuid.UUID):
        if target.get_id() in self.awaiting_approvals and self.awaiting_approvals[target.get_id()] == connection_key:
            self.connections[target.get_id()] = connection_key
            print(f"[{self.name}] Received finalized connection from {target.name}")
        else:
            print(f"[{self.name}] Received invalid finalized connection from {target.name}")
