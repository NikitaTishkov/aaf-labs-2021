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
        for command in parsed_commands:
            self.parse_command(command)

    def parse_command(self, command):
        """Recognize specific command and call it"""
        if command.split()[0].upper() == "CREATE":
            # call CREATE request
            self.request.CREATE(command.split()[1])
        elif command.split()[0].upper() == "INSERT":
            # call INSERT request
            doc_str = command[command.find('"') + 1:command.rfind('"')]
            self.request.INSERT(command.split()[1], doc_str)
        elif command.split()[0].upper() == "SEARCH":
            # call SEARCH request
            collection_name = command.split()[1]
            search_keywords = list()
            where_exist = False
            for i, word in enumerate(command.split()):
                if word == 'WHERE':
                    where_exist = True
                if where_exist and word != 'WHERE':
                    search_keywords.append(word)
            self.request.SEARCH(collection_name, search_keywords)
            print("SEARCH")
        elif command.split()[0].upper() == "PRINT_INDEX":
            # call PRINT_INDEX request
            self.request.PRINT_INDEX(command.split()[1])
        else:
            print("Wrong command, try again!")
            # TODO: Show commands info


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
            with open(collection_name + "/data.json", "w") as data_file:
                data = {}
                data_file.write(json.dumps(data))
        except OSError as error:
            print("Could not open/read file")
            print(error)
            # It is better to add file name to error log

        try:
            with open(collection_name + "/indexes.json", "w") as index_table_file:
                index_table_file.write('{}')
        except OSError as error:
            print("Could not open/read file")
            print(error)
            # It is better to add file name to error log
        
        try:
            doc_counter = {}
            if not Path("doc_counter.json").exists():
                with open("doc_counter.json", "w") as doc_counter_file:
                    doc_counter_file.write('{}')
            else: 
                with open("doc_counter.json", "r") as doc_counter_file:
                    doc_counter = json.loads(doc_counter_file.read())

            doc_counter.update({collection_name: 0})
            with open("doc_counter.json", "w") as doc_counter_file:
                doc_counter_file.write(json.dumps(doc_counter, indent=4))
        except OSError as error:
            print("Could not open/read file")
            print(error)
            # It is better to add file name to error log
        print(collection_name, " was successfully created!")

    def INSERT(self, collection_name, doc_str):
        """Insert document with value /doc_str/ 
        to collection /collection_name/"""
        index_table_file = open(collection_name + "/indexes.json", "r")
        index_table = json.loads(index_table_file.read())
        index_table_file.close()

        doc_counter_file = open("doc_counter.json", "r")
        doc_counter = json.loads(doc_counter_file.read())
        doc_counter_file.close()

        i = 0
        for word in doc_str.split():
            words_adr_list = list()
            docs_adr_dict = dict()
            word = word.lower()
            if index_table.get(word) is not None:
                docs_adr_dict = index_table.get(word)
                if index_table.get(word).get(doc_counter[collection_name]) is not None:
                    words_adr_list = index_table.get(word).get(doc_counter[collection_name])
            words_adr_list.append(i)
            docs_adr_dict.update({doc_counter[collection_name]: words_adr_list})
            index_table.update({word: docs_adr_dict})
            i = i + 1
        index_table_file = open(collection_name + "/indexes.json", "w")
        index_table_file.write(json.dumps(index_table, indent=4))
        index_table_file.close()

        data_file = open(collection_name + "/data.json", "r")
        data = json.loads(data_file.read())
        data.update({doc_counter[collection_name]: doc_str})
        data_file.close()
        with open(collection_name + "/data.json", "w") as data_file:
            data_file.write(json.dumps(data))
        doc_counter_file = open("doc_counter.json", "w")
        doc_counter.update({collection_name: doc_counter[collection_name] + 1})
        doc_counter_file.write(json.dumps(doc_counter, indent=4))
        doc_counter_file.close()
        print("Insertion was successfully done!")

    def PRINT_INDEX(self, collection_name):
        """Show word-indexes pairs for specific 
        collection /collection_name/"""
        index_table = None
        with open(collection_name + "/indexes.json", "r") as index_table_file:
            index_table = json.loads(index_table_file.read())
        for word in index_table.keys():
            print(word + ":\n")
            for doc in index_table[word].keys():
                print("   d" + doc + " -> " + str(index_table[word][doc]))

    def SEARCH(self, collection_name, search_keywords):
        """Full text search in specific
        collection /collection_name/"""
        if len(search_keywords) == 3 and search_keywords[1] == '-':
            search_keywords.pop(1)
            self.search_in_range(collection_name, search_keywords)
        elif len(search_keywords) == 3 and search_keywords[1][0] == '<':
            self.search_by_distance(collection_name, search_keywords)
        elif len(search_keywords) == 2 and search_keywords[1] == '*':
            search_keywords.pop(1)
            self.search_by_part_of_word(collection_name, search_keywords)
        elif len(search_keywords) == 1:
            self.search_by_single_word(collection_name, search_keywords)
        else:
            print("Incorrect attributes for WHERE")

    def search_by_single_word(self, collection_name, search_keyword):
        keyword = search_keyword[0]
        keyword = keyword[keyword.find('"') + 1:keyword.rfind('"')]
        index_table = None
        data = None
        with open(collection_name + '/indexes.json', 'r') as index_table_file:
            index_table = json.loads(index_table_file.read())
        with open(collection_name + '/data.json') as data_file:
            data = json.loads(data_file.read())
        searching_word = index_table.get(keyword, None)
        if searching_word is not None:
            for doc_id in searching_word.keys():
                print(data[doc_id])

    def search_in_range(self, collection_name, search_keywords):
        print(search_keywords)

    def search_by_distance(self, collection_name, search_keywords):
        print(search_keywords)

    def search_by_part_of_word(self, collection_name, part_of_word):
        print(part_of_word)


def info_global():
    print("Collection of text documents with full-text search. ")
    print("Our program allows you to search for words in several documents at once. "
          "The program analyzes the documents that are attached to the collections,"
          " selects individual words from them and saves a list of items where the word occurs within the document.")
    print("This can be convenient for accountants because they have a lot of documents that need to be processed.")
    print("This program has four commands that will help the user to use:")
    print("CREATE collection_name; - creating a new collection called collection_name.")
    print("INSERT collection_name “value”; - adding a new document to the collection collection_name.")
    print("PRINT_INDEX collection_name; - display of the internal structure of the inverted index built for the "
          "collection collection_name.")
    print("SEARCH collection_name [WHERE query]; - search for documents in the collection collection_name.")


def main():
    # Example:
    controller = Controller()
    s = 'SEARCH col1 WHERE "to"'
    controller.parse_code(s)


if __name__ == '__main__':
    main()
    
    