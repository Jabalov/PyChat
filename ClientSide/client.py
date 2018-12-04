from threading import Thread
import pickle, socket


CLIENT = socket.socket()
username, targetname = None, None

def send_data(client, data):
    if client.send(pickle.dumps(data)) == 0:
        sys.exit()

def recv_data(client):
    recvd_data = client.recv(1024)
    if recv_data == '':
        sys.exit()
    return pickle.loads(recvd_data)

def start_connection():
    global username, targetname
    CLIENT.connect(('35.240.84.231', 4466))

    while True:
        opt, src, msg = recv_data(CLIENT)

        if opt == 'POST' and src == 'HELLO':
            print("Connected!\n")

        if opt == 'GET' and src == 'USER':
            username = input("Enter username: ")
            send_data(CLIENT, ("POST", "USER", username))

        if opt == 'ERROR' and src == 'USERTAKEN':
            send_data(CLIENT, ("POST", "USER", input("Taken! Try again: ")))

        if opt == 'INFO' and src == 'READY':
            print("Chat Startred!")
            TR, TX = Thread(target=receiver), Thread(target=sender)
            TR.start(); TX.start()
            TR.join(); TX.join()
            CLIENT.close()
            quit()

def receiver():
    while True:
        opt, src, msg = recv_data(CLIENT)

        if opt == 'MSG':
            print("\n%s : %s" % (src, msg))


def sender():
    global targetname
    while True:
        raw_input = input("\n%s:" % username)

        if raw_input[0:2] == '!p':
            targetname = raw_input.split(' ')[1]
            continue

        if targetname:
            send_data(CLIENT, ("MSG", targetname, raw_input))

start_connection()
