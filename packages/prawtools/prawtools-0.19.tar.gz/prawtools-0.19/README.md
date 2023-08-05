# BBOE's PRAWtools

PRAWtools is a collection of tools that utilize reddit's API through
[PRAW](https://praw.readthedocs.org/). PRAWtools is currently made up of three
utillities:

* modutils
* reddit_alert
* subreddit_stats

## PRAWtools Installation

### Ubuntu/debian installation

    sudo apt-get install python-setuptools
    sudo easy_install pip
    sudo pip install prawtools

### Arch Linux installation
    sudo pacman -S python-pip
    sudo easy_install pip
    sudo pip install prawtools

### Mac OS X installation (only tested with Lion)

    sudo easy_install pip
    sudo pip install prawtools


## modutils

modutils is a tool to assist reddit community moderators in moderating
their community. At present, it is mostly useful for automatically building
flair templates from existing user flair, however, it can also be used to
quickly list banned users, contributors, and moderators.

### modutils examples

Note: all examples require you to be a moderator for the subreddit

0. List banned users for subreddit __foo__

        modutils -l banned foo

0. Get current flair for subreddit __bar__

        modutils -f bar

0. Synchronize flair templates with existing flair for subreddit __baz__,
building non-editable templates for any flair whose flair-text is common among
at least 2 users.

        modutils --sync --ignore-css --limit=2 baz

0. Send a message to approved submitters of subreddit __blah__. You will be
prompted for the message, and asked to verify prior to sending the messages.

        modutils --message contributors --subject "The message subject" blah


## reddit_alert

reddit_alert will notify you when certain keywords are used in comments. For
instance, to be notified whenever your username is mentioned you might run it
as:

    reddit_alert bboe

You can receive multiple alerts by specifying multiple keywords separated by
spaces. If you want to be alerted for keyphrases (those containing spaces) you
must put quotes around the term:

    reddit_alert bboe praw "reddit api"

By default reddit_alert will only provide links to the same terminal screen (or
command prompt) it's running in. To be notified via a reddit message specify
the `-m USER` option:

    reddit_alert -m bboe bboe praw "reddit_api"

When using the `-m USER` you will be prompted to login.

By default comments from __all__ subreddits are considered. If you want to
restrict the notifications to only a few subreddits use one or more `-s
SUBREDDIT` options:

    reddit_alert -m bboe -s redditdev -s learnpython bboe praw "reddit_api"

Finally, you may want to ignore notifications from certain users. You can use
the `-I USER` option to ignore comments from a certain user:

    reddit_alert -m bboe -I bizarrobboe bboe

To see a complete set of available options run:

    reddit_alert --help


## subreddit_stats

subreddit_stats is a tool to provide basic statistics on a subreddit.
To see the what sort of output subreddit stats generates check out
[/r/subreddit_stats](http://www.reddit.com/r/subreddit_stats).

The tool will only analyze up to 1,000 submissions.


### subreddit_stats examples

0. Generate stats for subreddit __foo__ for the last 30 days with extra
verbose output. Post results to subreddit __bar__ as user __user__.

        subreddit_stats -d30 -vv -R bar -u user foo
        
 The -d30 flag will get all submissions from the last 30 days, but will ignore the 
last three days. As a result, you may experience messages like "No submissions 
found". To analyze one month, try:

        subreddit_stats -tmonth -vv -R bar -u user foo
        
 Similarly, to analyze one year:

        subreddit_stats -tyear -vv -R bar -u user foo

0. Generate stats for subreddit __blah__ for the top posts of the year. Post
the results to the same subreddit as user __resu__.

        subreddit_stats --top year -u resu blah

0. To see other possible options

        subreddit_stats --help
