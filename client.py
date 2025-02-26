import socket
import os.path as path
import sys

IP = '127.0.0.1'  # change to the IP address of the server
PORT = 12000  # change to a desired port number
BUFFER_SIZE = 1024  # change to a desired buffer size

CONSOLE = "/usr/local/bin/python3.12 /Users/nbklaus21/Documents/VSCodeProjects/devDSU2025/ComputerNetworking/ProgrammingAssignments/ProgrammingAssignment2/ComputerNetworkingProgrammingAssignment2/client.py hello.txt 127.0.0.1 12000"

def get_file_size(file_name: str) -> int:
    size = 0
    try:
        size = path.getsize(file_name)
    except FileNotFoundError as fnfe:
        print(fnfe)
        sys.exit(1)
    return size


def send_file(filename: str, address: (str | int)):
    ret_value = 0
    # get the file size in bytes
    # TODO: section 2 step 2
    file_size = get_file_size(filename)
    
    # convert file_size to an 8-byte byte string using big endian
    # TODO: section 2 step 3
    file_size_bytes = file_size.to_bytes(8, "big")
    
    # create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # TODO: section 2 step 5
        client_socket.connect((IP, PORT))
        
        # send the file size in the first 8-bytes followed by the bytes
        # for the file name to server at (IP, PORT)
        # TODO: section 2 step 6
        message = file_size_bytes + file_name.encode()
        print(f"[+] Sending server the following message: {message}")
        client_socket.send(message)
        
        # TODO: section 2 step 7
        response = client_socket.recv(BUFFER_SIZE).decode()
        if response != "go ahead":
            raise OSError("Bad server response - was not go ahead!")
        
        # open the file to be transferred
        with open(file_name, 'rb') as file:
            # read the file in chunks and send each chunk to the server
            is_done = False
            while not is_done:
                pass
                # TODO: section 2 step 8a
                chunk = file.read(BUFFER_SIZE)
                # TODO: section 2 step 8b
                if len(chunk) > 0:
                    client_socket.send(chunk)
            
    except OSError as e:
        ret_value = 2
        print(f'An error occurred while sending the file:\n\t{e}')
    finally:
        client_socket.close()
    return ret_value

if __name__ == "__main__":
    # get filename from cmd line
    if len(sys.argv) < 2:
        print(f'SYNOPSIS: {sys.argv[0]} <filename> [IP address] [Port]')
        sys.exit(1)
    file_name = sys.argv[1]  # filename from cmdline argument
    # if an IP address is provided on cmdline, then use it
    if len(sys.argv) == 3:
        IP = sys.argv[2]

    try:
        # if port is provided on cmdline, then use it
        if len(sys.argv) == 4:
            PORT = int(sys.argv[3])
    except ValueError as ve:
        print(ve)

    ret_value = send_file(file_name, (IP, PORT))
    sys.exit(ret_value)




