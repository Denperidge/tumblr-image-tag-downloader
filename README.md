# Tumblr-Tagged-Image-Collector

A single file CLI script to collect all images from a Tumblr blog with a specific tag.
Outputs JSON, includes image descriptions if the reblog chain has one.
```
[
    {
        "image_url": "https://64.media.tumblr.com/name.jpg",
        "post_url": "https://www.tumblr.com/blog/view/blog/postid",
        "alt": "Image description: A description from a reblog"
    }
]
```

## How-to
### Usage
```bash
wget https://raw.githubusercontent.com/Denperidge/tumblr-tagged-image-collector/main/ttic.py
python ttic.py --blog blogname --api-key APIKEY --tag tagname
```

### Get an API key
Go to [https://www.tumblr.com/oauth/register](https://www.tumblr.com/oauth/register)
Example input:
- Application Name: `Tumblr Tagged Image Collector`
- Application Website: `https://github.com/Denperidge/tumblr-tagged-image-collector`
- Application Description: `Local instance of TITD`
- Default callback URL: `https://example.com`  (This is unused, but required)
- OAuth2 redirect URLS: `https://example.com`  (This is also unused, but also required)

After this, copy your `OAuth Consumer Key`, and pass it using `--api-key KEY` or `-a KEY`
