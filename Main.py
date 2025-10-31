import pymongo
import random
import time

######## Connection Configurations ########
uri = "mongodb://localhost:27017/"
client = pymongo.MongoClient(uri)
database = client["PasswordDB"]
collection = database["Password-Collection"]
######## Existing Characters ########

all = 'abcdefghijklmnopqrstuvwxyz1234567890!@#^&*'

######## Save generated password details in MongoDB ########

def save_document():
    ask_service = input("Enter your desired service for this password: ")
    ask_email = input("Enter associated email / username: ")
    ask_length = int(input("Enter your desired length for password: "))
    the_time = time.strftime('%H:%M - %Y/%m/%d')
    r = range(0,ask_length)
    password = ''

    for i in r:
        password += random.choice(all)

    the_document = {
        "Service": ask_service.strip(),
        "Email/Username": ask_email.strip(),
        "Password": password,
        "Generated time and date": the_time
    }
    collection.insert_one(the_document)
    return password

######## Retrive generated passwords from MongoDB ########

def retrive_document():
    if not list(collection.find()):
        print("Nothing show.")
    else:
        for i in list(collection.find()):
            print(
                f"\nService: {i['Service']}\nEmail / Username: {i['Email/Username']}\n"
                f"Password: {i['Password']}\nTime added: {i['Generated time and date']}\n"+ ("-" * 32)
                )

######## Delete all existing records ########

def delete_documents():
    if not list(collection.find()):
        print ("Nothing to delete \\'_'/")
    else:
        for i in list(collection.find()):
            collection.delete_many(i)

######## Main Function ########

def main():
    main_menu = int(input("""Welcome to Python password generator\n
    1.Generate a password
    2.List all generated passwords
    3.Delete all documents
    Choose an option: """))
    if main_menu == 1:
        result = save_document()
        print(f"Success!\nYour generated password is: {result}")
    elif main_menu == 2:
        retrive_document()
    elif main_menu == 3:
        delete_documents()

main()