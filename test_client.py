import grpc
from generated.test_pb2_grpc import TestServiceStub

from config import HOST, PORT

if __name__ == '__main__':
    with grpc.insecure_channel(f"{HOST}:{PORT}") as channel:
        client = TestServiceStub(channel)

        print("1. simple")
        print("2. respose stream")
        print("3. request stream")
        print("4. bidirectional")

        rpc = input("> ")

        if rpc == "1":
            raise NotImplementedError("simple rpc")
        elif rpc == "2":
            raise NotImplementedError("respose stream rpc")
        elif rpc == "3":
            raise NotImplementedError("request stream rpc")
        elif rpc == "4":
            raise NotImplementedError("bidirectional rpc")
