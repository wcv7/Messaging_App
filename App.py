import Data
import Commands
import os
Data.Initialise()

def Message(Exit):
    while Exit != True:
        UserInput = input("Messaging >")
        if UserInput.lower() == "back":
            break
        elif UserInput.lower() == "clear":
            os.system("cls")
        else:
            FinalCommand = "Messaging " + UserInput
            CurrentUser.Command(FinalCommand)

def Bank(Exit):
    while Exit != True:
        UserInput = input("Bank >")
        if UserInput.lower() == "back":
            break
        elif UserInput.lower() == "clear":
            os.system("cls")
        else:
            FinalCommand = "Banking " + UserInput
            CurrentUser.Command(FinalCommand)

def Main(Exit):
    print("Use 'cmds' For Commands")
    UserCommands = Commands.Commands()
    UserCommands.Initialise(CurrentUser.UserID)
    while Exit != True:
        UserInput = input(">")
        if UserInput.lower() == "message":
            Message(Exit)
        elif UserInput.lower() == "clear":
            os.system("cls")
        elif UserInput.lower() == "bank":
            Bank(Exit)
        elif UserInput.lower() == "logout":
            Login(Exit)
        elif UserInput.lower() == "exit":
            Exit = True
        else:
            CurrentUser.Command(UserInput)

def Login(Exit):
    FieldInput = input("Enter Your Username Or Email: ")
    if FieldInput.lower() == "signup":
        SignUp(Exit)
    PasswordInput = input("Enter Your Password: ")
    if CurrentUser.Login(FieldInput, PasswordInput):
        Main(Exit)
    else:
        print("Incorrect Username Or Password!")
        Login(Exit)

def SignUp(Exit):
    FNInput = input("Enter Your Firstname: ")
    if FNInput.lower() == "login":
        Login(Exit)
    LNInput = input("Enter Your Lastname:  ")
    UserInput = input("Enter A Username: ")
    if CurrentUser.SearchUser(UserInput):
        print("Username Already Exists!")
        SignUp(Exit)
    else:
        EmailInput = input("Enter Your Email: ")
        PassInput = input("Enter A Password: ")
        if CurrentUser.SignUp(FNInput, LNInput, UserInput, EmailInput, PassInput):
            Login(Exit)



if __name__ == "__main__":
    Exit = False
    CurrentUser = Data.User()
    UserInput = input("Do You Have An Account (Y/N)? ")
    if UserInput == "Y" or UserInput == "":
        Login(Exit)
    else:
        SignUp(Exit)