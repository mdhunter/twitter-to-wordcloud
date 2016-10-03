# twitter-to-wordcloud
A quick tool to generate a word cloud from a Twitter archive.


## Motivation
A fair time ago, one of the fads on Twitter was to use the [Twitter Word Cloud Bot](https://github.com/defacto133/twitter-wordcloud-bot) to generate word clouds from a user's timeline. Simply at-mention the bot, and it would scan through the referring user's timeline as the source for the word cloud corpus. Although I wanted to generate a word cloud for my timeline, my preference for a private account at the time precluded this.

At the time, I then went through the process of downloading my Tweet archive, compiling the Tweet data into a single file, and filtered it down using Unix command-line tools, finally using [Wordle](http://www.wordle.net/) to generate the final image. This was unfortunately very time-consuming.

So, for the longest time, I've wanted to automate this process, to generate images aperiodically, to see how my language usage changes. Developing this fun little tool was also a motivation to deepen my razor-thin knowledge of Python.


## Installation

1. Ensure that Python 3 is installed.
1. Clone the repository
1. Install the requirements:<br/>
```sudo pip3 install -r requirements```
1. Install the NLTK stopwords corpus:<br/>
```python3 -m nltk.downloader stopwords```

## Running

1. Pull down your Twitter archive. See [this Twitter support article](https://support.twitter.com/articles/20170160) for more information.
1. Run the twitter_to_wordcloud script with your archive:<br/>
```python3 twitter_to_wordcloud archive.zip```



## Author/Copyright

Copyright 2016, Mathew Hunter
