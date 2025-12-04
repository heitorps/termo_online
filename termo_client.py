import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

nome = input("Digite o seu nome: ")

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8081)
print ('connecting to %s port %s' % server_address)
sock.connect(server_address)
sock.send(nome.encode('utf-8'))

round = 1
while(round  <= 6):
    # numero da rodada
    # message = sock.recv(1600).decode('utf-8')
    print(f"Rodada {round}")
    round += 1

    # pessoa da vez
    message = sock.recv(1600).decode('utf-8')
    print(message)

    # message = sock.recv(1600).decode('utf-8')
    # print(message)

    while(True):
        message = input()
        sock.send(message.encode('utf-8'))

        message = sock.recv(1600).decode('utf-8')
        print(message)

        RESET = "\033[0m"
        if RESET in message:
            print("Fim da sua rodada")
            break
            

        # Look for the response
        # amount_received = 0
        # amount_expected = len(message)
        
        # while amount_received < amount_expected:
            # data = sock.recv(1600).decode('utf-8')
            # amount_received += len(data)
            # print (f'received {data}')

    # finally:
        # print ('closing socket')
        # sock.close()

