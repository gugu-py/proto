# element.py

import uuid

class Element:
    def __init__(self, name):
        self.name = name
        self.id = uuid.uuid4()
        self.connections = {}            # Stores active connections with unique keys
        self.pending_recieved_requests = {}  # Stores received connection requests awaiting approval
        self.pending_sent_requests = {}  # Stores sent connection requests awaiting approval
        self.awaiting_approvals = {}     # Tracks approvals sent but not yet connected

    def get_id(self):
        return self.id

    def initiate_connection(self, target):
        # Generate a unique key for this connection
        connection_key = uuid.uuid4()
        # Send a connection request to the target
        print(f"[{self.name}] Sent connection request to {target.name}")
        self.pending_sent_requests[target.get_id()] = connection_key
        target.receive_connection_request(self, connection_key)

    def receive_connection_request(self, requester, connection_key):
        # Store the incoming request as pending until approved
        self.pending_recieved_requests[requester.get_id()] = connection_key
        print(f"[{self.name}] Received connection request from {requester.name}")

    def approve_connection(self, requester):
        # Approve the connection if it exists in pending requests
        if requester.get_id() in self.pending_recieved_requests:
            connection_key = self.pending_recieved_requests.pop(requester.get_id())
            self.awaiting_approvals[requester.get_id()]=connection_key
            # Send approval message back to the requester with the connection key
            print(f"[{self.name}] Sent approval to {requester.name}")
            requester.receive_approval(self, connection_key)
        else:
            print(f"[{self.name}] No pending request from {requester.name}")

    def receive_approval(self, target, connection_key):
        # Upon receiving approval, establish the connection
        if target.get_id() in self.pending_sent_requests and self.pending_sent_requests[target.get_id()] == connection_key:
            self.awaiting_approvals[target.get_id()] = connection_key
            del self.pending_sent_requests[target.get_id()]
            self.finalize_connection(target)
        else:
            print(f"[{self.name}] Received invalid approval request from {target.name}")

    def finalize_connection(self, target):
        # Complete the connection only if approval was received
        if target.get_id() in self.awaiting_approvals:
            connection_key = self.awaiting_approvals.pop(target.get_id())
            # Establish mutual connection
            self.connections[target.get_id()] = connection_key
            print(f"[{self.name}] sent finalized connection to {target.name}")
            target.recieve_finalize_connection(self,connection_key)
            print(f"[{self.name}] Connection with {target.name} established with key {connection_key}")
        else:
            print(f"[{self.name}] invalid finalized connection to {target.name}")

    def recieve_finalize_connection(self, target, connection_key):
        if target.get_id() in self.awaiting_approvals and self.awaiting_approvals[target.get_id()]==connection_key:
            self.connections[target.get_id()] = connection_key
            print(f"[{self.name}] recieved finalized connection from {target.name}")
        else:
            print(f"[{self.name}] recieved invalid finalized connection from {target.name}")

    def reject_connection(self, requester):
        # Reject and remove a pending connection request
        if requester.get_id() in self.pending_recieved_requests:
            del self.pending_recieved_requests[requester.get_id()]
            print(f"[{self.name}] Rejected connection request from {requester.name}")
        else:
            print(f"[{self.name}] No pending request from {requester.name}")

    def cancel_connection(self, requester):
        if requester.get_id() in self.pending_sent_requests:
            del self.pending_sent_requests[requester.get_id()]
            print(f"[{self.name}] Canceled connection request to {requester.name}")
        else:
            print(f"[{self.name}] No sent request to {requester.name}")

    def terminate_connection(self, target):
        # Terminate an existing connection if it exists
        if target.get_id() in self.connections:
            target.recieve_terminate(self, self.connections[target.get_id()])
            del self.connections[target.get_id()]
            print(f"[{self.name}] Terminated connection with {target.name}")
        else:
            print(f"[{self.name}] No active connection with {target.name}")

    def recieve_terminate(self, target, connection_key):
        if target.get_id() in self.connections and self.connections[target.get_id()]==connection_key:
            del self.connections[target.get_id()]
            print(f"[{self.name}] Recieved terminated connection with {target.name}")
        else:
            print(f"[{self.name}] Recieved invalid terminated connection with {target.name}")
            
    # New message functions
    def send_message(self, target, message):
        # Send a message to a connected target
        if target.get_id() in self.connections:
            print(f"[{self.name}] Sent message to {target.name}: '{message}'")
            target.receive_message(self, message)
        else:
            print(f"[{self.name}] Cannot send message. No active connection with {target.name}")

    def receive_message(self, sender, message):
        # Receive a message from a connected sender
        if sender.get_id() in self.connections:
            print(f"[{self.name}] Received message from {sender.name}: '{message}'")
        else:
            print(f"[{self.name}] Cannot receive message. No active connection with {sender.name}")
