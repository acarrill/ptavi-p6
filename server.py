#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os

try:
    ServerIP = sys.argv[1]
    ServerPort = int(sys.argv[2])
    Audio = sys.argv[3]
    print("Listening...")
except IndexError:
    print("Usage: python server.py IP port audio_file")

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        """Manejador de conexión"""
        Received = self.rfile.read().decode('utf-8')
        ClientMethod = Received.split(' ')[0]
        if ClientMethod == 'INVITE':
            self.wfile.write(bytes('SIP/2.0 100 Trying\r\n'
                            'SIP/2.0 180 Ring\r\n'
                            'SIP/2.0 200 OK\r\n\r\n', 'utf-8'))
        elif ClientMethod == 'BYE':
            self.wfile.write(b('SIP/2.0 200 OK\r\n\r\n'))
        elif ClientMethod == 'ACK':
            ToClientExe = './mp32rtp -i 127.0.0.1 -p 23032 < ' + Audio
            os.system(ToClientExe)
        else:
            self.wfile.write(b('SIP/2.0 405 Method Not Allowed\r\n\r\n'))
            
                            
        
        


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((ServerIP, ServerPort), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
