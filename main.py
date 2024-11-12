# test_hacking_proxy.py

from proto_element import Element
import uuid

# Initialize Elements
alice = Element("Alice")
bob = Element("Bob")        # Legitimate proxy
charlie = Element("Charlie")
hacker = Element("Hacker")   # Malicious actor attempting proxy hacks

# Step 1: Hacker Attempts to Reuse an Expired Proxy Key
print("\n--- Step 1: Hacker Attempts to Reuse an Expired Proxy Key ---")
# Alice initiates a legitimate connection to Charlie through Bob
alice.initiate_connection(charlie, proxy=bob)
charlie.approve_connection(alice)  # Approve the connection to expire the proxy key

# Hacker tries to use the same expired proxy key to connect Alice to Charlie again
print("\n[Hacker] Trying to reuse expired proxy key...")
hacker.initiate_connection(charlie, proxy=bob)  # Should be blocked due to expired key

# Expected Output:
# The proxy key should be expired, and Hacker’s attempt should be blocked.

# Step 2: Hacker Attempts Unauthorized Proxy Connection
print("\n--- Step 2: Hacker Attempts Unauthorized Proxy Connection ---")
# Hacker tries to connect Alice to Charlie as an unauthorized proxy
alice.initiate_connection(charlie, proxy=hacker)

# Expected Output:
# Charlie should block the connection attempt because Hacker is not a trusted proxy.

# Step 3: Hacker Generates Fake Proxy Key and Tries to Connect
print("\n--- Step 3: Hacker Generates Fake Proxy Key and Attempts Connection ---")
# Hacker attempts to directly interact with Alice to act as a fake proxy
# This involves creating a fake proxy key and attempting to trick Alice
fake_proxy_key = uuid.uuid4()  # A random UUID representing a fake key

# Hacker directly initiates a connection with Alice using a fake proxy key
fake_proxy_content = {
    'proxy-id': hacker.get_id(),
    'proxy-key': fake_proxy_key
}

# Alice should block this because there is no valid key from a trusted proxy
alice.receive_connection_request(hacker, uuid.uuid4(), proxy=fake_proxy_content)

# Expected Output:
# Alice should reject the connection request, as the fake proxy key doesn’t match any valid key.

# Step 4: Hacker Tries to Impersonate Bob as a Proxy
print("\n--- Step 4: Hacker Tries to Impersonate Bob as a Proxy ---")
# Hacker attempts to initiate a connection as if they were Bob
# By passing Bob's ID and trying to use a key as if Hacker were Bob
impersonation_proxy_content = {
    'proxy-id': bob.get_id(),  # Hacker impersonates Bob's ID
    'proxy-key': fake_proxy_key  # Random fake key
}

# Charlie should detect that the key does not match the real proxy key from Bob
charlie.receive_connection_request(hacker, uuid.uuid4(), proxy=impersonation_proxy_content)

# Expected Output:
# Charlie should block the request because the proxy key does not match any legitimate key from Bob.

# Step 5: Hacker Attempts to Forge Approval with a Fake Key
print("\n--- Step 5: Hacker Attempts to Forge Approval with a Fake Key ---")
# Hacker tries to finalize a connection with Charlie using a forged approval
fake_connection_key = uuid.uuid4()
charlie.receive_approval(hacker, fake_connection_key)

# Expected Output:
# Charlie should block the request, as the connection key does not match any pending request from Hacker.
