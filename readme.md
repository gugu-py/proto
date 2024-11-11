# Decentralized Interaction Framework

## Project Overview

This project is a **Decentralized Interaction Framework** for creating autonomous, consent-based connections and message exchanges between independent entities, called "Elements." Each `Element` manages its own connection requests, approvals, message exchanges, and terminations, ensuring a fully decentralized structure with no centralized connection manager.

The framework enables secure, private communication by allowing Elements to control which connections are approved and enforce termination rules, supporting a peer-to-peer communication structure ideal for decentralized applications (dApps).

## Key Features

1. **Decentralized Connection Management**: Each `Element` independently handles its own connection requests and approvals, with no need for a central manager.
2. **Consent-Based Connections**: Both parties must approve a connection request for a connection to be established. By default, all requests are rejected until explicitly approved.
3. **Custom Message Exchange**: Connected Elements can send and receive custom messages. Unconnected or terminated connections prevent message exchanges, maintaining privacy and security.
4. **Secure Termination**: Either party in a connection can terminate the link, ensuring control over active connections.

## Code Structure

```plaintext
decentralized_framework/
├── element.py            # Core Element class handling connections and messaging
├── main.py               # Example script to demonstrate functionality
└── README.md             # Project overview and usage guide
```

### Key Classes

- **Element**: The main entity in the framework, capable of initiating and approving connection requests, exchanging messages with connected Elements, and managing termination of connections.

## Setup

### Prerequisites

- **Python 3.x**

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd decentralized_framework
   ```

2. Run the project:
   ```bash
   python main.py
   ```

## Usage

### 1. Creating Elements
Each `Element` represents an independent entity that can interact with others. Example:
```python
alice = Element("Alice")
bob = Element("Bob")
charlie = Element("Charlie")
```

### 2. Connection Workflow

1. **Initiate a Connection Request**:
   ```python
   alice.initiate_connection(bob)
   ```

2. **Approve or Reject a Connection Request**:
   ```python
   bob.approve_connection(alice)  # Approves the request from Alice
   charlie.reject_connection(alice)  # Rejects the request from Alice
   ```

3. **Terminate a Connection**:
   ```python
   alice.terminate_connection(bob)
   ```

### 3. Message Exchange

- **Send a Message**:
   ```python
   alice.send_message(bob, "Hello, Bob! How are you?")
   ```

- **Receive a Message**: The `receive_message` method in each `Element` class automatically displays incoming messages from connected Elements.

### Example Workflow

Here’s a sample interaction sequence found in `main.py`:

1. **Alice initiates a connection to Bob.**
2. **Bob approves Alice's connection request.**
3. **Alice and Bob exchange messages.**
4. **Alice initiates a connection request to Charlie.**
5. **Charlie rejects Alice's initial request, but later accepts a new request.**
6. **Alice and Charlie exchange messages.**
7. **Alice terminates her connection with Bob and can no longer send messages to him.**

## Expected Output

```plaintext
--- Step 1: Alice initiates a connection request to Bob ---
[Alice] Sent connection request to Bob
[Bob] Received connection request from Alice

--- Step 2: Bob approves Alice's connection request ---
[Bob] Sent approval to Alice
[Alice] Connection with Bob established with key <unique_key>

--- Step 3: Alice sends a message to Bob ---
[Alice] Sent message to Bob: 'Hello, Bob! How are you?'
[Bob] Received message from Alice: 'Hello, Bob! How are you?'

--- Step 4: Bob responds to Alice ---
[Bob] Sent message to Alice: 'I'm good, Alice! Thanks for asking.'
[Alice] Received message from Bob: 'I'm good, Alice! Thanks for asking.'

--- Step 5: Alice initiates a connection request to Charlie ---
[Alice] Sent connection request to Charlie
[Charlie] Received connection request from Alice

--- Step 6: Charlie approves Alice's connection request ---
[Charlie] Sent approval to Alice
[Alice] Connection with Charlie established with key <unique_key>

--- Step 7: Alice sends a message to Charlie ---
[Alice] Sent message to Charlie: 'Hi Charlie! Great to connect with you.'
[Charlie] Received message from Alice: 'Hi Charlie! Great to connect with you.'

--- Step 8: Charlie responds to Alice ---
[Charlie] Sent message to Alice: 'Hi Alice! Nice to connect as well.'
[Alice] Received message from Charlie: 'Hi Alice! Nice to connect as well.'

--- Step 9: Alice terminates the connection with Bob and tries to send a message ---
[Alice] Terminated connection with Bob
[Alice] Cannot send message. No active connection with Bob
```

## Future Enhancements

1. **Enhanced Security**: Add encryption for message exchanges.
2. **Additional Protocols**: Implement protocols for group messaging or multi-party connections.
3. **Error Handling**: Add more robust error handling for network issues or failed connection attempts.

## Summary

The **Decentralized Interaction Framework** is designed for secure, consent-based peer-to-peer connections without relying on a centralized manager. The `Element` class manages requests, approvals, messaging, and terminations autonomously, supporting flexible decentralized applications with privacy and security in mind. This project serves as a foundation for building more complex decentralized communication systems.

