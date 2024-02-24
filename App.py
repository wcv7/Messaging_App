import Data
import Commands
Data.Initialise()
Exit = False

def Main():
    UserCommands = Commands.Commands()
    UserCommands.Initialise(CurrentUser.UserID)
    while Exit != True:
        UserInput = input(">")
        CurrentUser.Command(UserInput)

def Login():
    FieldInput = input("Enter Your Username Or Email: ")
    PasswordInput = input("Enter Your Password: ")
    if CurrentUser.Login(FieldInput, PasswordInput):
        Main()
    else:
        print("Incorrect Username Or Password!")
        Login()

def SignUp():
    FNInput = input("Enter Your Firstname: ")
    LNInput = input("Enter Your Lastname:  ")
    UserInput = input("Enter A Username: ")
    if CurrentUser.SearchUser(UserInput):
        print("Username Already Exists!")
        SignUp()
    else:
        EmailInput = input("Enter Your Email: ")
        PassInput = input("Enter A Password: ")
        if CurrentUser.SignUp(FNInput, LNInput, UserInput, EmailInput, PassInput):
            Login()



if __name__ == "__main__":
    CurrentUser = Data.User()
    UserInput = input("Do You Have An Account (Y/N)? ")
    if UserInput == "Y" or UserInput == "":
        Login()
    else:
        SignUp()