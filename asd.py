# -*- encoding: utf-8 -*-

import wx,subprocess,os,sys,socket,threading

class MyTxtCtr(wx.PySimpleApp):
    
    def OnInit(self):
        HOST, PORT = socket.gethostname(), 61955
        argvs = sys.argv

        instance_name = u"%s-%s" % (self.GetAppName(), wx.GetUserId())
        self.instance = wx.SingleInstanceChecker(instance_name)
        if self.instance.IsAnotherRunning():
            if len(argvs) >= 2:
                self.client(HOST, PORT, argvs)
            wx.Exit()
        else:
            server = self.start_server(HOST, PORT)

        # タスクトレイ
        self.tb_ico=wx.TaskBarIcon()
        self.tb_ico.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTbiLeftDClick)
        self.tb_ico.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.OnTbiRightUp)
        self.ico = wx.Icon("homu.ico", wx.BITMAP_TYPE_ICO)
        self.tb_ico.SetIcon(self.ico, u"homuhomu")

        # タスクトレイ用メニューの作成
        self.menu = wx.Menu()
        self.menu.Append(1,   u"Exit(&X)")
        wx.EVT_MENU(self.menu, 1, self.OnClose)

        self.Frm = wx.Frame(None, -1, "homuLauncher", size=(400,60),pos=(400,400))
        self.TxtCtr = wx.TextCtrl(self.Frm, -1)
        self.Frm.Show()
        return 1

    def start_server(self,host, port):

        server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
        ip, port = server.server_address
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.setDaemon(True)
        server_thread.start()

    def client(self,ip, port, argvs):
        message = os.path.abspath(' '.join(argvs[1:]))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        sock.send(message)
        response = sock.recv(1024)
#        print "Received: %s" % response
        sock.close()

    # タスクトレイ左ダブルクリック
    def OnTbiLeftDClick(self, evt):
        if self.Frm.IsShown():
            self.Frm.Show(False)
        else:
            self.Frm.Show()
            self.Frm.Raise()
            
    # タスクトレイ右クリック
    def OnTbiRightUp(self, evt):
        self.tb_ico.PopupMenu(self.menu)

    def OnClose(self, evt):
        self.tb_ico.RemoveIcon()
        wx.Exit()

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        wx.GetApp().TxtCtr.SetValue(data)
        response = 'string length: %d' % len(data)
#        print 'responding to',data,'with',response
        self.request.send(response)
        
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

app = MyTxtCtr()
app.MainLoop()