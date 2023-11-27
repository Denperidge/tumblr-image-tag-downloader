# Tumblr-Image-Tag-Downloader

A single file CLI script to download all images from a Tumblr blog with a specific tag.
Outputs JSON, includes image descriptions if the reblog chain has one.

## How-to
## Usage
```bash
git clone https://github.com/Denperidge/tumblr-image-tag-downloader.git
cd tumblr-image-tag-downloader
titd.py --blog blogname --api-key APIKEY --tag tagname
```

### Get an API key
Go to [https://www.tumblr.com/oauth/register](https://www.tumblr.com/oauth/register)
Example input:
- Application Name: `Tumblr Image Tag Downloader`
- Application Website: `https://github.com/Denperidge/tumblr-image-tag-downloader`
- Application Description: `Local instance of TITD`
- Default callback URL: `https://github.com/Denperidge/tumblr-image-tag-downloader`
- OAuth2 redirect URLS: `https://github.com/Denperidge/tumblr-image-tag-downloader`

After this, copy your `OAuth Consumer Key`, and pass it using `--api-key KEY` or `-a KEY`
