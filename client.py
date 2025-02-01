#/usr/bin/python3

import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText


def send_message(client_socket, username, text_widget, entry_widget):
    message = entry_widget.get()
    client_socket.sendall(f"{username} > {message}".encode()) # La data debe ser convertida en 1 y 0

    entry_widget.delete(0, END) # Cuando se envie el mesnaje limpiar la pantalla
    text_widget.configure(state='normal')
    text_widget.insert(END, f"{username} > {message}\n") #Para que pueda seguir un flujo de arriba a abajo el chat
    text_widget.configure(state='disabled')

def receive_message(client_socket, text_widget):
    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break
            text_widget.configure(state='normal')
            text_widget.insert(END,message)
            text_widget.configure(state='disabled')
        except:
            break

    client.socket.close()
    client.remove(client_socket)
    del usernames[client_socket]


def list_users_request(client_socket):
    client_socket.sendall("!usuarios".encode())


def exit_request(client_socket, username, window):

    #AVISO  a todo el mundo de que el usuario se sale 
    client_socket.sendall(f"\n[!]El usuario ha salido del chat {username}\n\n".encode())
    #desconectar las conexiones del cliente y del servidor
    client_socket.close()
    #cerrar la ventana y 
    window.quit()
    window.destroy()


def client_program():

    host = 'localhost'
    port = 1234

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host,port))

    username = input(f"[+] Ingrese tu usuario: ")
    client_socket.sendall(username.encode())


    window = Tk()
    window.title('Chat')

    text_widget = ScrolledText(window, state='disabled')
    text_widget.pack(padx=5, pady=5)
    
    #Establecemos el frame donde estará el entry y el boton para enviar
    frame_widget = Frame(window)
    frame_widget.pack(padx=5, pady=5, fill=BOTH, expand=1)
    

    entry_widget = Entry(frame_widget)
    entry_widget.bind("<Return>", lambda _: send_message(client_socket, username, text_widget, entry_widget))
    entry_widget.pack(side=LEFT, fill=BOTH, expand=1)

    button_widget = Button(frame_widget, text="Enviar", command=lambda: send_message(client_socket, username, text_widget, entry_widget))
    button_widget.pack(side=RIGHT, padx =5)


    user_widget = Button(frame_widget, text="Listar usuarios", command=lambda: list_users_request(client_socket))
    user_widget.pack(padx =5, pady=5)


    user_widget = Button(frame_widget, text="Salir", command=lambda: exit_request(client_socket, username, window))
    user_widget.pack(padx =5, pady=5)

    thread = threading.Thread(target=receive_message, args=(client_socket, text_widget))
    thread.daemon = True
    thread.start()


    window.mainloop()
    client_socket.close()

if __name__ == '__main__':
    client_program()

