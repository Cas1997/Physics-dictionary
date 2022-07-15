# Author: Casper van Veen
# Version v2

import json
import sys
from difflib import get_close_matches as gcm

class Dictionary:
    def __init__(self):
        self.file_name = "<YourPathHere>/PhysicsDictionary.json"
        self.data = json.load(open(self.file_name))
        self.tags = {"A":"Accelerator", "DE":"Detector & Experiments", "H":"Heavy Flavour", "P":"Photons", "L":"Leptons", "AM":"Anti-matter", "DM":"Dark Matter", "DC":"Detector Components", "CO":"CERN Office Terms", "I":"Institutes"}

    # Look for direct matches
    def direct_match(self, word):
        result = ""
        match = []
        close_match = False
        if(word in self.data):
            match.append(word)
        elif(word.lower() in self.data):
            match.append(word.lower())
        elif(word.title() in self.data):
            match.append(word.title())
        elif(word.upper() in self.data):
            match.append(word.upper())
        else:
            match = self.close_match(word)
            close_match = True

        return match, close_match

    # Look for close matches
    def close_match(self, word):
        thresh = 1.
        if(len(word) > 1):
            thresh = (len(word) - 1)/len(word) - 0.001

        match_found = False
        match = []
        # Close match attempt number 1
        match = gcm(word, self.data.keys(), cutoff = thresh)
        if(len(match) > 0):
            match_found = True
        # Close match attempt number 2
        if(not match_found):
            match = gcm(word.upper(), self.data.keys(), cutoff = thresh)
            if(len(match) > 0):
                match_found = True
        # Close match attempt number 3
        if(not match_found):
            match = gcm(word.title(), self.data.keys(), cutoff = thresh)
            if(len(match) > 0):
                match_found = True
        # Close match attempt number 4
        if(not match_found):
            match = gcm(word.lower(), self.data.keys(), cutoff = thresh)
            if(len(match) > 0):
                match_found = True

        return match

    # Print the result
    def find_result(self, word):
        print("Requested:", word)
        print("")
        match, close_match_bool = self.direct_match(word)
        if(len(match) > 0):
            if(close_match_bool):
                print("No direct match found. Trying close matches")
                print("")
            for i in match:
                if(close_match_bool):
                    print("Did you mean %s?" % i)
                result = self.data[i]
                if(len(result) > 1):
                    print("Found", len(result), "results")
                for j in result:
                    tag_string = ''
                    print("Description:", j[0])
                    tags = j[1].split(",")
                    if(not tags[0] == ''):
                        for k in tags:
                            tag_string = self.tags[k] + " "
                    print("Tags:", tag_string)
                    print("Link:", j[2])
                    print("")

        elif(len(match) == 0):
            print("This word does not exist in the dictionary yet.")
            print("Please add it when you find the definition.")

        return

    # Merge your file with the data file
    def merge(self, file):
        return

    def add(self, word, meaning):
        return


dict = Dictionary()

program = sys.argv[0]
arg1 = sys.argv[1]
arg2 = sys.argv[2]

if(arg1 == "what"):
    meaning = dict.find_result(arg2)
