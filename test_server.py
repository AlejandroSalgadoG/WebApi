from concurrent import futures

import grpc
from generated.test_pb2 import TestReply, TestMultiReply
from generated.test_pb2_grpc import (
    add_TestServiceServicer_to_server,
    TestServiceServicer,
)

from config import HOST, PORT


class TestService(TestServiceServicer):
    def simpleRpc(self, request, context):
        print("simple rcp request:")
        print(request)
        return TestReply(msg=f"{request.name} hi")

    def responseStreamRpc(self, request, context):
        print("response stream rcp request:")
        print(request)

        for i in range(3):
            yield TestReply(msg=f"{request.name} hi {i+1}")

    def requestStreamRpc(self, request_iterator, context):
        multi_reply = TestMultiReply()
        for request in request_iterator:
            print("request stream rcp request:")
            print(request)

            multi_reply.request.append(request)

        multi_reply.msg = f"sent {len(multi_reply.request)} requests"
        return multi_reply


    def bidirectionalStreamRpc(self, request_iterator, context):
        for request in request_iterator:
            print("bidirectional stream rcp request:")
            print(request)

            yield TestReply(msg=f"{request.name} {request.msg} - hi")


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_TestServiceServicer_to_server(TestService(), server)
    server.add_insecure_port(f"{HOST}:{PORT}")
    server.start()
    print("server started")
    server.wait_for_termination()
