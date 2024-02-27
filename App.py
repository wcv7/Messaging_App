import Data
import Commands
import os
Data.Initialise()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def Message():
    while True:
        UserInput = input("Messaging >")
        if UserInput.lower() == "back":
            cls()
            break
        elif UserInput.lower() == "clear":
            cls()
        else:
            FinalCommand = "Messaging " + UserInput
            CurrentUser.Command(FinalCommand)

def Bank():
    while True:
        UserInput = input("Bank >")
        if UserInput.lower() == "back":
            cls()
            break
        elif UserInput.lower() == "clear":
            cls()
        else:
            FinalCommand = "Banking " + UserInput
            CurrentUser.Command(FinalCommand)

def PassManager():
    while True:
        UserInput = input("PassManager >")
        if UserInput.lower() == "back":
            cls()
            break
        elif UserInput.lower() == "clear":
            cls()
        else:
            FinalCommand = "PassManager " + UserInput
            CurrentUser.Command(FinalCommand)
            
def Settings():
    passverify = input("Please Verify Your Password: ")
    if CurrentUser.CheckPassword(passverify, CurrentUser.GetUserID()):
        cls()
        while True:
            UserInput = input("Settings >")
            if UserInput.lower() == "back":
                cls()
                break
            elif UserInput.lower() == "clear":
                cls()
            else:
                FinalCommand = "Settings " + UserInput
                CurrentUser.Command(FinalCommand)
    elif passverify == "back":
        exit
    else:
        print("Wrong Password!")

def Main():
    cls()
    print("Use 'cmds' For Commands")
    UserCommands = Commands.Commands()
    UserCommands.Initialise(CurrentUser.UserID)
    while True:
        UserInput = input(">")
        if UserInput.lower() == "message":
            cls()
            Message()
        elif UserInput.lower() == "settings":
            cls()
            Settings()
        elif UserInput.lower() == "clear":
            cls()
        elif UserInput.lower() == "bank":
            cls()
            Bank()
        elif UserInput.lower() == "passmanager":
            cls()
            PassManager()
        elif UserInput.lower() == "logout":
            cls()
            Login()
        elif UserInput.lower() == "exit":
            exit()
        else:
            CurrentUser.Command(UserInput)

def Login():
    FieldInput = input("Enter Your Username Or Email: ")
    if FieldInput.lower() == "signup":
        SignUp()
    PasswordInput = input("Enter Your Password: ")
    if CurrentUser.Login(FieldInput, PasswordInput):
        cls()
        Main()
    else:
        print("Incorrect Username Or Password!")
        Login()

def SignUp():
    FNInput = input("Enter Your Firstname: ")
    if FNInput.lower() == "login":
        cls()
        Login()
    LNInput = input("Enter Your Lastname:  ")
    UserInput = input("Enter A Username: ")
    if CurrentUser.SearchUser(UserInput):
        print("Username Already Exists!")
        cls()
        SignUp()
    else:
        EmailInput = input("Enter Your Email: ")
        PassInput = input("Enter A Password: ")
        if CurrentUser.SignUp(FNInput, LNInput, UserInput, EmailInput, PassInput):
            cls()
            Login()

if __name__ == "__main__":
    CurrentUser = Data.User()
    UserInput = input("Do You Have An Account (Y/N)? ")
    if UserInput == "Y" or UserInput == "":
        Login()
    else:
        SignUp()