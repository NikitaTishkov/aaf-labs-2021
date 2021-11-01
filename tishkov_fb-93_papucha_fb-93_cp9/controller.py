# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
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
        if text[-1] == ';':
            text = text[:text.rfind(';')]
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
            doc_str = command[command.find('"') + 1:command.rfind('"') - 1]
            self.request.INSERT(command.split()[1], doc_str)
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
        pass

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
            index_table_file = open(collection_name + "/indexes.json", "w")
            index_table = '{}'
            index_table_file.write(index_table)
            index_table_file.close()
        except OSError as error:
            print("Could not open/read file")
            print(error)
            # It is better to add file name to error log
        
        try:
            doc_counter = {}
            if not Path("doc_counter.json").exists():
                doc_counter_file = open("doc_counter.json", "w")
                doc_counter_file.write('{}')
                doc_counter_file.close()
            else: 
                doc_counter_file = open("doc_counter.json", "r")
                doc_counter = json.loads(doc_counter_file.read())
                doc_counter_file.close()
            doc_counter.update({collection_name: 0})
            doc_counter_file = open("doc_counter.json", "w")
            doc_counter_file.write(json.dumps(doc_counter, indent=4))
            doc_counter_file.close()
        except OSError as error:
            print("Could not open/read file")
            print(error)
            # It is better to add file name to error log
        print(collection_name, " was succesfully created!")

    def INSERT(self, collection_name, doc_str):
        """Insert document with value /doc_str/ 
        to collection /collection_name/"""
        #TODO: Complete functionality
        index_table_file = open(collection_name + "/indexes.json", "r")
        index_table = json.loads(index_table_file.read())
        index_table_file.close()

        doc_counter_file = open("doc_counter.json", "r")
        doc_counter = json.loads(doc_counter_file.read())
        doc_counter_file.close()

        i = 0
        for word in doc_str.split():
            words_addr_list = []
            if index_table.get(word) != None:
                if index_table.get(word).get(doc_counter[collection_name]) != None:
                    words_addr_list = index_table.get(word).get(doc_counter[collection_name])
            words_addr_list.append(i)
            index_table.update({word: {doc_counter[collection_name]:words_addr_list}})
            i = i + 1
        index_table_file = open(collection_name + "/indexes.json", "w")
        index_table_file.write(json.dumps(index_table, indent=4))
        index_table_file.close()
        data_file = open(collection_name + "/data.txt", "a")
        data_file.write("\n\n\ndoc #" + str(doc_counter[collection_name]) + ":\n" + doc_str)
        doc_counter_file = open("doc_counter.json", "w")
        doc_counter.update({collection_name: doc_counter[collection_name] + 1})
        doc_counter_file.write(json.dumps(doc_counter, indent=4))
        doc_counter_file.close()

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
    print("Collection of text documents with full-text search./n Our program allows you to search for words in several documents at once. The program analyzes the documents that are attached to the collections, selects individual words from them and saves a list of items where the word occurs within the document./n This can be convenient for accountants because they have a lot of documents that need to be processed./n This program has four commands that will help the user to use:/n CREATE collection_name; - creating a new collection called collection_name./n INSERT collection_name “value”; - adding a new document to the collection collection_name./n PRINT_INDEX collection_name; - display of the internal structure of the inverted index built for the collection collection_name./n SEARCH collection_name [WHERE query]; - search for documents in the collection collection_name.")

def main():
    #Example:
    controller = Controller()
    s = input()
    controller.parse_code(s)

if __name__ == '__main__':
    main()
    
    