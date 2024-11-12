# test_main.py

from element import Element
import uuid

# Initialize Elements
alice = Element("Alice")
bob = Element("Bob")        # Bob will act as a legitimate proxy
charlie = Element("Charlie")
hacker = Element("Hacker")   # Hacker will attempt unauthorized proxy actions

# Step 1: Test Legitimate Proxy Request and Approval
print("\n--- Step 1: Legitimate Proxy Request and Approval ---")
alice.initiate_connection(charlie, proxy=bob)

# Expected Output:
# Alice sends a connection request to Charlie through Bob.
# Bob generates a valid proxy key and sends it to both Alice and Charlie.
# Charlie should receive the proxied connection request with verification.

charlie.approve_connection(alice)

# Expected Output:
# Charlie approves the connection request from Alice.
# Proxy key is expired after approval.
# Connection is established between Alice and Charlie.

# Step 2: Test Expired Proxy Key Usage
print("\n--- Step 2: Attempt Reuse of Expired Proxy Key ---")
# Alice attempts to initiate another connection to Charlie through the expired proxy key.
alice.initiate_connection(charlie, proxy=bob)

# Expected Output:
# The system should detect that the proxy key is expired, and Charlie should block the request.

# Step 3: Unauthorized Proxy Request Attempt by Hacker
print("\n--- Step 3: Unauthorized Proxy Request Attempt by Hacker ---")
# Alice attempts to connect to Charlie through Hacker as an unauthorized proxy
alice.initiate_connection(charlie, proxy=hacker)

# Expected Output:
# Hacker generates a proxy key, but Charlie does not recognize Hacker as a legitimate proxy and blocks the request.

# Step 4: Test Legitimate Proxy Request and Rejection
print("\n--- Step 4: Legitimate Proxy Request and Rejection ---")
# Alice initiates another connection request to Charlie through Bob
alice.initiate_connection(charlie, proxy=bob)
charlie.reject_connection(alice)

# Expected Output:
# Charlie receives the connection request from Alice through Bob.
# Charlie rejects the request, and the proxy key is expired immediately after rejection.

# Step 5: Direct Connection Request (Blocked Due to Settings)
print("\n--- Step 5: Direct Connection Request (Should be Blocked) ---")
# Alice attempts a direct connection to Charlie, but direct requests are not allowed by Charlie's settings
alice.initiate_connection(charlie)

# Expected Output:
# Charlie blocks the direct connection request due to `allow_direct_request` being False.

# Step 6: Canceling a Pending Connection Request
print("\n--- Step 6: Canceling a Pending Connection Request ---")
# Alice initiates a connection request to Bob
alice.initiate_connection(bob)
# Alice decides to cancel the connection request
alice.cancel_connection(bob)

# Expected Output:
# Alice successfully cancels the connection request to Bob before it is approved or rejected.

# Step 7: Sending and Receiving Messages in Established Connection
print("\n--- Step 7: Sending and Receiving Messages in Established Connection ---")
# Re-establish a legitimate connection between Alice and Charlie through Bob
alice.initiate_connection(charlie, proxy=bob)
charlie.approve_connection(alice)

# Expected Output:
# A connection is established between Alice and Charlie.

# Alice sends a message to Charlie
alice.send_message(charlie, "Hello, Charlie! Good to connect.")
# Charlie responds to Alice
charlie.send_message(alice, "Hello, Alice! Connection is working well.")

# Expected Output:
# Alice and Charlie should successfully send and receive messages through the established connection.

# Step 8: Terminating an Active Connection
print("\n--- Step 8: Terminating an Active Connection ---")
# Alice decides to terminate the connection with Charlie
alice.terminate_connection(charlie)

# Expected Output:
# The connection between Alice and Charlie is terminated, and any further messaging attempts should be blocked.

# Step 9: Attempt to Reuse a Canceled or Terminated Connection
print("\n--- Step 9: Attempt to Reuse a Canceled or Terminated Connection ---")
# Alice tries to send another message to Charlie after terminating the connection
alice.send_message(charlie, "Trying to reconnect message.")

# Expected Output:
# Since the connection was terminated, Alice should not be able to send messages to Charlie, and the system should block this action.

# Step 10: Attempt Unauthorized Message Without Established Connection
print("\n--- Step 10: Unauthorized Message Attempt ---")
# Hacker tries to send a message to Alice without any established connection
hacker.send_message(alice, "Hello, Alice! This is Hacker.")

# Expected Output:
# The system should block the message attempt from Hacker, as there is no active connection between Hacker and Alice.
