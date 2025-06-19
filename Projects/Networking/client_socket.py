#TCP client socket program to solve mathematical questions given by the server
from socket import *
def create_connect_socket():
    serName = 'localhost'
    serPort = 8888
    cli_socket = socket(AF_INET, SOCK_STREAM)
    cli_socket.connect((serName, serPort))
    return cli_socket
def solve_math(question):
    _, numb_one, oprtr, numb_two = question.split()
    numb_one, numb_two = int(numb_one), int(numb_two)
    operations = {
        '+': numb_one + numb_two,
        '-': numb_one - numb_two,
        '*': numb_one * numb_two,
        '/': numb_one // numb_two
    }
    return operations[oprtr]

def trigger_client():
    csocket = create_connect_socket()
    welcome = csocket.recv(1024).decode().strip()
    print(f"Server: {welcome}")
    husky_name = input("Enter your Husky username: ")
    srvr_msg = f"HELLO {husky_name}\n"
    print(f"Sending: {srvr_msg.strip()}")
    csocket.send(srvr_msg.encode())
    while True:
        cli_msg = csocket.recv(1024).decode().strip()
        print(f"Server: {cli_msg}")
        if "DONE" in cli_msg:
            print(f"FLAG: {cli_msg.split()[1]}")
            break
        elif "MATH" in cli_msg:
            answer = solve_math(cli_msg)
            response = f"ANSWER {answer}\n"
            print(f"Sending: {response.strip()}")
            csocket.send(response.encode())
        elif not cli_msg:
            print("No data!")
            break
    csocket.close()

if __name__ == "__main__":
    trigger_client ()
