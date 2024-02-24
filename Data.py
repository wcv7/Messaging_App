import sqlite3
import Encrypt

def Initialise():
    with sqlite3.connect("Data.db") as db:
        cursor = db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS User(
                 UserID integer,
                 Firstname varchar(20),
                 Lastname varchar(20),
                 Username text UNIQUE,
                 Email text UNIQUE,
                 Password text,
                 Primary key(UserID));
               """
        cursor.execute(sql)
    with sqlite3.connect("Data.db") as db:
        cursor = db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS Message(
                 MessageID integer,
                 UserID integer,
                 UserIDSent text,
                 Message text,
                 Primary key(MessageID));
               """
        cursor.execute(sql)
    with sqlite3.connect("Data.db") as db:
        cursor = db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS Bank(
                 UserID integer,
                 Balance integer,
                 Primary key(UserID));
               """
        cursor.execute(sql)
def ViewTable():
    with sqlite3.connect("Data.db") as db:
        cursor = db.cursor()
        sql = """SELECT * FROM User;"""
        cursor.execute(sql)
        result = cursor.fetchall()
        for each in result:
            print(each)

class User():
    def __init__(self):
        self.Username = ""
        self.FName = ""
        self.LName = ""
        self.Email = ""
        self.Password = ""
        self.UserID = 0
        self.TempMessageList = ""
        self.Balance = 0

    def GetUsername(self):
        return self.Username
    
    def GetPassword(self):
        return self.Password

    def GetFName(self):
        return self.FName
    
    def GetLName(self):
        return self.LName
    
    def GetEmail(self):
        return self.Email
    
    def GetUserID(self):
        return self.UserID
    
    def GetBalance(self):
        return self.Balance
    
    def SetUserID(self, UserID):
        self.UserID = UserID

    def SetUsername(self, Username):
        self.Username = Username

    def SetFName(self, FName):
        self.FName = FName
    
    def SetLName(self, LName):
        self.LName = LName

    def SetEmail(self, Email):
        self.Email = Email

    def SetPassword(self, Password):
        self.Password = Password
    
    def SetBalance(self, Balance):
        self.Balance = Balance

    def LogAssociate(self, UserID):
        try:
            Values = (UserID,)
            with sqlite3.connect("Data.db") as db:
                cursor = db.cursor()
                sql = """SELECT * FROM User
                        WHERE UserID = ?;
                    """
                cursor.execute(sql, Values)
                result, = cursor.fetchall()
                self.SetUserID(result[0])
                self.SetFName(result[1])
                self.SetLName(result[2])
                self.SetUsername(result[3])
                self.SetEmail(result[4])
                self.SetPassword(result[5])
                Values = (self.GetUserID(),)
                sql = """SELECT Balance FROM Bank
                        WHERE UserID = ?;
                      """
                cursor.execute(sql, Values)
                result = cursor.fetchone()
                self.SetBalance(result[0])
        except:
            return False
        
    def GetUsernameFromID(self, UserID):
        try:
            Values = (UserID,)
            with sqlite3.connect("Data.db") as db:
                cursor = db.cursor()
                sql = """SELECT Username FROM User
                        WHERE UserID = ?;
                    """
                cursor.execute(sql, Values)
                result, = cursor.fetchone()
                return result
        except:
            return "Failed To Get Username"
        
    def SearchUser(self, Field):
        try:
            Values = (Field, Field)
            with sqlite3.connect("Data.db") as db:
                cursor = db.cursor()
                sql = """SELECT Username FROM User
                        WHERE Username = ? OR UserID = ?;
                    """
                cursor.execute(sql, Values)
                result, = cursor.fetchone()
                if result == Field:
                    return True
                else:
                    return False
        except:
            return False

    def FindUserID(self, Field):
        try:
            Values = (Field, Field)
            with sqlite3.connect("Data.db") as db:
                cursor = db.cursor()
                sql = """SELECT UserID FROM User
                        WHERE Username = ? OR Email = ?;
                    """
                cursor.execute(sql, Values)
                result, = cursor.fetchone()
                return result
        except:
            return False

    def CheckPassword(self, Password, UserID):
        try:
            Values = (UserID,)
            with sqlite3.connect("Data.db") as db:
                cursor = db.cursor()
                sql = """SELECT Password FROM User
                        WHERE UserID = ?;
                    """
                cursor.execute(sql, Values)
                result, = cursor.fetchone()
                if result == Password:
                    return True
                else:
                    return False
        except:
            return False
            
    def Login(self, Field, Password):
        Values = (Field, Password)
        UserID = self.FindUserID(Field)
        if UserID != False:
            if self.CheckPassword(Password, UserID):
                self.LogAssociate(UserID)
                return True
            else:
                return False
        else:
            return False
        
    def CreateAccount(self, FName, LName, Username, Email, Password):
        try:
            Values = (FName, LName, Username, Email, Password)
            with sqlite3.connect("Data.db") as db:
                cursor = db.cursor()
                sql = """INSERT INTO User(Firstname, Lastname, Username, Email, Password)
                        Values(?, ?, ?, ?, ?)
                    """
                cursor.execute(sql, Values)
                db.commit()
                UserID = self.FindUserID(Username)
                Values = (UserID, 0)
                sql = """INSERT INTO Bank(UserID, Balance)
                         Values(?, ?)
                      """
                cursor.execute(sql, Values)
                db.commit()
                return True
        except:
            return False


    def SignUp(self, FName, LName, Username, Email, Password):
        if self.CreateAccount(FName, LName, Username, Email, Password):
            return True
        else:
            return False
        
    def Messaging(self, Parameter):
        print(Parameter)
        Cmd = Parameter[0].lower()
        del Parameter[0]
        if Cmd == "message":
            UserTo = Parameter[0]
            del Parameter[0]
            Message = ""
            for each in Parameter:
                Message += each + " "
            print(Message)
            if self.SearchUser(UserTo):
                SendToUser = self.FindUserID(UserTo)
                Values = (SendToUser, self.GetUserID(), Message)
                try:
                    with sqlite3.connect("Data.db") as db:
                        cursor = db.cursor()
                        sql = """INSERT INTO Message(UserID, UserIDSent, Message)
                                Values(?, ?, ?)
                            """
                        cursor.execute(sql, Values)
                        db.commit()
                        print("Message Sent!")
                except:
                    print("Message Failed To Send")
            else:
                print("User Does Not Exist")
        elif Cmd == "inbox":
            try:
                with sqlite3.connect("Data.db") as db:
                    cursor = db.cursor()
                    Values = (self.GetUserID(),)
                    sql = """SELECT MessageID, UserIDSent FROM Message
                            WHERE UserID = ?;
                        """
                    cursor.execute(sql, Values)
                    result = cursor.fetchall()
                    self.TempMessageList = result
                    i = 1
                    for each in result:
                        Username = self.GetUsernameFromID(each[1])
                        if Username == "Failed To Get Username":
                            print("Error Getting Message")
                        else:
                            print(i, "- Message From " + Username)
                        i += 1
            except:
                print("Error Getting Inbox")
        elif Cmd == "recieve":
            try:
                MessageToRecieve = Parameter[0]
                if MessageToRecieve != "all":
                    MessageToRecieve = int(MessageToRecieve)
                    with sqlite3.connect("Data.db") as db:
                        cursor = db.cursor()
                        MessageTuple = self.TempMessageList[MessageToRecieve-1]
                        MessageID = MessageTuple[0]
                        Values = (MessageID,)
                        sql = """SELECT Message FROM Message
                                WHERE MessageID = ?;
                            """
                        cursor.execute(sql, Values)
                        result, = cursor.fetchone()
                        print(result)
                else:
                    with sqlite3.connect("Data.db") as db:
                        cursor = db.cursor()
                        Values = (self.GetUserID(),)
                        sql = """SELECT Message FROM Message
                                WHERE UserID = ?;
                            """
                        cursor.execute(sql, Values)
                        result = cursor.fetchall()
                        for each in result:
                            print(each[0])
            except:
                print("Message Failed To Recieve")
        elif Cmd == "delete":
            try:
                MessageToDelete = Parameter[0]
                if MessageToDelete != "all":
                    MessageToDelete = int(MessageToDelete)
                    with sqlite3.connect("Data.db") as db:
                        cursor = db.cursor()
                        MessageTuple = self.TempMessageList[MessageToDelete-1]
                        MessageID = MessageTuple[0]
                        Values = (MessageID,)
                        sql = """DELETE FROM Message
                                WHERE MessageID = ?;
                            """
                        cursor.execute(sql, Values)
                        db.commit()
                        print("Successfully Deleted Message!")
                else:
                    with sqlite3.connect("Data.db") as db:
                        cursor = db.cursor()
                        Values = (self.GetUserID(),)
                        sql = """DELETE FROM Message
                                WHERE UserID = ?;
                            """
                        cursor.execute(sql, Values)
                        db.commit()
                        print("All Messages Successfully Deleted!")
            except:
                print("Message Failed To Delete")
        elif Cmd == "cmds":
            print("'Message' '{Username}' '{Message}' -- Sends A Message To Selected User \n'Inbox' -- Gives A List Of All Incoming Messages \n'Recieve' '{Number From Inbox Or 'All'}' -- Recieves The Message Selected \n'Delete' '{Number From Inbox Or 'All'}' -- Deletes The Selected Message")

    def UpdateBalance(self):
        with sqlite3.connect("Data.db") as db:
            cursor = db.cursor()
            Values = (self.GetBalance(), self.GetUserID())
            sql = """UPDATE Bank
                     SET Balance = ?
                     WHERE UserID = ?
                  """
            cursor.execute(sql, Values)
            db.commit()
            return True

    def Bank(self, Parameter):
        print(Parameter)
        Cmd = Parameter[0].lower()
        del Parameter[0]
        if Cmd == "balance":
            try:
                with sqlite3.connect("Data.db") as db:
                    cursor = db.cursor()
                    Values = (self.GetUserID(),)
                    sql = """SELECT Balance FROM Bank
                             WHERE UserID = ?
                            """
                    cursor.execute(sql, Values)
                    result, = cursor.fetchone()
                    print(f"Balance: {result}")
                    self.SetBalance(1200)
                    self.UpdateBalance()
            except:
                print("Error Getting Balance")
        elif Cmd == "send":
            Amount = int(Parameter[1])
            UserToSendTo = Parameter[0]
            with sqlite3.connect("Data.db") as db:
                cursor = db.cursor()
                Values = (self.FindUserID(UserToSendTo), Amount)
                sql = """SELECT Balance FROM"""
        elif Cmd == "cmds":
            print("'Balance' -- Checks Your Balance \n'Send' '{Username}' '{Amount}' -- Sends Selected User Amount Of Money")

    def Command(self, Parameter):
        Parameter = Parameter.split(" ")
        print(Parameter)
        Cmd = Parameter[0].lower()
        del Parameter[0]
        if Cmd == "messaging":
            self.Messaging(Parameter)
        elif Cmd == "banking":
            self.Bank(Parameter)
        elif Cmd == "cmds":
            print("'Cmds' -- Gives List Of All Commands \n")
        
    def CheckMessages(self):
        pass

    def CheckMessagesFrom(self, FromUser):
        pass
        
    def Message(self, ToUser, Message):
        pass