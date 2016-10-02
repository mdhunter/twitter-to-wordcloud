
import argparse
import json
import nltk
import os
import PIL
import pprint
import re
import wordcloud
import zipfile


# Pulls the words from a given content file
def extractWords(stringData, tokenizer, stopwords):

    # Process the string data into tweet objects and process them
    contentWords = []
    tweets = json.loads(stringData)
    for tweet in tweets:

        # Pull words from the text
        tweetTokens = tokenizer.tokenize(tweet["text"])
        tweetWords = [word for word in tweetTokens if re.match("^(?!http|\d)\w+", word) and word not in stopwords]
        contentWords.extend(tweetWords)

    return contentWords


# Processes the referenced archives to produce a corpus
def processArchives(archiveFilename):

    # Unzip the archive to a temporary directory and process it
    with zipfile.ZipFile(archiveFilename) as archive:

        # Pull the tweet content file names
        contentFiles = []
        try:
            contentFiles = [name for name in archive.namelist() if re.match("data/js/tweets/.*", name)]
        except:
            print("There was an error reading the archive.")

        if (len(contentFiles) < 1):
            print("No data to process")
            exit -1

        # Process each file, dumping the words from each tweet into the list
        words = []
        stopwords = nltk.corpus.stopwords.words("english")
        tokenizer = nltk.tokenize.TweetTokenizer(preserve_case=False, strip_handles=True)
        for contentFile in contentFiles:
            with archive.open(contentFile) as file:

                # Pull the raw data for the file
                rawStringData = str(file.read(), "utf-8")
                stringData = rawStringData[rawStringData.index("["):]

                # Pull the words
                words.extend(extractWords(stringData, tokenizer, stopwords))

        # Output the corpus
        return " ".join(words)

def generateCloud(corpus):

    # Generate a word cloud image
    cloudImage = wordcloud.WordCloud().generate(corpus)

    return cloudImage


if __name__ == "__main__":

    # Create an argument parser
    parser = argparse.ArgumentParser(description="Unwraps a Twitter archive to produce a body of text")
    parser.add_argument("source_file", help="the source file to process")

    # Parse the arguments and pull pertinent args
    args = parser.parse_args()
    archiveFilename = args.source_file

    # Produce a corpus
    corpus = processArchives(archiveFilename)

    # Produce a wordcloud
    cloudImage = generateCloud(corpus)

    # Output the file
    outputFilename = os.path.realpath(__file__) + "test.png"
    cloudImage.to_file(outputFilename)

    # Show the image
    image = PIL.Image.open(outputFilename)
    image.show()
