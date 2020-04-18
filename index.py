from getpass import getpass
import requests
from firebase import firebase
import pyrebase
import hashlib
import os
from os import path


# Initializing the app
config = {
  "apiKey": "apiKey",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://databaseName.firebaseio.com",
  "storageBucket": "projectId.appspot.com"
}


# Generating email hash 
def generate_hash(username):
    user_hash = hashlib.sha256(username.encode()).hexdigest()
    return user_hash


# Creating new folder with the key name
def create_folder():
    name = input('\nEnter your full name : ')
    email = input('Enter your email id : ')
    contact = input('Enter your contact number : ')
    data = {
        'Name': name,
        'Email': email,
        'Contact': contact
    }
    username = generate_hash(email)
    print('\n YOUR KEY IS %s' % username)
    print('\n Please save it securely, you will need it.')
    message = db.child("users").child(username).set(data)
    storage.child(username)
    print('\nFolder created Successfully.')

    return message


# Uploading file 
def upload_file():
    user_hash = input('Enter your key\t')
    path_local = input('Enter your image local storage path\t')
    filename = os.path.basename(path_local)
    path_cloud = path.join(user_hash, filename)
    message = storage.child(path_cloud).put(path_local)
    print('\n Image Uploaded Successfully.')
    return message


# Downloading file
def download_file():
    user_hash = input('Enter your key\t')
    stored_as = input('File stored as\t')
    save_as = input('Save as\t')
    path_cloud = path.join(user_hash, user_hash, stored_as)
    message = storage.child(path_cloud).download(save_as)
    print('\n File Downloaded Successfully.')
    return message



def main():
    print('\n\n------------------------- Firebase Data Entry ----------------------------\n\n')

    print('Hello user, what would you like to do?')
    user_input = input(
        '1. Create New Folder \n2. Upload File \n3. Download File \n4. Exit\n\nInput\t')
    if user_input == str(1):
        message = create_folder()
        print(message)
        main()
    elif user_input == str(2):
        message = upload_file()
        print(message)
        main()
    elif user_input == str(3):
        message = download_file()
        print(message)
        main()
    elif user_input == str(4):
        print('\n Bye! See you soon.')
        exit(0)
    else:
        val = input('Opes! wrong entry. Would you like to try again?(y/n)')
        if val == 'y' or val == 'Y':
            main()
        else:
            print('\n Bye! See you soon.')
            exit(0)


def user_signup():
    print('\n SIGN UP')
    email = input('Enter your email  ')
    password = input('enter your password  ')
    password2 = getpass('Re-enter your password  ')
    if password == password2:
        try:
            auth.create_user_with_email_and_password(email, password)
            auth.sign_in_with_email_and_password(email, password)
            print('\n\t Sign-In Successful!\n\t Please check your email and verify the account.')
        except requests.exceptions.HTTPError:
            print('\n** User Already Exists with this email id. Please try again with new email.')
            user_input = input('\n Forgot Password?(y/n)\t')
            if user_input == 'y' or user_input == 'Y':
                email = input('Enter your email  ')
                auth.send_password_reset_email(
                    "\nWe just sent a password reset request to %s. Please check your email." % email)
                user_signin()
            user_signup()
    else:
        print('\n** Password does not match. Try Again.')
        user_signup()


def user_signin():
    print('\n Log-IN')
    email = input('Enter your email  ')
    password = getpass('enter your password  ')
    try:
        auth.sign_in_with_email_and_password(email, password)
        print('\n\t Log-In Successful!\n')
    except requests.exceptions.HTTPError:
        print('\n** Account does not exists.')
        user_signup()


if __name__ == '__main__':
    print('-------------------------------------------------------------------------')
    firebase = firebase.FirebaseApplication('https://projectId.firebaseio.com/', None)
    fbase = pyrebase.initialize_app(config)
    auth = fbase.auth()
    db = fbase.database()
    storage = fbase.storage()

    user_input = input('Do you have an account?(y/n)\t')
    if user_input == 'y' or user_input == 'Y':
        user_signin()
        main()
    else:
        user_signup()
        main()
