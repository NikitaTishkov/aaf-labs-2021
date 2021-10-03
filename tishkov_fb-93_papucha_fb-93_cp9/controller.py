import os
import json
class Controller:
    def __init__(self):
        self.request = Request()

    def info_command(self, command):
        """Show information about all commands 
        or about specific one """
        if command == "CREATE":
            #TODO: Write CREATE command description
            #print(description)
            print("CREATE")
        elif command == "INSERT":
            #TODO: Write INSERT command description
            print()
        elif command == "SELECT":
            #TODO: Write SELECT command description
            print()
        elif command == "ALL":
            print()
            #TODO: Show all commands description 
            # Maybe it`s better to use recursion
            # e.g. info_command("CREATE")
            #      info_command("INSERT") ...

    def parse_command(self, command):
        """Recognize specific command and call it"""
        if command.split()[0] == "CREATE":
            #call CREATE request
            self.request.CREATE(command.split()[1])
        elif command.split()[0] == "INSERT":
            #TODO: call INSERT request
            print()
        elif command.split()[0] == "SELECT":
            #TODO: call SELECT request
            print()
        else:
            print("Wrong command, try again!")
            #TODO: Show commands info
         
class Request:

    def __init__(self):
        self.doc_counter = 0

    def CREATE(self, collection_name):
        """Create collection 
        with name /collection_name/ for docs"""

        try:
            os.mkdir("./" + collection_name)
        except OSError as error:
            print("Error! This collection already exist")
            print(error)
            # It is better to add file name to error log

        try:
            data_file = open(collection_name + "/data.txt", "w") 
            data_file.write("collection_name: " + collection_name)
            data_file.close()
        except OSError as error:
            print("Could not open/read file")
            print(error)
            # It is better to add file name to error log

        try:
            index_table = open(collection_name + "/indexes.json", "w")
            # Add first description fields to json file
            #TODO: Verify this solution with teacher
            index_table.close()
        except OSError as error:
            print("Could not open/read file")
            print(error)
            # It is better to add file name to error log
        self.doc_counter = self.doc_counter + 1
        print(collection_name, " was succesfully created!")

    def INSERT(self, collection_name, doc_str):
        """Insert document with value /doc_str/ 
        to collection /collection_name/"""

    def SELECT(self):
        #TODO: Complete functionality
        print()

def info_global():
    """Show app descrition 
    (The goal and the basic instructions)"""
    #TODO: Add full description for application
    print("HEllo!")

def main():
    #Example:
    controller = Controller()
    com = input()
    print(com)
    controller.parse_command(com)
        

if __name__ == '__main__':
    main()