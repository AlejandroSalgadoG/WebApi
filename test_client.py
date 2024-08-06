import grpc
from generated.test_pb2 import TestRequest
from generated.test_pb2_grpc import TestServiceStub

from config import HOST, PORT


def iter_test_request():
    for i in range(3):
        yield TestRequest(name="alejo", msg=f"hello {i}")


if __name__ == '__main__':
    with grpc.insecure_channel(f"{HOST}:{PORT}") as channel:
        client = TestServiceStub(channel)

        print("1. simple")
        print("2. respose stream")
        print("3. request stream")
        print("4. bidirectional")

        rpc = input("> ")

        if rpc == "1":
            request = TestRequest(name="alejo", msg="hello")
            reply = client.simpleRpc(request)
            print("simple rcp response:")
            print(reply)
        elif rpc == "2":
            request = TestRequest(name="alejo", msg="hello")
            for reply in client.responseStreamRpc(request):
                print("response stream rcp response:")
                print(reply)
        elif rpc == "3":
            multi_reply = client.requestStreamRpc(iter_test_request())
            print("request stream rpc response:")
            print(multi_reply)
        elif rpc == "4":
            responses = client.bidirectionalStreamRpc(iter_test_request())
            for response in responses:
                print("bidirectional stream rpc response:")
                print(response)
