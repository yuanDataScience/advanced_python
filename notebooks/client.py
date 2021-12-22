"""Example gRPC weather client"""
import grpc

import weather_grpc_pb2 as pb
import weather_grpc_pb2_grpc as gpb

# Create message
message = pb.Temperature(station='NYC', value=3.4)
message.time.GetCurrentTime()
print('sending:', message)


# open the connection to the server using the port 8088
# and create a channel(chan) to the server
with grpc.insecure_channel('localhost:8088') as chan:
    # create the connection to the server (stub)
    stub = gpb.WeatherStub(chan)
    # call method and get the response
    resp = stub.AddTemperature(message)
    print(f'Total of {resp.record_count} records')
