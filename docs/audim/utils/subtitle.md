# Subtitle

The `Subtitle` is an utility class that is used to handle and modify subtitle files.

It is used to handle the output subtitle files from `aud2sub` before feeding them to `sub2pod` for video generation.

List of utilities provided by the `Subtitle` class:

- `replace_speakers`: Replace the audim speaker tags (names) in the subtitle file with new ones
- `preview_replacement`: Preview the changes from `replace_speakers` in CLI without modifying the file
- more to come...

Below is the API documentation for the `Subtitle` utility:

::: audim.utils.subtitle
