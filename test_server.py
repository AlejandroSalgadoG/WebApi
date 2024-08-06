from concurrent import futures

import grpc
from generated.test_pb2 import TestReply
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
        return super().responseStreamRpc(request, context)

    def requestStreamRpc(self, request_iterator, context):
        return super().requestStreamRpc(request_iterator, context)

    def bidirectionalStreamRpc(self, request_iterator, context):
        return super().bidirectionalStreamRpc(request_iterator, context)


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_TestServiceServicer_to_server(TestService(), server)
    server.add_insecure_port(f"{HOST}:{PORT}")
    server.start()
    print("server started")
    server.wait_for_termination()
