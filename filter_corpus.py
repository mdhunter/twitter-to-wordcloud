#!/usr/bin/env python3

# Filters one or more input text files, building a collection of words from
#  the corpora, and filtering them
#
# Copyright 2016 Mathew Hunter

import argparse
import nltk
import os
import re

# default regex that filters out links, numbers, and single characters
default_regex = "^(?!http|\d)\w{2,}"


# Filters the specified corpus
def filter_corpus_data(string_data, stopwords=[], use_nltk_default=True):

    # Tokenize and get the words
    tokenizer = nltk.tokenize.TweetTokenizer(preserve_case=False, strip_handles=True)
    tokens = tokenizer.tokenize(string_data)

    # Filter
    filtered_words = filter_corpus_words(tokens, stopwords, use_nltk_default)

    return " ".join(filtered_words)


# Filters the referenced files to produce a filtered corpus
def filter_corpus_files(filenames, stopwords=[], use_nltk_default=True):

    # Process each file, filtering the data from it
    filtered_corpus = ""
    for filename in filenames:

        # Read and filter the content from each
        try:
            with open(filename, "r") as file:
                raw_data = str(file.read())
                filtered_data = filter_corpus_data(raw_data, stopwords=stopwords, use_nltk_default=use_nltk_default)
                filtered_corpus += " " + filtered_data
            file = open(filename, "r")

        except Exception as e:
            print("There was an error filtering the data from '" + filename + "': " + str(e))
            raise

    return filtered_corpus


# Filters the corpus words
def filter_corpus_words(words, stopwords=[], use_nltk_default=True):

    stopwords_set = set(stopwords)
    if use_nltk_default:
        stopwords_set |= set(nltk.corpus.stopwords.words("english"))

    filtered_words = [word for word in words if word not in stopwords_set and re.match(default_regex, word)]

    return filtered_words


# Loads a set of stopwords from a file
def __load_stopwords_from_file(file):

    stopwords = set()
    with open(file, "r") as file:
        for line in file:
            if line.strip():
                stopwords.add(line.strip())

    return stopwords



if __name__ == "__main__":

    # Create an argument parser and parse the args
    parser = argparse.ArgumentParser(description="Filters the incoming corpus, removing stopwords")
    parser.add_argument("source_file", nargs="+", help="the source file(s) to process")
    parser.add_argument("--stopwords", type=str, help="a file that contains custom stopwords")
    args = parser.parse_args()

    # If there was a custom stopwords file specified, load it
    stopwords = []
    custom_stopwords_file = args.stopwords
    if custom_stopwords_file:
        stopwords = __load_stopwords_from_file(custom_stopwords_file)

    # Filter the corpus files
    filtered_corpus = filter_corpus_files(args.source_file, stopwords=stopwords)
    print(filtered_corpus)
