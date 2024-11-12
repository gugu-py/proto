import uuid
from typing import Optional, Dict

class Element:
    def __init__(self, name: str):
        self.name = name
        self.id = uuid.uuid4()
        self.allow_direct_request: bool = False
        self.allow_indirect_request: bool = True
        self.allow_proxy_requests: bool = True  # Allow acting as a proxy
        self.connections: Dict[uuid.UUID, uuid.UUID] = {}  # Active connections with unique keys
        self.pending_recieved_requests: Dict[uuid.UUID, uuid.UUID] = {}  # Received connection requests
        self.pending_sent_requests: Dict[uuid.UUID, uuid.UUID] = {}  # Sent connection requests
        self.awaiting_approvals: Dict[uuid.UUID, uuid.UUID] = {}  # Approvals sent but not yet confirmed
        self.proxy_keys: Dict[tuple, uuid.UUID] = {}  # Store proxy connection keys for authentication

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

            if target.get_id() in self.proxy_keys:
                proxy_content = {
                    'proxy-name': proxy.get_id(),
                    'proxy-key': self.proxy_keys[target.get_id()],
                }
                target.receive_connection_request(self, connection_key, proxy=proxy_content)
        else:
            print(f"[{self.name}] Sent direct connection request to {target.name}")
            target.receive_connection_request(self, connection_key)

    def handle_proxy_request(self, sender: 'Element', receiver: 'Element'):
        if self.allow_proxy_requests:
            # Generate a unique proxy connection key
            proxy_connection_key = uuid.uuid4()
            # Store the key associated with both sender and receiver for validation
            self.proxy_keys[(sender.get_id(), receiver.get_id())] = proxy_connection_key
            print(f"[{self.name}] Generated proxy connection key for {sender.name} and {receiver.name}")
            # Send the proxy connection key to both the sender and the receiver
            sender.receive_proxy_key(self, receiver, proxy_connection_key)
            receiver.receive_proxy_key(self, sender, proxy_connection_key)
        else:
            print(f"[{self.name}] Proxy requests are not allowed")

    def receive_proxy_key(self, proxy: 'Element', target: 'Element', proxy_key: uuid.UUID):
        # Store the proxy key for the target
        self.proxy_keys[target.get_id()] = proxy_key
        print(f"[{self.name}] Received proxy key from {proxy.name} for connecting to {target.name}")

    def receive_connection_request(self, requester: 'Element', connection_key: uuid.UUID, proxy: Optional[Dict[str, str]] = None):
        if proxy is None:
            # Direct connection request handling
            if self.allow_direct_request:
                self.pending_recieved_requests[requester.get_id()] = connection_key
                print(f"[{self.name}] Received direct connection request from {requester.name}")
            else:
                print(f"[{self.name}] Blocked direct connection request from {requester.name}")
        else:
            # Indirect (proxied) request handling
            proxy_key = self.proxy_keys.get(requester.get_id())
            if self.allow_indirect_request and proxy and proxy_key == proxy['proxy-key']:
                self.pending_recieved_requests[requester.get_id()] = connection_key
                print(f"[{self.name}] Received proxied connection request from {requester.name} through {proxy['proxy-name']}")
            else:
                print(f"[{self.name}] Blocked proxied request from {requester.name} through untrusted proxy {proxy['proxy-name']}")

    def approve_connection(self, requester: 'Element'):
        # Approve the connection if it exists in pending requests
        if requester.get_id() in self.pending_recieved_requests:
            connection_key = self.pending_recieved_requests.pop(requester.get_id())
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

    def reject_connection(self, requester: 'Element'):
        # Reject and remove a pending connection request
        if requester.get_id() in self.pending_recieved_requests:
            del self.pending_recieved_requests[requester.get_id()]
            print(f"[{self.name}] Rejected connection request from {requester.name}")
        else:
            print(f"[{self.name}] No pending request from {requester.name}")

    def cancel_connection(self, requester: 'Element'):
        if requester.get_id() in self.pending_sent_requests:
            del self.pending_sent_requests[requester.get_id()]
            print(f"[{self.name}] Canceled connection request to {requester.name}")
        else:
            print(f"[{self.name}] No sent request to {requester.name}")

    def terminate_connection(self, target: 'Element'):
        # Terminate an existing connection if it exists
        if target.get_id() in self.connections:
            target.recieve_terminate(self, self.connections[target.get_id()])
            del self.connections[target.get_id()]
            print(f"[{self.name}] Terminated connection with {target.name}")
        else:
            print(f"[{self.name}] No active connection with {target.name}")

    def recieve_terminate(self, target: 'Element', connection_key: uuid.UUID):
        if target.get_id() in self.connections and self.connections[target.get_id()] == connection_key:
            del self.connections[target.get_id()]
            print(f"[{self.name}] Received terminated connection with {target.name}")
        else:
            print(f"[{self.name}] Received invalid terminated connection with {target.name}")
