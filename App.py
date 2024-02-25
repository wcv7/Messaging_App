import Data
import Commands
import os
Data.Initialise()

def Message():
    while True:
        UserInput = input("Messaging >")
        if UserInput.lower() == "back":
            os.system("cls")
            break
        elif UserInput.lower() == "clear":
            os.system("cls")
        else:
            FinalCommand = "Messaging " + UserInput
            CurrentUser.Command(FinalCommand)

def Bank():
    while True:
        UserInput = input("Bank >")
        if UserInput.lower() == "back":
            os.system("cls")
            break
        elif UserInput.lower() == "clear":
            os.system("cls")
        else:
            FinalCommand = "Banking " + UserInput
            CurrentUser.Command(FinalCommand)
            
def Settings():
    passverify = input("Please Verify Your Password: ")
    if CurrentUser.CheckPassword(passverify, CurrentUser.GetUserID()):
        os.system("cls")
        while True:
            UserInput = input("Settings >")
            if UserInput.lower() == "back":
                os.system("cls")
                break
            elif UserInput.lower() == "clear":
                os.system("cls")
            else:
                FinalCommand = "Settings " + UserInput
                CurrentUser.Command(FinalCommand)
    elif passverify == "back":
        exit
    else:
        print("Wrong Password!")

def Main():
    os.system("cls")
    print("Use 'cmds' For Commands")
    UserCommands = Commands.Commands()
    UserCommands.Initialise(CurrentUser.UserID)
    while True:
        UserInput = input(">")
        if UserInput.lower() == "message":
            os.system("cls")
            Message()
        elif UserInput.lower() == "settings":
            os.system("cls")
            Settings()
        elif UserInput.lower() == "clear":
            os.system("cls")
        elif UserInput.lower() == "bank":
            os.system("cls")
            Bank()
        elif UserInput.lower() == "logout":
            os.system("cls")
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
        os.system("cls")
        Main()
    else:
        print("Incorrect Username Or Password!")
        Login()

def SignUp():
    FNInput = input("Enter Your Firstname: ")
    if FNInput.lower() == "login":
        os.system("cls")
        Login()
    LNInput = input("Enter Your Lastname:  ")
    UserInput = input("Enter A Username: ")
    if CurrentUser.SearchUser(UserInput):
        print("Username Already Exists!")
        os.system("cls")
        SignUp()
    else:
        EmailInput = input("Enter Your Email: ")
        PassInput = input("Enter A Password: ")
        if CurrentUser.SignUp(FNInput, LNInput, UserInput, EmailInput, PassInput):
            os.system("cls")
            Login()

if __name__ == "__main__":
    CurrentUser = Data.User()
    UserInput = input("Do You Have An Account (Y/N)? ")
    if UserInput == "Y" or UserInput == "":
        Login()
    else:
        SignUp()