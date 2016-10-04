#!/usr/bin/env python3

# Analyzes one or more input text files, building a collection of words from
#  the corpora, and getting the most frequently used words.
#
# Copyright 2016 Mathew Hunter

import argparse
import nltk
import os


# Reads the referenced files to produce analysis
def analyze_corpus_data(filenames, count=25):

    # Process each file, building up a full corpus to analyze
    corpus_words = []
    tokenizer = nltk.tokenize.TweetTokenizer(preserve_case=False, strip_handles=True)
    for filename in filenames:

        # Read and filter the content from each
        try:
            with open(filename, "r") as file:
                raw_data = str(file.read())
                tokens = tokenizer.tokenize(raw_data)
                corpus_words.extend(tokens)
            file = open(filename, "r")

        except Exception as e:
            print("There was an error filtering the data from '" + filename + "': " + str(e))
            raise

    # Run a frequency distribution
    dist = nltk.probability.FreqDist(corpus_words)

    print(dist.most_common(count))



if __name__ == "__main__":

    # Create an argument parser and parse the args
    parser = argparse.ArgumentParser(description="Analyzes the incoming corpus, getting the most common words")
    parser.add_argument("source_file", nargs="+", help="the source file(s) to process")
    parser.add_argument("--word_count", nargs="?", type=int, help="the number of words to return", default=25)
    args = parser.parse_args()

    # Filter the corpus files
    filtered_corpus = analyze_corpus_data(args.source_file, args.word_count)
