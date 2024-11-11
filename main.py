# main.py

from element import Element

# Create elements
alice = Element("Alice")
bob = Element("Bob")
charlie = Element("Charlie")

print("\n--- Step 1: Alice initiates a connection request to Bob ---")
alice.initiate_connection(bob)

print("\n--- Step 2: Bob approves Alice's connection request ---")
bob.approve_connection(alice)

print("\n--- Step 3: Alice initiates a connection request to Charlie ---")
alice.initiate_connection(charlie)

print("\n--- Step 4: Charlie rejects Alice's connection request ---")
charlie.reject_connection(alice)

print("\n--- Step 5: Alice re-initiates a connection request to Charlie ---")
alice.initiate_connection(charlie)

print("\n--- Step 6: Charlie approves Alice's connection request ---")
charlie.approve_connection(alice)

print("\n--- Step 7: Alice decides to terminate the connection with Bob ---")
alice.terminate_connection(bob)
