#!/usr/bin/env python3

# Reads one or more Twitter archives, building and filtering a corpus, and then
#  generating a wordcloud image.
#
# Copyright 2016 Mathew Hunter

import twitter_to_corpus
import filter_corpus
import corpus_to_wordcloud

import argparse
import os
import PIL


if __name__ == "__main__":

    # Create an argument parser and parse the args
    parser = argparse.ArgumentParser(description="Reads the Twitter archive from the specified files, building a wordcloud")
    parser.add_argument("source_file", nargs="+", help="the source file(s) to process")
    parser.add_argument("--width", nargs="?", type=int, help="the width of the output image", default=400)
    parser.add_argument("--height", nargs="?", type=int, help="the height of the output image", default=300)
    args = parser.parse_args()

    # Produce a corpus
    corpus = twitter_to_corpus.generate_corpus(args.source_file)

    # Filter it
    filtered_corpus = filter_corpus.filter_corpus_words(corpus)

    # Generate a wordcloud image
    image = corpus_to_wordcloud.generate_image_from_words(filtered_corpus, args.width, args.height)

    # Output the file
    output_filename = os.path.dirname(os.path.realpath(__file__)) + "test.png"
    image.to_file(output_filename)

    # Show the image
    image = PIL.Image.open(output_filename)
    image.show()
