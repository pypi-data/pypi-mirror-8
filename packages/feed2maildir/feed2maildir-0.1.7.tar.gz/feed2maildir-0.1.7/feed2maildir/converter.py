import datetime
import json
import os
import sys

# Python 2.x compabitlity
if sys.version[0] == '2':
    FileNotFoundError = IOError

TEMPLATE = """MIME-Version: 1.0
Date: {}
Subject: [{}] {}
From: {}

[Feed2Maildir] Read the update here:
{}

{}
"""

class Converter:
    """Compares the already parsed feeds and converts new ones to maildir"""

    def __init__(self, feeds, db='~/.f2mdb', maildir='~/mail/feeds',
                 silent=False):
        self.silent = silent
        self.feeds = feeds
        self.maildir = os.path.expanduser(maildir)

        try: # to read the database
            with open(os.path.expanduser(db), 'r') as f:
                self.db = json.loads(f.read())
        except FileNotFoundError:
            self.db = None
        except ValueError:
            self.output('WARNING: database is malformed and will be ignored')
            self.db = None

        inval = []
        for feed, content in self.feeds.items():
            try: # to validate the feeds, access some essential keys
                content['feed']['title']
                content['feed']['link']
                content['feed']['updated']
            except:
                self.output('WARNING: feed {} seems to be broken'.format(feed))
                inval.append(feed)
        for i in inval: # pop invalid feeds
            self.feeds.pop(i)

    def writeout(self):
        """Check which updates need to be written to the maildir"""
        if not os.access(self.maildir, os.W_OK):
            try: # to make the maildir
                os.mkdir(self.maildir)
                os.mkdir('{}/tmp'.format(self.maildir))
                os.mkdir('{}/new'.format(self.maildir))
                os.mkdir('{}/cur'.format(self.maildir))
            except:
                sys.exit('ERROR: accessing "{}" failed'.format(self.maildir))

        for feed, content in self.feeds.items():
            try:
                pubdate = self.mktime(self.db[feed]['feed']['updated'])
            except:
                pubdate = None
            for entry in content['entries']:
                if not self.db or self.mktime(entry['published']) > pubdate:
                    mail = TEMPLATE.format(entry['published'],
                    entry['author'], entry['title'], feed, entry['link'],
                    entry['description'])
                    self.write(mail)

    def write(self, message):
        """Take a message and write it to a mail"""
        dt = str(datetime.datetime.now())
        pid = str(os.getpid())
        host = os.uname()[1]
        name = '{}/new/{}{}{}'.format(self.maildir, dt, pid, host)
        try: # to write out the message
            with open(name, 'w', encoding='utf-8') as f:
                f.write(message)
        except:
            self.output('WARNING: failed to write message to file')

    def mktime(self, arg):
        """Make a datetime object from a time string"""
        return datetime.datetime.strptime(arg, '%a, %d %b %Y %H:%M:%S %Z')

    def output(self, arg):
        if not self.silent:
            print(arg)

