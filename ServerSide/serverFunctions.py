from threading import Thread
import pickle
import sys

users_addresses_database = {}


def send_data(client, data):
    return client.send(pickle.dumps(data))

def recv_data(client):
    return pickle.loads(client.recv(1024))


def main_thread(main_socket):
    while True:
        client_socket, client_address = main_socket.accept()
        send_data(client_socket, ("POST", "HELLO", "Connected!"))
        Thread(target=handle_client, args=(client_socket, client_address)).start()


def handle_client(client, address):
    while True:
        send_data(client, ("GET", "USER", ""))
        opt, src, user_name = recv_data(client)

        if opt == 'POST' and src == 'USER':
            if user_name in users_addresses_database:
                send_data(client, ("ERROR", "USERTAKEN", ""))
            else:
                users_addresses_database[user_name] = (client, address)
                send_data(client, ("INFO", "READY", ""))
                break

    while True:
        opt, src, msg = recv_data(client)

        if opt == 'EXIT':
            del users_addresses_database[user_name]
            return

        if opt == 'MSG':
            if src in users_addresses_database:
                t_client, t_address= users_addresses_database[src]
                send_data(t_client, ("MSG", user_name, msg))
            else:
                send_data(client, ("ERROR", "USEROFFLINE", ""))
