# main.py

from element import Element

# Create elements
alice = Element("Alice")
bob = Element("Bob")
charlie = Element("Charlie")

# Step 1: Alice initiates a connection request to Bob
print("\n--- Step 1: Alice initiates a connection request to Bob ---")
alice.initiate_connection(bob)

# Step 2: Bob approves Alice's connection request
print("\n--- Step 2: Bob approves Alice's connection request ---")
bob.approve_connection(alice)

# Step 3: Alice sends a message to Bob
print("\n--- Step 3: Alice sends a message to Bob ---")
alice.send_message(bob, "Hello, Bob! How are you?")

# Step 4: Bob responds to Alice
print("\n--- Step 4: Bob responds to Alice ---")
bob.send_message(alice, "I'm good, Alice! Thanks for asking.")

# Step 5: Alice initiates a connection request to Charlie
print("\n--- Step 5: Alice initiates a connection request to Charlie ---")
alice.initiate_connection(charlie)

# Step 6: Charlie approves Alice's connection request
print("\n--- Step 6: Charlie approves Alice's connection request ---")
charlie.approve_connection(alice)

# Step 7: Alice sends a message to Charlie
print("\n--- Step 7: Alice sends a message to Charlie ---")
alice.send_message(charlie, "Hi Charlie! Great to connect with you.")

# Step 8: Charlie responds to Alice
print("\n--- Step 8: Charlie responds to Alice ---")
charlie.send_message(alice, "Hi Alice! Nice to connect as well.")

# Step 9: Alice tries to send a message to Bob after terminating the connection
print("\n--- Step 9: Alice terminates the connection with Bob and tries to send a message ---")
alice.terminate_connection(bob)
alice.send_message(bob, "This message should not be sent.")
