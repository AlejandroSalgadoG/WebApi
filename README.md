# Python gRPC Demo

A gRPC (Google Remote Procedure Call) implementation in Python, showcasing all four types of RPC communication patterns.

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#️-technology-stack)
- [Prerequisites](#-prerequisites)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [RPC Methods Explained](#-rpc-methods-explained)
- [Usage Examples](#-usage-examples)
- [Protocol Buffers](#-protocol-buffers)
- [Code Generation](#-code-generation)
- [Configuration](#️-configuration)
- [Troubleshooting](#-troubleshooting)
- [Learning Resources](#-learning-resources)

## 🎯 Overview

gRPC is a high-performance, open-source RPC framework developed by Google. It uses Protocol Buffers (protobuf) as its interface definition language and provides features like authentication, load balancing, and more.

This project demonstrates:
- **Simple/Unary RPC**: Single request → single response
- **Server Streaming RPC**: Single request → multiple responses (stream)
- **Client Streaming RPC**: Multiple requests (stream) → single response
- **Bidirectional Streaming RPC**: Multiple requests ↔ multiple responses (both streams)

## ✨ Features

- 🔄 **All 4 RPC Communication Patterns** - Complete implementation of every gRPC pattern
- 📡 **Server & Client Implementation** - Working examples of both sides
- 📝 **Protocol Buffers Definition** - Clear `.proto` file with detailed comments
- 🎮 **Interactive Client** - Menu-driven client for testing all RPC methods
- 🧩 **Auto-generated Code** - Python code generated from protobuf definitions
- 🔧 **Easy Configuration** - Simple host/port configuration
- 📚 **Educational Comments** - Well-documented code for learning

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **RPC Framework** | gRPC 1.65.4+ |
| **Serialization** | Protocol Buffers (proto3) |
| **Language** | Python 3.11+ |
| **Concurrency** | ThreadPoolExecutor |
| **Code Generation** | grpcio-tools |

## 📋 Prerequisites

- **Python 3.11+** (check `.python-version`)
- **pip** (Python package manager)

### Required Python Packages

```bash
pip install grpcio grpcio-tools
```

Or create a `requirements.txt`:
```txt
grpcio>=1.65.4
grpcio-tools>=1.65.4
```

## 📁 Project Structure

```
WebApi/
├── protos/
│   └── test.proto              # Protocol Buffer definitions
│
├── generated/                  # Auto-generated code (do not edit manually)
│   ├── __init__.py
│   ├── test_pb2.py            # Message classes
│   └── test_pb2_grpc.py       # Service classes
│
├── test_server.py             # gRPC server implementation
├── test_client.py             # gRPC client implementation
├── config.py                  # Configuration (host, port)
├── .python-version            # Python version specification
├── .gitignore                 # Git ignore patterns
└── README.md                  # This file
```

### File Descriptions

#### `protos/test.proto`
Protocol Buffer definition file that defines:
- Service methods (RPCs)
- Message types (request/response structures)
- Field types and numbers

#### `test_server.py`
Server implementation that:
- Defines the `TestService` class
- Implements all 4 RPC methods
- Starts the gRPC server
- Listens on configured host:port

#### `test_client.py`
Client implementation that:
- Connects to the gRPC server
- Provides interactive menu
- Demonstrates calling each RPC method
- Shows request/response handling

#### `generated/`
Auto-generated Python code from `.proto` file:
- `test_pb2.py` - Message serialization/deserialization
- `test_pb2_grpc.py` - Service stubs and servicers

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd WebApi
```

### 2. Install Dependencies

```bash
pip install grpcio grpcio-tools
```

### 3. Generate gRPC Code (if needed)

```bash
python -m grpc_tools.protoc \
  -I protos \
  --python_out=./generated \
  --grpc_python_out=./generated \
  protos/test.proto
```

### 4. Start the Server

Open a terminal and run:

```bash
python test_server.py
```

You should see:
```
server started
```

The server is now listening on `localhost:50051`

### 5. Run the Client

Open another terminal and run:

```bash
python test_client.py
```

You'll see an interactive menu:
```
1. simple
2. respose stream
3. request stream
4. bidirectional
>
```

### 6. Test Different RPC Methods

Type `1`, `2`, `3`, or `4` and press Enter to test different RPC patterns.

## 🔍 RPC Methods Explained

### 1. Simple RPC (Unary)

**Pattern**: Client sends one request → Server returns one response

**Use Case**: Standard request-response, like REST API calls

**Example**:
```python
# Client sends
TestRequest(name="alejo", msg="hello")

# Server responds
TestReply(msg="alejo hi")
```

**When to use**:
- Getting user profile
- Fetching single record
- Simple operations

---

### 2. Server Streaming RPC

**Pattern**: Client sends one request → Server returns a stream of responses

**Use Case**: Server needs to send multiple items in response

**Example**:
```python
# Client sends once
TestRequest(name="alejo", msg="hello")

# Server streams multiple responses
TestReply(msg="alejo hi 1")
TestReply(msg="alejo hi 2")
TestReply(msg="alejo hi 3")
```

**When to use**:
- Fetching list of items
- Downloading files in chunks
- Real-time updates/notifications
- Streaming logs

---

### 3. Client Streaming RPC

**Pattern**: Client sends a stream of requests → Server returns one response

**Use Case**: Client needs to send large amount of data

**Example**:
```python
# Client streams multiple requests
TestRequest(name="alejo", msg="hello 0")
TestRequest(name="alejo", msg="hello 1")
TestRequest(name="alejo", msg="hello 2")

# Server responds once
TestMultiReply(msg="sent 3 requests", request=[...])
```

**When to use**:
- Uploading files in chunks
- Batch data import
- Sensor data collection
- Logging/metrics aggregation

---

### 4. Bidirectional Streaming RPC

**Pattern**: Client and server both send streams of messages

**Use Case**: Both sides need continuous two-way communication

**Example**:
```python
# Client streams
TestRequest(name="alejo", msg="hello 0")

# Server streams back immediately
TestReply(msg="alejo hello 0 - hi")

# Client streams again
TestRequest(name="alejo", msg="hello 1")

# Server streams back again
TestReply(msg="alejo hello 1 - hi")
# ... continues ...
```

**When to use**:
- Chat applications
- Real-time collaboration
- Video/audio streaming
- Online gaming
- Live dashboards

## 💡 Usage Examples

### Example 1: Simple RPC

**Terminal 1 (Server)**:
```bash
$ python test_server.py
server started
simple rcp request:
name: "alejo"
msg: "hello"
```

**Terminal 2 (Client)**:
```bash
$ python test_client.py
1. simple
2. respose stream
3. request stream
4. bidirectional
> 1
simple rcp response:
msg: "alejo hi"
```

---

### Example 2: Server Stream RPC

**Terminal 1 (Server)**:
```bash
response stream rcp request:
name: "alejo"
msg: "hello"
```

**Terminal 2 (Client)**:
```bash
> 2
response stream rcp response:
msg: "alejo hi 1"

response stream rcp response:
msg: "alejo hi 2"

response stream rcp response:
msg: "alejo hi 3"
```

---

### Example 3: Client Stream RPC

**Terminal 1 (Server)**:
```bash
request stream rcp request:
name: "alejo"
msg: "hello 0"

request stream rcp request:
name: "alejo"
msg: "hello 1"

request stream rcp request:
name: "alejo"
msg: "hello 2"
```

**Terminal 2 (Client)**:
```bash
> 3
request stream rpc response:
msg: "sent 3 requests"
request {
  name: "alejo"
  msg: "hello 0"
}
request {
  name: "alejo"
  msg: "hello 1"
}
request {
  name: "alejo"
  msg: "hello 2"
}
```

---

### Example 4: Bidirectional Stream RPC

**Terminal 1 (Server)**:
```bash
bidirectional stream rcp request:
name: "alejo"
msg: "hello 0"

bidirectional stream rcp request:
name: "alejo"
msg: "hello 1"

bidirectional stream rcp request:
name: "alejo"
msg: "hello 2"
```

**Terminal 2 (Client)**:
```bash
> 4
bidirectional stream rpc response:
msg: "alejo hello 0 - hi"

bidirectional stream rpc response:
msg: "alejo hello 1 - hi"

bidirectional stream rpc response:
msg: "alejo hello 2 - hi"
```

## 📦 Protocol Buffers

### Message Definitions

#### TestRequest
```protobuf
message TestRequest {
  string name = 1;  // Field number 1
  string msg = 2;   // Field number 2
}
```

#### TestReply
```protobuf
message TestReply {
  string msg = 1;
}
```

#### TestMultiReply
```protobuf
message TestMultiReply {
  string msg = 1;
  repeated TestRequest request = 2;  // Array of TestRequest
}
```

### Service Definition

```protobuf
service TestService {
  rpc simpleRpc(TestRequest) returns (TestReply) {}
  rpc responseStreamRpc(TestRequest) returns (stream TestReply) {}
  rpc requestStreamRpc(stream TestRequest) returns (TestMultiReply) {}
  rpc bidirectionalStreamRpc(stream TestRequest) returns (stream TestReply) {}
}
```

### Proto3 Syntax Features

- **Field Numbers**: Unique identifiers for fields (1, 2, etc.)
- **Types**: `string`, `int32`, `int64`, `bool`, `bytes`, etc.
- **repeated**: Indicates array/list
- **stream**: Indicates streaming data

## 🔨 Code Generation

### Generate Python Code from Proto

```bash
python -m grpc_tools.protoc \
  -I protos \
  --python_out=./generated \
  --grpc_python_out=./generated \
  protos/test.proto
```

**Flags explained**:
- `-I protos` - Input directory containing `.proto` files
- `--python_out=./generated` - Output directory for message classes
- `--grpc_python_out=./generated` - Output directory for service classes
- `protos/test.proto` - The proto file to compile

### Generated Files

1. **test_pb2.py** - Contains:
   - `TestRequest` class
   - `TestReply` class
   - `TestMultiReply` class
   - Serialization/deserialization methods

2. **test_pb2_grpc.py** - Contains:
   - `TestServiceStub` - Client stub
   - `TestServiceServicer` - Server interface
   - `add_TestServiceServicer_to_server()` - Server registration

**⚠️ Do not edit generated files manually! They will be overwritten.**

## ⚙️ Configuration

### config.py

```python
PORT = 50051
HOST = "localhost"
```

**Customization**:

To change server address:
```python
PORT = 8080
HOST = "0.0.0.0"  # Listen on all interfaces
```

To use in production:
```python
PORT = 443
HOST = "api.yourdomain.com"
```

### Server Configuration

In `test_server.py`, adjust thread pool size:
```python
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
```

Increase `max_workers` for higher concurrency.

## 🐛 Troubleshooting

### Issue: "Address already in use"

**Problem**: Port 50051 is already being used

**Solution**:
```bash
# Find process using the port
lsof -i :50051

# Kill the process
kill -9 <PID>

# Or change PORT in config.py
```

---

### Issue: "Module not found: generated.test_pb2"

**Problem**: Generated code doesn't exist or Python can't find it

**Solution**:
```bash
# Regenerate the code
python -m grpc_tools.protoc \
  -I protos \
  --python_out=./generated \
  --grpc_python_out=./generated \
  protos/test.proto

# Ensure __init__.py exists
touch generated/__init__.py
```

---

### Issue: "grpc module not found"

**Problem**: gRPC not installed

**Solution**:
```bash
pip install grpcio grpcio-tools
```

---

### Issue: "Connection refused"

**Problem**: Server is not running or wrong host/port

**Solution**:
1. Verify server is running: `python test_server.py`
2. Check config.py matches on both server and client
3. Check firewall settings

---

### Issue: "Method not implemented"

**Problem**: Server method not properly implemented

**Solution**:
Ensure `TestService` class implements all methods from `TestServiceServicer`

---

### Issue: Generated code version mismatch

**Problem**: Warning about grpc version mismatch

**Solution**:
```bash
# Upgrade grpc
pip install --upgrade grpcio grpcio-tools

# Or regenerate code with current version
python -m grpc_tools.protoc -I protos --python_out=./generated --grpc_python_out=./generated protos/test.proto
```

## 📚 Learning Resources

### Official Documentation
- [gRPC Official Website](https://grpc.io/)
- [gRPC Python Documentation](https://grpc.io/docs/languages/python/)
- [Protocol Buffers](https://protobuf.dev/)
- [Proto3 Language Guide](https://protobuf.dev/programming-guides/proto3/)

### Tutorials
- [gRPC Python Quick Start](https://grpc.io/docs/languages/python/quickstart/)
- [gRPC Basics Tutorial](https://grpc.io/docs/languages/python/basics/)
- [Protocol Buffers Tutorial](https://protobuf.dev/getting-started/pythontutorial/)

### Concepts
- [gRPC Core Concepts](https://grpc.io/docs/what-is-grpc/core-concepts/)
- [Service Types](https://grpc.io/docs/what-is-grpc/core-concepts/#service-definition)
- [Streaming RPCs](https://grpc.io/docs/what-is-grpc/core-concepts/#server-streaming-rpc)

### Comparison
- **gRPC vs REST**: gRPC is faster, uses binary protocol, supports streaming
- **gRPC vs GraphQL**: gRPC is more performant, GraphQL is more flexible for queries
- **gRPC vs WebSockets**: gRPC has better tooling, typed contracts, and multiplexing

## 🎓 Understanding the Code

### Server Side

```python
class TestService(TestServiceServicer):
    def simpleRpc(self, request, context):
        # request: TestRequest object
        # context: gRPC context (metadata, status, etc.)
        return TestReply(msg=f"{request.name} hi")
```

**Key points**:
- Inherit from `TestServiceServicer`
- Implement each RPC method
- Use `yield` for streaming responses
- Use `request_iterator` for streaming requests

### Client Side

```python
with grpc.insecure_channel(f"{HOST}:{PORT}") as channel:
    client = TestServiceStub(channel)
    reply = client.simpleRpc(TestRequest(name="alejo", msg="hello"))
```

**Key points**:
- Create channel with `grpc.insecure_channel()`
- Create stub from channel
- Call RPC methods directly on stub
- Use `for` loop to iterate streaming responses

## 🔐 Production Considerations

This demo uses **insecure channels** for simplicity. In production:

### Use Secure Channels (TLS/SSL)

```python
# Server
credentials = grpc.ssl_server_credentials(...)
server.add_secure_port(f"{HOST}:{PORT}", credentials)

# Client
credentials = grpc.ssl_channel_credentials(...)
channel = grpc.secure_channel(f"{HOST}:{PORT}", credentials)
```

### Add Authentication

```python
# Add metadata/tokens
metadata = [('authorization', 'Bearer YOUR_TOKEN')]
client.simpleRpc(request, metadata=metadata)
```

### Error Handling

```python
try:
    response = client.simpleRpc(request)
except grpc.RpcError as e:
    print(f"Error: {e.code()}, {e.details()}")
```

### Timeouts

```python
response = client.simpleRpc(request, timeout=10)
```
