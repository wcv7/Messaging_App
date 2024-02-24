class Commands():
    def __init__(self):
        self.UserID = 0

    def Initialise(self, UserID):
        self.UserID = UserID
    
    def GetUserID(self):
        return self.UserID
    
    def ConnectServer(self, Server):
        pass