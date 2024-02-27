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
    with sqlite3.connect("Data.db") as db:
        cursor = db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS Social(
                 UserID integer,
                 Friends integer,
                 FriendRequests integer,
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
            Password = Encrypt.Encryptor.Encrypt(Password)
            print(Password)
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
        
    def ChangeTableName(self, Name):
        try:
            with sqlite3.connect("Data.db") as db:
                cursor = db.cursor()
                sql = """ALTER TABLE {}
                         RENAME TO {}
                      """.format(self.GetUsername(), Name)
                cursor.execute(sql)
            print("Success")
        except:
            print("Failed To Change Table Name")
        
    def InitialisePassManager(self, Username):
        try:
            with sqlite3.connect("Data.db") as db:
                cursor = db.cursor()
                sql = """CREATE TABLE IF NOT EXISTS {}(
                            AccountID integer,
                            AccountName text,
                            AccountUsername text,
                            AccountPassword text,
                            Extra text,
                            Primary key(AccountID));
                        """.format(Username)
                cursor.execute(sql)
        except:
            print("Failed To Create Table")

    def UpdateData(self, Data , Field, UserID):
        if Data == "password":
            Field = Encrypt.Encryptor.Encrypt(Field)
        Data = Data.capitalize()
        print(Data)
        Values = (Field, UserID)
        with sqlite3.connect("Data.db") as db:
            cursor = db.cursor()
            sql = """UPDATE User
                     SET {} = ?
                     WHERE UserID = ?
                    """.format(Data)
            cursor.execute(sql, Values)
            db.commit()
            print("Updated", Data)
            
    def Login(self, Field, Password):
        Values = (Field, Password)
        UserID = self.FindUserID(Field)
        if UserID != False:
            if self.CheckPassword(Password, UserID):
                self.LogAssociate(UserID)
                self.InitialisePassManager(self.GetUsernameFromID(UserID))
                return True
            else:
                return False
        else:
            return False
        
    def CreateAccount(self, FName, LName, Username, Email, Password):
        try:
            Password = Encrypt.Encryptor.Encrypt(Password)
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
            self.InitialisePassManager(Username)
            return True
        else:
            return False
        
    def CheckBalanceFromUserID(self, UserID):
        try:
            with sqlite3.connect("Data.db") as db:
                cursor = db.cursor()
                Values = (UserID,)
                sql = """SELECT Balance FROM Bank
                        WHERE UserID = ?
                    """
                cursor.execute(sql, Values)
                result = cursor.fetchone()
                return result[0]
        except:
            print("Error Retrieving Balance")
        
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
            Message = Encrypt.Encryptor.Encrypt(Message)
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
        elif Cmd == "outbox":
            try:
                with sqlite3.connect("Data.db") as db:
                    cursor = db.cursor()
                    Values = (self.GetUserID(),)
                    sql = """SELECT MessageID, UserID FROM Message
                            WHERE UserIDSent = ?;
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
                            print(i, "- Message To " + Username)
                        i += 1
            except:
                print("Error Getting Outbox")
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
                        result = Encrypt.Encryptor.Decrypt(result)
                        print(result)
                else:
                    with sqlite3.connect("Data.db") as db:
                        cursor = db.cursor()
                        Values = (self.GetUserID(),)
                        sql = """SELECT Message, UserID FROM Message
                                WHERE UserID = ?;
                            """
                        cursor.execute(sql, Values)
                        result = cursor.fetchall()
                        i = 1
                        for each in result:
                            print(i, "- " + self.GetUsernameFromID(each[1]) + ":", Encrypt.Encryptor.Decrypt(each[0]))
                            i += 1
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
                        Values = (self.GetUserID(),)
                        sql = """SELECT MessageID, UserID FROM Message
                            WHERE UserIDSent = ?;
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
                                print(i, "- Message To " + Username)
                            i += 1
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
                        Values = (self.GetUserID(),)
                        sql = """SELECT MessageID, UserID FROM Message
                            WHERE UserIDSent = ?;
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
                                print(i, "- Message To " + Username)
                            i += 1
            except:
                print("Message Failed To Delete")
        elif Cmd == "cmds":
            print("'Message' '{Username}' '{Message}' -- Sends A Message To Selected User \n'Inbox' -- Gives A List Of All Incoming Messages \n'Recieve' '{Number From Inbox Or 'All'}' -- Recieves The Message Selected \n'Delete' '{Number From Inbox Or 'All'}' -- Deletes The Selected Message \n'Outbox' -- Checks All Outgoing Messages \n'Back' -- Goes Back To Main App")

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
            if len(Parameter) > 0:
                try:
                    UserToCheckBalance = Parameter[0]
                    Password = Parameter[1]
                    UserIDToCheckBalance = self.FindUserID(UserToCheckBalance)
                    if self.CheckPassword(Password, UserIDToCheckBalance):
                        print(f"Balance: {self.CheckBalanceFromUserID(UserIDToCheckBalance)}")
                    else:
                        print("Wrong Password")
                except:
                    print("You Entered Command Wrong Or Got Wrong Password")
            else:
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
                        self.UpdateBalance()
                except:
                    print("Error Getting Balance")
        elif Cmd == "send":
            try:
                Amount = int(Parameter[1])
                UserToSendTo = Parameter[0]
                if Amount < self.Balance:
                    with sqlite3.connect("Data.db") as db:
                        cursor = db.cursor()
                        Values = (Amount, self.FindUserID(UserToSendTo))
                        sql = """UPDATE Bank
                                SET Balance = Balance + ?
                                WHERE UserID = ?
                            """
                        cursor.execute(sql, Values)
                    self.Balance = self.Balance - Amount
                    self.UpdateBalance()
                else:
                    print("Not Enough In Your Account")
            except:
                print("Entered Command Wrong")
        elif Cmd == "transfer":
            try:
                Amount = int(Parameter[1])
                UserToGetFrom = Parameter[0]
                Password = Parameter[2]
                UserIDToGetFrom = self.FindUserID(UserToGetFrom)
                if self.CheckPassword(Password, UserIDToGetFrom):
                    if self.CheckBalanceFromUserID(UserIDToGetFrom) >= Amount:
                        try:
                            with sqlite3.connect("Data.db") as db:
                                cursor = db.cursor()
                                Values = (Amount, UserIDToGetFrom)
                                sql = """UPDATE Bank
                                        SET Balance = Balance - ?
                                        WHERE UserID = ?
                                    """
                                cursor.execute(sql, Values)
                            self.Balance = self.Balance + Amount
                            self.UpdateBalance()
                        except:
                            print("Error Transfering")
                    else:
                        print("Not Enough In The Account")
                else:
                    print("Wrong Password!")
            except:
                print("Error")
        elif Cmd == "cmds":
            print("'Balance' '{Username}' '{Password}' -- Checks Balance, Username If You Want To See Another Account \n'Send' '{Username}' '{Amount}' -- Sends Selected User Amount Of Money \n'Transfer' '{Username}' '{Amount}' '{Password}' -- Transfers Amount From Account \n'Back' -- Goes Back To Main App")

    def Settings(self, Parameter):
        print(Parameter)
        Cmd = Parameter[0].lower()
        del Parameter[0]
        if Cmd == "update":
            try:
                Cmd2 = Parameter[0].lower()
                del Parameter[0]
                if Cmd2 == "password":
                    Password = Parameter[0]
                    NewPass = Parameter[1]
                    if self.CheckPassword(Password, self.GetUserID()):
                        self.UpdateData(Cmd2, NewUser, self.GetUserID())
                        print("Success")
                    else:
                        print("Wrong Password!")
                elif Cmd2 == "username":
                    Username = Parameter[0]
                    NewUser = Parameter[1]
                    if self.SearchUser(NewUser):
                        print("Username Already Exists")
                    else:
                        self.ChangeTableName(NewUser)
                        self.UpdateData(Cmd2, NewUser, self.GetUserID())
                        print("Success")
                elif Cmd2 == "email":
                    Email = Parameter[0]
                    NewEmail = Parameter[1]
                    if self.SearchUser(NewEmail):
                        print("Username Already Exists")
                    else:
                        self.UpdateData(Cmd2, NewEmail, self.GetUserID())
                        print("Success")
                else:
                    print("Wrong Command")
            except:
                print("Error")
        elif Cmd == "cmds":
            print("'Update' '{Password / Username / Email}' '{Old Data}' '{New Data}' -- Updates Values \n'Back' -- Goes Back To Main App")

    def PassManager(self, Parameter):
        print(Parameter)
        Cmd = Parameter[0].lower()
        del Parameter[0]
        if Cmd == "show":
            try:
                Cmd2 = Parameter[0].lower()
                if Cmd2 == "all":
                    with sqlite3.connect("Data.db") as db:
                        cursor = db.cursor()
                        sql = """SELECT * FROM {}
                            """.format(self.GetUsername())
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        print("AccountID - Account Name  Account Username  Account Password  Extra")
                        for each in result:
                            if each[4] == None:
                                print(f"{each[0]} - {Encrypt.Encryptor.Decrypt(each[1])} {Encrypt.Encryptor.Decrypt(each[2])} {Encrypt.Encryptor.Decrypt(each[3])}")
                            else:
                                print(f"{each[0]} - {Encrypt.Encryptor.Decrypt(each[1])} {Encrypt.Encryptor.Decrypt(each[2])} {Encrypt.Encryptor.Decrypt(each[3])} {Encrypt.Encryptor.Decrypt(each[4])}")
                else:
                    with sqlite3.connect("Data.db") as db:
                        cursor = db.cursor()
                        Field = Parameter[0]
                        Field = Encrypt.Encryptor.Encrypt(Field)
                        Values = (Field, Field)
                        sql = """SELECT * FROM {}
                                    WHERE AccountName = ? OR AccountUsername = ?
                                """.format(self.GetUsername())
                        cursor.execute(sql, Values)
                        result = cursor.fetchall()
                        for each in result:
                            if each[4] == None:
                                print(f"{each[0]} - {Encrypt.Encryptor.Decrypt(each[1])} {Encrypt.Encryptor.Decrypt(each[2])} {Encrypt.Encryptor.Decrypt(each[3])}")
                            else:
                                print(f"{each[0]} - {Encrypt.Encryptor.Decrypt(each[1])} {Encrypt.Encryptor.Decrypt(each[2])} {Encrypt.Encryptor.Decrypt(each[3])} {Encrypt.Encryptor.Decrypt(each[4])}")
            except:
                print("Error")
        elif Cmd == "create":
            try:
                AccountName = Parameter[0]
                AccountName = Encrypt.Encryptor.Encrypt(AccountName)
                AccountUser = Parameter[1]
                AccountUser = Encrypt.Encryptor.Encrypt(AccountUser)
                AccountPass = Parameter[2]
                AccountPass = Encrypt.Encryptor.Encrypt(AccountPass)
                Extra = None
                if len(Parameter) > 3:
                    Extra = Parameter[3]
                    Extra = Encrypt.Encryptor.Encrypt(Extra)
                Values = (AccountName, AccountUser, AccountPass, Extra)
                with sqlite3.connect("Data.db") as db:
                    cursor = db.cursor()
                    sql = """INSERT INTO {}(AccountName, AccountUsername, AccountPassword, Extra)
                                Values(?, ?, ?, ?)
                            """.format(self.GetUsername())
                    cursor.execute(sql, Values)
                print("Success")
            except:
                print("Error")
        elif Cmd == "cmds":
            print("'Show' 'All' Or '{Name Or Account Name}' -- Shows All Or Corresponding Accounts \n'Create' '{Name}' '{Account Username}' '{Account Password}' '{Extra}' -- Creates An Account With The Details \n'Back' -- Goes Back To Main App")

    def Social(self, Parameter):
        Parameter = Parameter.split(" ")
        Cmd = Parameter[0].lower()
        del Parameter[0]
        if Cmd == "friend":
            try:
                Username = Parameter[0]
                with sqlite3.connect("Data.db") as db:
                    cursor = db.cursor()
                    Values = (self.GetUserID, self.FindUserID(Username))
            except:
                print("Error")

    def Command(self, Parameter):
        Parameter = Parameter.split(" ")
        Cmd = Parameter[0].lower()
        del Parameter[0]
        if Cmd == "messaging":
            self.Messaging(Parameter)
        elif Cmd == "settings":
            self.Settings(Parameter)
        elif Cmd == "banking":
            self.Bank(Parameter)
        elif Cmd == "passmanager":
            self.PassManager(Parameter)
        elif Cmd == "social":
            self.Social(Parameter)
        elif Cmd == "cmds":
            print("'Cmds' -- Gives List Of All Commands \n'Message' -- Sends You To The Messaging App \n'Bank' -- Sends You To The Bank App \n'Settings' -- Sends You To Settings \n'Passmanager' -- Sends You To The Password Managing App \n'Exit' -- Exits App")