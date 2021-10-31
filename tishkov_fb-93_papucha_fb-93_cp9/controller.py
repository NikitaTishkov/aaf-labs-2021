# -*- coding: utf-8 -*-
import os
import json
class Controller:
    def __init__(self):
        self.request = Request()

    def info_command(self, command):
        """Show information about all commands 
        or about specific one """
        if command == "CREATE":
            print("CREATE - creating a new collection")
            print("Example:")
            print("CREATE wiki_articles; ")
        elif command == "INSERT":
            print("INSERT - add a new document to the collection")
            print("Example:")
            print("INSERT wiki_articles “The word 'algorithm' has its roots in Latinizing the ... ”;")
        elif command == "SEARCH":
            print("SEARCH - search for documents in the collection")
            print("Example:")
            print("SEARCH wiki_articles;")
            print("SEARCH wiki_articles WHERE “algorithm”; ('algorithm')")
            print("SEARCH wiki_articles WHERE “haa” - “haz”; (has)")
            print("SEARCH wiki_articles WHERE “has” <2> “roots”; (its)")
        elif command == "PRINT_INDEX":
            print("PRINT_INDEX - display of the internal structure of the inverted index built for the collection")
            print("Example:")
            print("PRINT_INDEX collection_name;")
            print("The output will be of this type:")
            print("word:")
            print("document->[word position numbers")
            print("be:")
            print("d1 -> [2, 6]")
        elif command == "ALL":
            self.info_command("CREATE")
            self.info_command("INSERT")
            self.info_command("SEARCH")
            self.info_command("PRINT_INDEX")

    def parse_code(self, text):
        """Splits string into commands and parse them"""
        parsed_commands = text.split("; ")
        #print(parsed_commands)
        for command in parsed_commands:
            self.parse_command(command)
        

    def parse_command(self, command):
        """Recognize specific command and call it"""
        if command.split()[0].upper() == "CREATE":
            #call CREATE request
            self.request.CREATE(command.split()[1])
        elif command.split()[0].upper() == "INSERT":
            #TODO: call INSERT request
            print("INSERT")
        elif command.split()[0].upper() == "SEARCH":
            #TODO: call SEARCH request
            print("SEARCH")
        elif command.split()[0].upper() == "PRINT_INDEX":
            #TODO: call PRINT_INDEX request
            print("PRINT_INDEX")
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
        #TODO: Complete functionality
    def SEARCH(self, collection_name):
        """Full text search in specific 
        collection /collection_name/"""
        #TODO: Complete functionality

    def PRINT_INDEX(self, collection_name):
        """Show word-indexes pairs for specific 
        collection /collection_name/"""
        #TODO: Complete functionality
        pass

def info_global():
    """Show app descrition 
    (The goal and the basic instructions)"""
    #TODO: Add full description for application
    pass

def main():
    #Example:
    controller = Controller()
    s = input()
    controller.parse_code(s)

if __name__ == '__main__':
    main()
    
    