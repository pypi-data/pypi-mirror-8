import json
from websocketserver import WebSocket, SimpleWebSocketServer




class WebExporter(WebSocket):
    def handleMessage(self):
        if self.data is None:
            self.data = ''

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'


class WebSocketBackend(object):
    def __init__(self, clust):
        self.clust = clust
        port = clust.websocket.get('port', 6769)
        self.server = SimpleWebSocketServer(clust.addr, port, WebExporter)


    def run(self):
	self.server.serveforever()


    def get_info(self):
        return {'nb_connexions': len(self.server.connections)}
    

    def send_all(self, o):
        try:
            msg = json.dumps(o)
        except ValueError:
            print "BAD MESSAGE"
            return
        for client in self.server.connections.itervalues():
            print "SENDING"*100
            try:
                client.sendMessage(msg)
            except Exception as n:
                print n
            print "SENT DONE"*100
        
