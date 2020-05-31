import socket
import zipfile
import os


def send(client, file_name):

    path_file = "serwer/rozpakowane/" + file_name
    size = os.stat(path_file).st_size

    client.sendall(("SEND: \r\nNAME: " + file_name + "\r\nSIZE: " + str(size) + "\r\n\r\n").encode()) #dane pliku

    data = b''
    while not b'\r\n\r\n' in data:      #gotowosc do odbioru przez klienta
        data += client.recv(SIZE)


    if data.split()[0] == b'OKSEDN':

        size_send= 0

        with open(path_file, 'rb') as file:
            while size > size_send :        #wysylanie pliku
                data = file.read(SIZE)
                client.sendall(data)
                size_send+=len(data)
                print(str(size_send)+"/"+str(size))

            file.close()


        data = b''


        while not b'\r\n\r\n' in data:
            data += client.recv(SIZE)

        serwer_recv = int(((data.split(b'RECEIVED:')[1]).split(b'\r\n')[0]).decode())
        if serwer_recv == size:             #sprawdzenie czy caly plik zostal przeslany
            print("Dane zostały poprawnie wysłane")




def recv():

    data = b''
    while not b'\r\n\r\n' in data:      #inforamcje o pliku
        data += client.recv(SIZE)

    size = int((data.split(b'SIZE:')[1]).split(b'\r\n')[0])
    file_name = (data.split(b'NAME:')[1]).split(b'\r\n')[0].decode()

    print(file_name, str(size))

    data=b''
    content_lenght = 0
    with open('serwer/' + file_name, 'wb') as f:
        while content_lenght < size:            #pobieranie pliku
            data = client.recv(SIZE)
            content_lenght += len(data)
            f.write(data)
            print('Recv:  ' + str(content_lenght) + '/' + str(size))

    f.close()

    client.sendall(("RECEIVED: " + str(content_lenght)+"\r\n\r\n").encode())  #informacja o ilosci pobranych bajtow

    return file_name

def unzip(file_name):
    with zipfile.ZipFile("serwer/"+file_name, 'r') as zip_ref:      #rozpakowanie pobranego pliku .ZIP
        zip_ref.extractall("serwer/rozpakowane")

    print("Nowe pliki:")
    for file in zip_ref.namelist():
        print(file)

    print("\nWszystkie pliki:")
    list_file = os.listdir("serwer/rozpakowane")
    for file in list_file:
        print(file)



SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 1769))
s.listen(5)

while True:

    client, addr = s.accept()
    print("Connected: " + addr[0])

    try:
        data = b''
        while not b'\r\n\r\n' in data:
            data += client.recv(SIZE)

        if data.split()[0]==b'SENDZIP':     #klient chce przesylac
            client.sendall("OKSEDN\r\n\r\n".encode())

            file_name = recv()
            unzip(file_name)

        if data.split()[0] == b'RECVFILE':      #klient chce pobrac plik
            list_file = os.listdir('serwer/rozpakowane')
            list = ''
            for file in list_file:
                list+=file+' '

            client.sendall((list+"\r\n\r\n").encode())  #przeslanie listy dostepnych plikow

            data = b''
            while not b'\r\n\r\n' in data:          #odebranie nazwy pliku
                data += client.recv(SIZE)

            file_name = data.decode()
            file_name=file_name[:-4]
            print(file_name)
            if list_file.count(file_name):
                send(client,file_name)


    except:
        print("ERROR")