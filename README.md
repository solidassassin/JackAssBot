# JackAssBot

This bot is nothing more than a hobby to improve my Python skills overtime. As
long as this hobby doesn't get boring new features and improvements will
constantly be added as I get more fluent in Python.

## Who's it for

Initially this was created for our small server (just couldn't find a bot that
would fit our needs). At the beginning the goal was to try and make the bot as
offensive as possible (hence the name), but later was forgotten (might focus on
that in the future). Python's focus isn't speed, so don't expect this bot to be
the fastest out there, moreover speed was never considered when building it.

### As a result

- The bot doesn't handle exceeded API usage limits
- Permission checks are not very specific
- Management commands are almost non-existent
- Some features and commands might not be fully tested
- Not optimized for speed

If the mentioned downfalls aren't a problem for you, then you're more than
welcome to use an instance of my bot.

## Setup

All you need to do is to create a `config.py` file in the `data/` folder.
Here's an example of what it should look like:

```py
token = ''  # required
giphy = ''
google = ''
google_cx = ''
```

## Running

### Using Docker

The Docker installation is up to you. To build the image run
`docker build -t <name> <bot root directory>`. To run the container in detached
mode: `docker run -d <name>`.

### On The Host

`python-3.8+` and `discord.py-1.0.0+` are required for the
bot to run. Python's installation process will vary on the operating system you're
using (I'll leave that up to you). You might also need to install `git` depending
on your operating system. The required modules can be installed from
`requirements.txt` with `pip`.

```console
git clone https://github.com/solidassassin/JackAssBot.git
pip install -r requirements.txt
```

Then just run the `launch.py` script located in the `./data/` folder.

## Contributing

Anyone is free to create a pull request, reporting issues is also encouraged. I
usually value the idea way more than the implementation, but if possible please
follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines.
