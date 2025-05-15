import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

while True:
    user_input = input("Enter a city name or date (YYYY-MM-DD): ")
    socket.send_string(user_input)
    reply = socket.recv_string()
    print("Response:", reply)
