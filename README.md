# Peer-to-peer chat

## Overview
Create a decentralized chat system with individual nodes (peers). Each peer discovers others in the network, retrieves chat message history from them, merges it with its own history, and then sends and receives new messages. Messages received are stored in the local message history, ensuring no message loss as long as at least one peer in the network retains the history.

The program should be demonstrated in `lab8a` and communicate with 3-4 other applications from classmates. Anything smaller will not be considered evaluable.

## Peer Communication
Peers use three types of communication:
- UDP: for peer discovery in the network
- TCP: for maintaining permanent connections with other peers (bidirectional communication)
- HTTP server running on the peer's localhost: implements a simple API for command-line communication (via `curl`) or serves as an API for a web backend displaying the chat in a browser (optional - bonus points)

### 1. UDP Discovery
After starting, a peer initiates periodic peer discovery using UDP. It broadcasts a UDP packet on port 9876 every five seconds and waits for responses. Communication is JSON-based, with each line representing a query or response. Lines end with either CR-LF or just LF.

Example:
```json
Q: {"command":"hello","peer_id":"molic-peer1"}
A: {"status":"ok","peer_id":"molic-peer1"}
A: {"status":"ok","peer_id":"molic-peer2"}
A: {"status":"ok","peer_id":"molic-peer3"}
```

### 2. TCP Protocol (Bidirectional Peer Communication)
Upon finding a new peer, a permanent TCP connection is established on port 9876. Communication follows a JSON-based protocol similar to UDP discovery. After a handshake, peers exchange their chat message history.

Example:
```json
Q: {"command":"hello","peer_id":"molic-peer1"}
A: {"status":"ok", "messages": {"1707243010934": {"peer_id":"molic-peer3", "message":"pokus"}, ...}}
```

Peers use this established TCP connection to send new messages to each other.

### 3. Web API
For message reading and writing, a backend implements an HTTP server listening on port 8000. The API includes:
- Reading messages: `GET /messages`
- Sending a message: `GET /send?message=...`

Example:
```bash
$ curl http://127.0.0.1:8000/messages
{"1707243010934":{"peer_id":"molic-peer3","message":"pokus"},"..."}
$ curl http://127.0.0.1:8000/send?message=blablabla
{"status":"ok"}
```

## Technical and Organizational Guidelines
- Run the application on a school VM or Raspberry PI connected to LAB 8a.
- Application runs on IP range 172.16.0.0/12.
- Each peer has a unique ID, either configured or based on the hostname.
- Timestamp (message ID) is a string of at least 13 digits representing milliseconds since 1970.
- Peer retains only the latest 100 messages to avoid overload.
- Use only technologies taught in class.

### System Daemon and Logging
- Application runs as a systemd service, not as root.
- Logs can be viewed using `journalctl -fu chat`.

### Demo Application and Testing
Three instances run in the network on VMs:
- `ssh -p 20110 jouda@dev.spsejecna.net` # molic-peer1
- `ssh -p 20185 jouda@dev.spsejecna.net` # molic-peer2
- `ssh -p 20393 jouda@dev.spsejecna.net` # molic-peer3

Log in using the password 'jooouda' and test the application with `curl` or Telnet.

## Help
- Follow the suggested workflow.
- Test with classmates' programs, not in isolation.
- Use PuTTY or Telnet, not self-programmed clients.
- Stick to allowed commands and exact syntax.
- Implement and test timeouts.
- Collaborate with classmates but avoid sharing code.
