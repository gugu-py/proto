import uuid

class Element:
    def __init__(self, name):
        self.name = name
        self.id = uuid.uuid4()
        self.connections = {}           # Stores active connections with unique keys
        self.pending_recieved_requests = {}       # Stores recieved connection requests awaiting approval
        self.pending_sent_requests = {}   # Stores sent connection requests awaiting approval
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
            # Send approval message back to the requester with the connection key
            print(f"[{self.name}] Sent approval to {requester.name}")
            requester.receive_approval(self, connection_key)
        else:
            print(f"[{self.name}] No pending request from {requester.name}")

    def receive_approval(self, target, connection_key):
        # Upon receiving approval, establish the connection
        if target.get_id() in self.pending_sent_requests and self.pending_sent_requests[target.get_id()]==connection_key:
            self.awaiting_approvals[target.get_id()] = connection_key
            self.finalize_connection(target)
        else:
            print(f"[{self.name}] Recieved invalid approval request from {target.name}")

    def finalize_connection(self, target):
        # Complete the connection only if approval was received
        if target.get_id() in self.awaiting_approvals:
            connection_key = self.awaiting_approvals.pop(target.get_id())
            # Establish mutual connection
            self.connections[target.get_id()] = connection_key
            target.connections[self.get_id()] = connection_key
            print(f"[{self.name}] Connection with {target.name} established with key {connection_key}")

    def reject_connection(self, requester):
        # Reject and remove a pending connection request
        if requester.get_id() in self.pending_recieved_requests:
            del self.pending_recieved_requests[requester.get_id()]
            print(f"[{self.name}] Rejected connection request from {requester.name}")
        else:
            print(f"[{self.name}] No pending request from {requester.name}")

    def terminate_connection(self, target):
        # Terminate an existing connection if it exists
        if target.get_id() in self.connections:
            del self.connections[target.get_id()]
            target.connections.pop(self.get_id(), None)  # Remove mutual connection
            print(f"[{self.name}] Terminated connection with {target.name}")
        else:
            print(f"[{self.name}] No active connection with {target.name}")
