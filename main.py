# main.py

from element import Element
import uuid

# Create elements
alice = Element("Alice")
bob = Element("Bob")
attacker = Element("Attacker")

# Test 1: Legitimate Connection and Message Exchange
print("\n--- Test 1: Legitimate Connection and Message Exchange ---")
alice.initiate_connection(bob)
bob.approve_connection(alice)
alice.send_message(bob, "Hello, Bob!")

# Expected:
# Alice and Bob establish a legitimate connection.
# Messages are successfully exchanged.

# Test 2: Attacker Attempts Unauthorized Message Exchange
print("\n--- Test 2: Attacker Attempts Unauthorized Message Exchange ---")
attacker.send_message(alice, "Hi Alice! This is Attacker.")

# Expected:
# [Attacker] Cannot send message. No active connection with Alice

# Test 3: Attacker Sends Invalid Approval to Establish Unauthorized Connection
print("\n--- Test 3: Attacker Sends Invalid Approval to Alice ---")
alice.receive_approval(attacker, uuid.uuid4())

# Expected:
# [Alice] Received invalid approval request from Attacker

# Test 4: Attacker Attempts to Send Finalized Connection to Alice Without Approval
print("\n--- Test 4: Attacker Attempts Unauthorized Finalized Connection ---")
alice.recieve_finalize_connection(attacker, uuid.uuid4())

# Expected:
# [Alice] received invalid finalized connection from Attacker

# Test 5: Attacker Attempts to Terminate Connection Between Alice and Bob
print("\n--- Test 5: Attacker Attempts Unauthorized Termination ---")
attacker.terminate_connection(bob)

# Expected:
# [Attacker] No active connection with Bob

# Test 6: Legitimate Connection Cancellation
print("\n--- Test 6: Alice Cancels Connection Request to Bob Before Approval ---")
alice.initiate_connection(bob)
alice.cancel_connection(bob)

# Expected:
# [Alice] Canceled connection request to Bob
# [Bob] should have no record of Alice's connection request after this

# Test 7: Attacker Mimics Termination Request from Alice
print("\n--- Test 7: Attacker Mimics Termination Request from Alice ---")
bob.recieve_terminate(alice, uuid.uuid4())

# Expected:
# [Bob] Received invalid terminated connection with Alice

# Test 8: Attacker Mimics Finalized Connection to Alice After Legitimate Connection is Established with Bob
print("\n--- Test 8: Attacker Mimics Finalized Connection After Alice-Bob Connection ---")
alice.initiate_connection(bob)
bob.approve_connection(alice)
attacker.recieve_finalize_connection(alice, uuid.uuid4())

# Expected:
# [Attacker] Received invalid finalized connection from Alice

# Test 9: Unauthorized Connection Key Manipulation Attempt
print("\n--- Test 9: Unauthorized Connection Key Manipulation Attempt ---")
alice.initiate_connection(bob)
fake_key = uuid.uuid4()
alice.awaiting_approvals[bob.get_id()] = fake_key
bob.approve_connection(alice)

# Expected:
# Bob’s approval should not finalize the connection with Alice if the key is manipulated.
