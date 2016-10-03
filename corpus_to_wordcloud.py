#!/usr/bin/env python3

# Reads one or more text files, building a corpus, and generating a wordcloud
#  image.
#
# Copyright 2016 Mathew Hunter

import argparse
import json
import nltk
import os
import PIL
import pprint
import re
import wordcloud
import zipfile


# Generates an image from a collection of words
def generate_image_from_words(words):

    # Generate a word cloud image
    image = wordcloud.WordCloud().generate(words)

    return image


# Reads the referenced files to produce a collection of words
def __read_corpus_data(filenames):

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
            print("There was an error reading the data from '" + filename + "': " + str(e))
            raise

    return corpus_words



if __name__ == "__main__":

    # Create an argument parser and parse the args
    parser = argparse.ArgumentParser(description="Reads the incoming corpus from the specified files, building a wordcloud")
    parser.add_argument("source_file", nargs="+", help="the source file(s) to process")
    args = parser.parse_args()

    # Produce a corpus
    words = __read_corpus_data(args.source_file)

    # Produce a wordcloud
    image = generate_image_from_words(" ".join(words))

    # Output the file
    output_filename = os.path.dirname(os.path.realpath(__file__)) + "test.png"
    image.to_file(output_filename)

    # Show the image
    image = PIL.Image.open(output_filename)
    image.show()
