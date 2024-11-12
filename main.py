# main.py

from element import Element
import uuid

# Create elements
alice = Element("Alice")
bob = Element("Bob")        # Bob will act as the legitimate proxy
charlie = Element("Charlie")
hacker = Element("Hacker")   # Hacker will attempt an unauthorized proxy
fake_proxy_key = uuid.uuid4() # A fake proxy key for the unauthorized attempt

# Step 1: Legitimate Proxy Request
print("\n--- Step 1: Legitimate Proxy Request ---")
# Alice initiates a request to connect to Charlie via Bob (legitimate proxy)
alice.initiate_connection(charlie, proxy=bob)

# Expected Output:
# Alice informs Bob that it wants to connect to Charlie through him.
# Bob generates a unique proxy key and shares it with both Alice and Charlie.
# Charlie receives a proxied connection request from Alice through Bob and processes it.

# Step 2: Bob Approves Proxy Request to Charlie on Alice's Behalf
print("\n--- Step 2: Bob Approves Proxy Request to Charlie on Alice's Behalf ---")
charlie.approve_connection(alice)

# Expected Output:
# Charlie approves the proxied connection request from Alice.
# A connection is established between Alice and Charlie, verified by the proxy key.

# Step 3: Unauthorized Proxy Request Attempt by Hacker
print("\n--- Step 3: Unauthorized Proxy Request Attempt by Hacker ---")
# Alice attempts to connect to Charlie through Hacker as a fake proxy
alice.initiate_connection(charlie, proxy=hacker)

# Expected Output:
# Alice informs Hacker that it wants to connect to Charlie through him.
# Hacker generates a fake proxy key that is not valid for Charlie.
# Charlie receives the proxied request but blocks it due to the invalid proxy key.

# Step 4: Charlie Approves and Establishes Connection with Alice via Legitimate Proxy (Bob)
print("\n--- Step 4: Finalize Legitimate Connection ---")
# Charlie, who received a valid proxied request from Bob on behalf of Alice, finalizes the connection
bob.handle_proxy_request(alice, charlie)
charlie.approve_connection(alice)

# Expected Output:
# Charlie receives and approves the request via the legitimate proxy, Bob, confirming a valid connection with Alice.
