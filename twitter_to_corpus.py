#!/usr/bin/env python3

# Converts one or more Twitter archives into a combined corpus. This script
#  performs no filtering.
#
# Copyright 2016 Mathew Hunter

import argparse
import json
import nltk
import re
import zipfile


# Processes the referenced archives to produce a corpus
def generate_corpus(archive_filenames):

    # Process each archive, extracting words from it
    corpus_words = []
    tokenizer = nltk.tokenize.TweetTokenizer(preserve_case=False, strip_handles=True)
    for archive_filename in archive_filenames:

        # Pull the words from the archive
        try:
            archive_words = __extract_words_from_twitter_archive(archive_filename, tokenizer)
            corpus_words.extend(archive_words)
        except Exception as e:
            print("There was an error extracting words from the archive '" + archive_filename + "': " + str(e))
            raise

    return corpus_words


# Pulls words from a Twitter archive
def __extract_words_from_twitter_archive(archive_filename, tokenizer):

    # Open the archive and extract words from the content files within
    corpus_words = []
    with zipfile.ZipFile(archive_filename) as archive:

        # Pull the Tweet content file names
        content_files = []
        try:
            content_files = [name for name in archive.namelist() if re.match("data/js/tweets/.*", name)]
        except Exception as e:
            print("There was an error reading the archive: " + str(e))
            raise

        # Check if there are content files to process
        if (len(content_files) < 1):
            print("No data to process")
            exit -1

        # Process each file, dumping the words from each content file into the list
        for content_file in content_files:
            with archive.open(content_file) as file:

                # Pull the raw data for the file
                raw_string_data = str(file.read(), "utf-8")
                string_data = raw_string_data[raw_string_data.index("["):]

                # Pull the words
                content_words = __extract_words_from_twitter_content(string_data, tokenizer)
                corpus_words.extend(content_words)

    return corpus_words


# Pulls words from Twitter content represented by JSON
def __extract_words_from_twitter_content(string_data, tokenizer):

    # Load the JSON data as a collection of Tweet objects
    tweets = []
    try:
        tweets = json.loads(string_data)
    except Exception as e:
        print("There was an error decoding the JSON content: " + str(e))
        raise

    # Process each Tweet, pulling words from the text content
    content_words = []
    for tweet in tweets:

        # Tokenize the Tweet content and add found tokens
        tokens = tokenizer.tokenize(tweet["text"])
        content_words.extend(tokens)

    return content_words



if __name__ == "__main__":

    # Create an argument parser
    parser = argparse.ArgumentParser(description="Unwraps one or more Twitter archives to produce a body of text")
    parser.add_argument("source_file", nargs="+", help="the source file(s) to process")

    # Parse the arguments and pull pertinent args
    args = parser.parse_args()
    archive_filenames = args.source_file

    # Produce a corpus and output it
    corpus_words = generate_corpus(archive_filenames)
    print(" ".join(corpus_words))
