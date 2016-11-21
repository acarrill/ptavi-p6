#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Parámetros para establecer la conexión.
try:
    Method = sys.argv[1].upper()
    ReceiverLogin = sys.argv[2].split('@')[0]
    ReceiverIP = (sys.argv[2].split('@')[1]).split(':')[0]
# Comprueba si el puerto es un digito antes de asignarlo
    if not str.isdigit(sys.argv[2].split(':')[1]):
        raise IndexError
    ReceiverPort = int(sys.argv[2].split(':')[1])
except IndexError:
    print("Usage: python client.py method receiver@IP:SIPport ")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
if __name__ == "__main__":
    """Se crea socket y se manda método al server"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.connect((ReceiverIP, ReceiverPort))
        Message = (Method + ' sip:' + ReceiverLogin + '@' +
                   ReceiverIP + ' SIP/2.0')

        print("Enviando:", Message)
        my_socket.send(bytes(Message, 'utf-8') + b'\r\n\r\n')
        data = my_socket.recv(1024)
        Answer = data.decode('utf-8')
        OK = ('SIP/2.0 100 Trying\r\n\r\n'  # Invite recibido correctamente
              'SIP/2.0 180 Ring\r\n\r\n'
              'SIP/2.0 200 OK\r\n\r\n')
        if Answer == OK and Method == 'INVITE':
            Method = 'ACK'
            Message = (Method + ' sip:' + ReceiverLogin + '@' +
                       ReceiverIP + ' SIP/2.0')
        try:  # Evitamos que se envien mensajes BYE innecesarios
            if Method == 'BYE':
                raise KeyboardInterrupt
            my_socket.send(bytes(Message, 'utf-8') + b'\r\n\r\n')
        except KeyboardInterrupt:
            print("You has been disconected from server")
        print('Recibido -- ', data.decode('utf-8'))
        print("Socket terminado.")
