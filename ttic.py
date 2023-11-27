"""
Tumblr-Tagged-Image-Collector

Requirments:
- Python 3
- Tumblr API key (https://www.tumblr.com/docs/en/api/v2#what-you-need)
- This script

Usage: python ttic.py -b staff -a APIKEY  
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
    argparse.add_argument("--output", "-o", default="output.json", help="File to save output to")
    return argparse.parse_args()

def create_request_url(blogname: str, api_key: str, tag: str):
    return "https://api.tumblr.com/v2/blog/" \
        + blogname \
        + "/posts" \
        + "?api_key=" + api_key \
        + "&tag=" + tag

def get_posts(blogname: str, api_key: str, tag: str):
    request_url = create_request_url(blogname, api_key, tag)
    print(f"[TTIC] Sending request to {request_url}")
    with urlopen(request_url) as req:
        posts = loads(req.read())["response"]["posts"]
    return posts 


def parse_post(post_object):
    # Get the short_url to link back
    post_url: str = post_object["post_url"]
    # Get the post with all reblogs to extract the image & image id
    trail: str = post_object["trail"]

    print(f"[TTIC] Processing {post_url}")

    post_images = []

    # All images in any parts of the post
    post_image_urls = []
    # All image descriptiosn in any parts of the post
    post_image_descriptions = []

    # Process every part
    for post_part in trail:
        post_part_content = post_part["content"]

        post_image_urls += REGEX_IMAGES.findall(post_part_content)
        post_image_descriptions += REGEX_IMAGE_DESCRIPTION.findall(post_part_content)
    
    # After finding all image urls & description, transform that data into a json object & add it to post_images
    for i in range(len(post_image_urls)):
        image = dict({
            "image_url": post_image_urls[i],
            "post_url": post_url
        })
        try:
            image["alt"] = post_image_descriptions[i]
        except IndexError:
           print("No alt text for " + image["image_url"])
        
        post_images.append(image)
    
    # Return post_images
    return post_images

def save_output_json(filename: str, images: list):
    with open(filename, "w", encoding="UTF-8") as output:
        print(f"[TTIC] Saving output...")
        dump(images, output)
    
# Main
if __name__ == "__main__":
    args = setup_cli()

    all_post_objects = get_posts(args.blog, args.api_key, args.tag)

    images = []

    for post_object in all_post_objects:
        images += parse_post(post_object)

    save_output_json(args.output, images)


    print(f"[TTIC] Done!")
