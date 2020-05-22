import socket
import os
from tkinter import filedialog as fd


def send(s, path_file):

    size = os.stat(path_file).st_size
    file_name = path_file.split("/")[-1]

    s.sendall(("SEND: \r\nNAME: " + file_name + "\r\nSIZE: " + str(size) + "\r\n\r\n").encode())

    data = b''
    while not b'\r\n\r\n' in data:
        data += s.recv(SIZE)

    print(data)

    if data.split()[0] == b'OKSEDN':

        size_send= 0

        with open(path_file, 'rb') as file:
            while size > size_send :
                data = file.read(SIZE)
                s.sendall(data)
                size_send+=len(data)
                #print('Sent ' + repr(data))
                print(str(size_send)+"/"+str(size))

            file.close()


        data = b''


        while not b'\r\n\r\n' in data:
            data += s.recv(SIZE)

        serwer_recv = int(((data.split(b'RECEIVED:')[1]).split(b'\r\n')[0]).decode())
        if serwer_recv == size:
            print("Dane zostały poprawnie wysłane")





def recv(s):

    data = b''
    while not b'\r\n\r\n' in data:
        data += s.recv(SIZE)

    size = int((data.split(b'SIZE:')[1]).split(b'\r\n')[0])
    file_name = (data.split(b'NAME:')[1]).split(b'\r\n')[0].decode()

    print(file_name, str(size))
    s.sendall("OKSEDN\r\n\r\n".encode())

    data=b''
    content_lenght = 0
    with open('klient/pobrane/' + file_name, 'wb') as f:
        while content_lenght < size:
            print("a")
            data = s.recv(SIZE)
            print("b")
            content_lenght += len(data)
            f.write(data)
            print('Recv:  ' + str(content_lenght) + '/' + str(size))

    f.close()

    s.sendall(("RECEIVED: " + str(content_lenght)+"\r\n\r\n").encode())

    return file_name


def action(s):

    a = input("S - wyślij, R - pobierz")

    if a =="S":
        s.sendall('SENDZIP\r\n\r\n'.encode())
        filename = fd.askopenfilename(filetypes=[("Plik archwium", "*.zip")])
        send(s, filename)

    elif a=="R":
        s.sendall('RECVFILE\r\n\r\n'.encode())
        print("Lista plikow: ")

        data = b''
        while not b'\r\n\r\n' in data:
            data += s.recv(SIZE)

        data = data.decode()
        data = data.split(' ')
        i = 1
        for file in data:
            print(str(i) + ". " + file)
            i += 1

        print(data)


        file_name = input("Podaj nazwe pliku do pobrania: ")

        s.sendall((file_name + '\r\n\r\n').encode())

        if data.count(file_name):
            recv(s)
        else:
            print("Plik o podanej nazwie nie jest dostępny")

    else:
        print("Nie poprawna komenda")


SIZE = 1024


def main():


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect(("localhost", 1769))
    action(s)





if __name__ == '__main__':
    main()



