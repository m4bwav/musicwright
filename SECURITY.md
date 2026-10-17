# Security policy

## Reporting a problem

Open an issue or a pull request and I'll take a look. A pull request with the fix is the quickest route.

You can also report privately: open the repository's **Security** tab and choose **Report a vulnerability**.

This is a one-person project with no bug bounty and no response deadline. I'll reply when I can and say what I plan to do. Good-faith testing on your own copy is welcome.

## Supported versions

Only the latest release on the default branch gets fixes.

## Scope

The skills' instructions and scripts run on your machine with your agent's permissions. `mw.py` runs ffmpeg and ffprobe on audio and video files you give it, sends generation graphs and requests to ComfyUI or ACE-Step REST hosts you configure and downloads the audio they return, and writes verdicts and notes to a studio folder in your home directory. In scope: anything that leads the agent to run commands, write files, fetch URLs or send data beyond what the skill says it does. That includes instructions planted in an audio file's tags, a downloaded workflow, a host's response, lyrics or a web page the skill reads (prompt injection), and any path by which an input file or a host's reply could make mw.py run code or write outside the folders it was given. Out of scope: bugs in the agent tool itself (Claude Code, Copilot, Codex, Cursor), in ffmpeg, ComfyUI, ACE-Step, librosa, hosted music services or DAW and notation MCP servers; report those to their makers.
