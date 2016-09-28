# AP DEJA-VU
[That strange feeling we sometimes get that we've lived through something before.](https://www.youtube.com/watch?v=G2eUopy9sd8)

`ap-deja-vu` is a small web service that will replay JSON from an AP election test. `ap-deja-vu` does not require a database for persistence and does not write to the filesystem.

## Important Note
`ap-deja-vu` requires that you have **already recorded** an AP election test to JSON files. [Elex](http://elex.readthedocs.org/en/latest/recording.html#flat-files) is highly recommended for this process.

Contact your AP support representative to get an up-to-date schedule for election tests. Typically, they occur on Wednesdays and Fridays between 11am and noon EST.

## User interface
![screen shot 2016-01-29 at 1 04 07 pm](https://cloud.githubusercontent.com/assets/109988/12683723/d2134152-c688-11e5-8ac1-9c65a2a3c33a.png)

## Getting Started
#### Install requirements

Note: Requires a running redis instance on localhost. Install with homebrew (development on a Mac) or via apt-get (production use on an Ubuntu-based server).

##### Mac
Note: Requires (Homebrew)[].
```
brew install redis
brew services start redis
```

##### Ubuntu Linux
```
Sudo apt-get install redis-server
```

#### Install this app

```bash
mkvirtualenv ap-deja-vu && git clone git@github.com:newsdev/ap-deja-vu.git && cd ap-deja-vu
pip install -r requirements.txt
add2virtualenv ap_deja_vu
```

#### Run The Server
```bash
python -m ap_deja_vu.app
```

## How It Works

#### Environment Variables

Export an `AP_DEJAVU_DATA_DIRECTORY` environment variable.

```
export AP_DEJAVU_DATA_DIRECTORY=/tmp/ap-elex-data/
```

#### AP Elections Files

Your data directory should contain a series of folders corresponding to AP election dates. Within each of those folders, `ap-deja-vu` expects a series of files, named as UNIX timestamps. Really, any incrementing number or letter combination will work as long as the default sort produces the correct order. Each of these files should contain the output of the AP election API v2. Use this layout as a guide:

```bash
/tmp/
    /ap-elex-data/
        /2016-02-01/
                /local/
                    001.json
                    002.json
                    003.json
                /national/
                    001.json
                    002.json
                    003.json
        /2016-02-09/
                /local/
                    001.json
                    002.json
                    003.json
                /national/
                    001.json
                    002.json
                    003.json
```

*Note*: This software assumes you have two AP API keys; one for national data, and one for local data.

We recommend The New York Times's [Elex-loader](https://github.com/newsdev/elex-loader/) for capturing and parsing AP election data. Pay particular attention to [the `get_national_results` and `get_local_results` functions in this script](https://github.com/newsdev/elex-loader/blob/master/scripts/stg/_results.sh). 

#### Playback

The route `/<election_date>` will replay the election files found in the folder
`/<DATA_DIR>/<election_date>/`. The files should be named such that the first file
will be sorted first in a list by `glob.glob()`, e.g., a higher letter (a) or lower
number (0). Incrementing UNIX timestamps (such as those captured by Elex) would be
ideal.

This route takes two optional control parameters. Once these have been passed to set
up an election test, the raw URL will obey the instructions below until the last
file in the hopper has been reached.

* `position` will return the file at this position in the hopper. So, for example,
`position=0` would set the pointer to the the first file in the hopper and return it.

* `playback` will increment the position by itself until it is reset. So, for example, 
`playback=5` would skip to every fifth file in the hopper.

When the last file in the hopper has been reached, it will be returned until the Flask
app is restarted OR a new pair of control parameters are passed.

Example: Let's say you would like to test an election at 10x speed. You have 109
files in your `/<DATA_DIR>/<election_date>/` folder named 001.json through 109.json

* Request 1: `/<election_date>?position=0&playback=10&national=true` > 001.json
* Request 2: `/<election_date>?national=true` > 011.json
* Request 3: `/<election_date>?national=true` > 021.json
* Request 4: `/<election_date>?national=true` > 031.json
* Request 5: `/<election_date>?national=true` > 041.json
* Request 6: `/<election_date>?national=true` > 051.json
* Request 7: `/<election_date>?national=true` > 061.json
* Request 8: `/<election_date>?national=true` > 071.json
* Request 9: `/<election_date>?national=true` > 081.json
* Request 10: `/<election_date>?national=true` > 091.json
* Request 11: `/<election_date>?national=true` > 101.json
* Request 12: `/<election_date>?national=true` > 109.json
* Request 13 - ???: `/<election_date>?national=true` > 109.json

Requesting /<election_date>?position=0&playback=1&national=true will reset to the default position
and playback speeds, respectively.

#### Status

The route /<election_date>/status will return the status of a given
election date test, including the current position in the hopper, the
playback speed, and the path of the file that will be served at the current
position.

```javascript
{
    position: 22,
    playback: 1,
    file: "/tmp/ap-elex-data/2016-02-09/ap_elections_loader_recording-1449676507.json"
}
```