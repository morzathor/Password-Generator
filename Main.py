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

######## get the last index (ID) ########
def retrieve_index():
    return list(collection.find())

######## Password generator function ########
def passwd_generator(length):
    r = range(0,length)
    password = ''

    for i in r:
        password += random.choice(all)
    return password
######## Save generated password details in MongoDB ########

def save_document():
    if not retrieve_index():
      last_id = 1
    else:
      last_id = retrieve_index()[-1]['the_id'] + 1

    ask_service = input("Enter your desired service: ")
    ask_email = input("Enter associated email / username: ")
    ask_length = int(input("Enter your desired length: "))
    the_time = time.strftime('%H:%M - %Y/%m/%d')

    the_pass = passwd_generator(ask_length)
    the_document = {
        "the_id":last_id,
        "Service": ask_service.strip(),
        "Email/Username": ask_email.strip(),
        "Password": the_pass,
        "Generated time and date": the_time
    }
    collection.insert_one(the_document)
    return the_pass

######## Retrive generated passwords from MongoDB ########

def retrive_document():
    if not list(collection.find()):
        print("Nothing show.")
    else:
        for i in list(collection.find()):
            print(f"\nID: {i['the_id']}"
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

######## Regenerate a service's password ########

def regenerate(user_id,use_length):
    e = list(collection.find())
    for i in e:
        if i['the_id'] == user_id :
            print(i['the_id'])
            new_pass = passwd_generator(use_length)
            collection.update_one({'the_id':user_id},{'$set':{'Password':new_pass}})
            return new_pass

######## Main Function ########
def main():
    while True:
        main_menu = int(input("""Welcome to Python password generator\n
        1.Generate a password
        2.List all generated passwords
        3.Re-generate password
        4.Delete all documents
        5.Exit
        Choose an option: """))
        if main_menu == 1:
            result = save_document()
            print(f"Success!\nYour generated password is: {result}")
            input("\nPress enter to continue...\n")
            continue
        elif main_menu == 2:
            retrive_document()
            input("\nPress enter to continue...\n")
            continue
        elif main_menu == 3:
            while True:
                try:
                    us_id = int(input("select desired service by ID: "))
                except ValueError:
                    print("Please enter a valid number (just number) !")            
                    continue
                break
            if not list(collection.find()):
                print("No service added")
                input("\nPress enter to continue...\n")
                continue
            else:
                try:
                    us_length = int(input("Enter desired length: "))
                except ValueError:
                    print("Please enter a valid number (just number) !")
                reg_result = regenerate(us_id,us_length)
                if reg_result == None:
                    print("\nInvalid ID !")
                    input("\nPress enter to continue...\n")
                else:
                    print(f"\nYour new regenrated password is: {reg_result}")
                    input("\nPress enter to continue...\n")
                    continue

        elif main_menu == 4:
            delete_documents()
            input("\nPress enter to continue...\n")
            continue
        elif main_menu == 5:
            break
main()