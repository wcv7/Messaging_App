import sqlite3

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
        except:
            return False
        
    def SearchUser(self, Username):
        try:
            Values = (Username,)
            with sqlite3.connect("Data.db") as db:
                cursor = db.cursor()
                sql = """SELECT Username FROM User
                        WHERE Username = ?;
                    """
                cursor.execute(sql, Values)
                result, = cursor.fetchone()
                if result == Username:
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
                return True
        except:
            return False


    def SignUp(self, FName, LName, Username, Email, Password):
        if self.CreateAccount(FName, LName, Username, Email, Password):
            return True
        else:
            return False