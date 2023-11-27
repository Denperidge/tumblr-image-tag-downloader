"""
Tumblr-Image-Tag-Downloader

Requirments:
- Python 3
- Tumblr API key (https://www.tumblr.com/docs/en/api/v2#what-you-need)
- This script

Usage: python titd.py -b staff -a APIKEY  
"""

# Imports
from os import makedirs
from argparse import ArgumentParser
from re import compile, RegexFlag

from json import loads, dump
from urllib.request import urlopen

# Regex
REGEX_IMAGES = compile(r"(?<=src=\").*?(?=\")")
REGEX_IMAGE_DESCRIPTION = compile(r"(?<=\[)Im.*?(?=\])", RegexFlag.IGNORECASE)

# Functions
def setup_cli():
    argparse = ArgumentParser(prog="tumblr-image-downloader")
    argparse.add_argument("--blog", "-b", required=True, help="Blog name. Example input: staff")
    argparse.add_argument("--api-key", "-a", "-ak", required=True, help="Tumblr API key")
    argparse.add_argument("--tag", "-t", required=True, help="Tag to download")
    return argparse.parse_args()



# Main
if __name__ == "__main__":
    args = setup_cli()

    request_url = "https://api.tumblr.com/v2/blog/" \
        + args.blog \
        + "/posts" \
        + "?api_key=" + args.api_key \
        + "&tag=" + args.tag
        
    print(f"[TITD] Sending request to {request_url}")

    with urlopen(request_url) as req:
        all_posts = loads(req.read())["response"]["posts"]
    
    images = []

    for post in all_posts:
        # Get the short_url to link back
        post_url: str = post["post_url"]
        # Get the post with all reblogs to extract the image & image id
        trail: str = post["trail"]

        post_images = []
        post_image_descriptions = []

        print(f"[TITD] Processing {post_url}")

        for post_part in trail:
            post_part_content = post_part["content"]

            post_images += REGEX_IMAGES.findall(post_part_content)
            post_image_descriptions += REGEX_IMAGE_DESCRIPTION.findall(post_part_content)


        for i in range(len(post_images)):
            image = dict({
                "image_url": post_images[i],
                "post_url": post_url
            })
            try:
                image["alt"] = post_image_descriptions[i]
            except IndexError:
                print("No alt text for " + image["image_url"])

            images.append(image)
        
    with open("output.json", "w") as output:
        print(f"[TITD] Saving output...")
        dump(images, output)

    print(f"[TITD] Done!")
    