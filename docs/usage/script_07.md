# **Video** to **Podcast** Generation

## Use Case

You have a video recording and you want to generate a podcast video from just the video using `audim`.

## Script

!!! warning "🚧"
    We don't have a single standalone script for this,
    and it won't be possible until we have an automatic speaker identification from `audim`.

You can use the following series of actions to achieve this:

1. Use [script 04](./script_04.md) to extract the audio from the video
2. Use [script 01](./script_01.md) to generate a subtitle file
3. Manually identify the speakers with help from [script 08](./script_08.md)
4. Replace the speaker names with the names you identified using [script 10](./script_10.md)
5. Use [script 02](./script_02.md) to generate a podcast video
