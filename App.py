import Data
import Commands
Data.Initialise()

def Message(Exit):
    while Exit != True:
        UserInput = input("Messaging >")
        if UserInput.lower() == "back":
            break
        else:
            FinalCommand = "Messaging " + UserInput
            CurrentUser.Command(FinalCommand)

def Bank(Exit):
    while Exit != True:
        UserInput = input("Bank >")
        if UserInput.lower() == "back":
            break
        else:
            FinalCommand = "Banking " + UserInput
            CurrentUser.Command(FinalCommand)

def Main(Exit):
    UserCommands = Commands.Commands()
    UserCommands.Initialise(CurrentUser.UserID)
    while Exit != True:
        UserInput = input(">")
        if UserInput.lower() == "message":
            Message()
        elif UserInput.lower() == "bank":
            Bank()
        elif UserInput.lower() == "exit":
            Exit = True
        else:
            CurrentUser.Command(UserInput)

def Login(Exit):
    FieldInput = input("Enter Your Username Or Email: ")
    PasswordInput = input("Enter Your Password: ")
    if CurrentUser.Login(FieldInput, PasswordInput):
        Main(Exit)
    else:
        print("Incorrect Username Or Password!")
        Login(Exit)

def SignUp(Exit):
    FNInput = input("Enter Your Firstname: ")
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