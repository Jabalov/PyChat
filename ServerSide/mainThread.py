import serverFunctions, socket
from threading import Thread


SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(('', 4466))
SERVER.listen(5)


ACCEPT_THREAD = Thread(target=serverFunctions.main_thread, args=(SERVER,))
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()


SERVER.close()
