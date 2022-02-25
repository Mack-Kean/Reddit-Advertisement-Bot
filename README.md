# Reddit-Advertisement-Bot
A bot designed to advertise a podcast on multiple subreddits.  Can be tweaked for any other kind of content promotion.
---

## Usage:
This bot requires a JSON file named 'data.json' to run.  The file must specify
`client_id`, `client_secret_key`, `user_agent`, `password`, and `username` properties in addition to
a `subreddits` property which contains an array of subreddits you would like the bot to post in.

### Warning:
According to the [reddit API Github wiki](https://github.com/reddit-archive/reddit/wiki/API) there is a limit of 60 OAuth requests per minute.  Thus,  more than 60 subreddits being added to the `subreddits` json could result in unexpected behaviour.  This has not yet been tested.

