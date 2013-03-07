#!/usr/bin/env python

"""
    Export JSON results from Sentimentron into a CSV for easy analysis.

    Instructions:
        Submit request at http://sentimentron.co.uk
        Upon redirect to results, note the identifier
            i.e. http://results.sentimentron.co.uk/#<id>
        Run this script with the identifier at the end
            i.e. python csv_export.py <id>
"""


import csv 
import os
import requests 
import sys

from datetime import datetime

def main():
    
    # Process arguments
    result_identifier = None
    for i in sys.argv:
        result_identifier = i
    
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Convert identifier
    result_identifier = int(result_identifier)
    
    # Open output file
    ofn = "%d.csv" % (result_identifier)
    if os.path.exists(ofn):
        if not "--overwrite" in sys.argv:
            while 1:
                response = raw_input("Output file '%s' already exists. Overwrite? (y/n) " % (ofn,))
                response = response.upper()
                if response == "Y":
                    overwrite = True 
                    break
                elif response == "N":
                    overwrite = False
                    break 
        else:
            overwrite = True 
        if not overwrite:
            sys.exit(0)
            
    wtr = csv.writer(open(ofn,'w'))
    wtr.writerow(["site", "date method", "date", "pos_phrases", 
        "neg_phrases", "pos_sentences", "neg_sentences", 
        "relevant_pos", "relevant_neg", "label", 
        "phrase_prob", "_id"]
    )

    
    # Form request URL
    url = "http://results.sentimentron.co.uk/results/%d" % (result_identifier, )
    
    # Execute request
    r = requests.get(url)
    
    # Extract JSON
    body = r.json()
    docs = body['siteData']
    
    for site in docs:
        for doc in docs[site]['docs']:
            method, date, pos_phrases, neg_phrases, pos_sentences, neg_sentences, relevant_pos, relevant_neg, label, phrase_prob, _id = doc
            date = datetime.fromtimestamp(date / 1000) # Correct for Javascript
            date = date.strftime(date_format)
            wtr.writerow([site, method, date, pos_phrases, neg_phrases, pos_sentences, neg_sentences, relevant_pos, relevant_neg, label, phrase_prob, _id])
    
if __name__ == "__main__":
    main()