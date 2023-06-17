# :construction: youtube-to-frontmatter

## Goals

This script is to help get metadata out of YouTube Channels and Playlists. It's a WIP, but can be immediately useful.

## Usage

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

## Contributing

PRs are welcome at <https://github.com/jefftriplett/youtube-to-frontmatter>.

Linting should be verified by running `just lint`. There are currently no tests, so `just test` is expected to fail.

In addition to the development supporting packages that will be installed by `just`, you may need to install the following:

- [just](https://github.com/casey/just#installation)
- [pre-commit](https://pre-commit.com/) `pip install pre-commit`

## Contact / Social Media

Here are a few ways to keep up with me online. If you have a question about this project, please consider opening a GitHub Issue.

[![](https://jefftriplett.com/assets/images/social/github.png)](https://github.com/jefftriplett)
[![](https://jefftriplett.com/assets/images/social/globe.png)](https://jefftriplett.com/)
[![](https://jefftriplett.com/assets/images/social/twitter.png)](https://twitter.com/webology)
[![](https://jefftriplett.com/assets/images/social/docker.png)](https://hub.docker.com/u/jefftriplett/)
