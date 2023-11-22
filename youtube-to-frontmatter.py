"""
----------------------------------------------------------------------------
Author: Jeff Triplett <https://github.com/jefftriplett>
Copyright (c) 2023 - Jeff Triplett
License: PolyForm Noncommercial License 1.0.0 - https://polyformproject.org/licenses/noncommercial/1.0.0/
----------------------------------------------------------------------------

1. To extract video URLs, titles, and descriptions from a YouTube playlist using Python, you can use the google-api-python-client library. Here's a step-by-step guide on how to do this:

  Install the google-api-python-client library:

```shell
pip install google-api-python-client environs pydantic python-frontmatter python-slugify rich typer
```

2. Get an API key for the YouTube Data API:
  - Go to the Google Cloud Console: https://console.cloud.google.com/
  - Create a new project or select an existing one.
  - Click on "Enable APIs and Services" and search for "YouTube Data API v3".
  - Click "Enable" to enable the API for your project.
  - Click "Create credentials" and follow the steps to get an API key.

3. To use it:

```shell
export YOUTUBE_API_KEY=YOUR-API-KEY-HERE

python youtube-to-frontmatter.py --playlist=PL2NFhrDSOxgUoF-4F2MdAFvOK1wOrNdqB
```

"""

import frontmatter
import googleapiclient.discovery
import os
import typer

from environs import Env
from pathlib import Path
from pydantic import BaseModel
from rich import print
from slugify import slugify
from typing import Optional


__version__ = "2023.6.1"


env = Env()

YOUTUBE_API_KEY: str = env.str("YOUTUBE_API_KEY")


class VideoModel(BaseModel):
    """
    Our base class for our default "Video" fields.
    """

    title: str
    slug: Optional[str] = None
    url: Optional[str]
    year: Optional[int] = None

    class Config:
        extra = "allow"

    def __init__(self, **data):
        super().__init__(**data)

        # if slugs are blank default them to slugify(name)
        if not self.slug:
            self.slug = slugify(self.title)


def get_channel_videos(*, channel_id: str, max_results: int = 50):
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=YOUTUBE_API_KEY
    )

    request = youtube.search().list(
        part="snippet", channelId=channel_id, maxResults=max_results, type="video"
    )
    videos = []

    while request:
        response = request.execute()
        for item in response["items"]:
            video = {
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
            }
            videos.append(video)

        request = youtube.search().list_next(request, response)

    return videos


def get_playlist_videos(
    *,
    playlist_id: str,
    max_results: int = 50,
):
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=YOUTUBE_API_KEY
    )

    request = youtube.playlistItems().list(
        part="snippet", maxResults=max_results, playlistId=playlist_id
    )
    videos = []

    while request:
        response = request.execute()
        for item in response["items"]:
            video = {
                "url": f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}",
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
            }
            videos.append(video)

        request = youtube.playlistItems().list_next(request, response)

    return videos


def main(
    channel_id: Optional[str] = typer.Option(None, "--channel"),
    max_results: Optional[int] = typer.Option(100, "--max"),
    playlist_id: Optional[str] = typer.Option(None, "--playlist"),
    year: Optional[int] = 2023,
):
    if channel_id and playlist_id:
        print("You can't specify both a channel and a playlist.")
        raise typer.Exit(code=1)

    if channel_id:
        videos = get_channel_videos(channel_id=channel_id, max_results=max_results)

    elif playlist_id:
        videos = get_playlist_videos(playlist_id=playlist_id, max_results=max_results)

    else:
        print("You need to specify a channel or a playlist.")
        raise typer.Exit(code=1)

    save_videos(videos, year)


def save_videos(videos, year: int):
    output_folder = Path(f"{year}")
    if not output_folder.exists():
        output_folder.mkdir()

    for video in videos:
        description = video.pop("description")
        data = VideoModel(**video)
        data.year = year
        post = frontmatter.loads(description)
        post.metadata.update(data.model_dump(exclude_unset=True))
        output_folder.joinpath(f"{data.slug}.md").write_text(
            frontmatter.dumps(post) + os.linesep
        )


if __name__ == "__main__":
    typer.run(main)
