# ffmpeg recipes

Verified with ffmpeg 9.0.1 on Windows on 2026-10-17 unless marked. mw.py wraps most of them;
these are for one-offs and for reading what mw.py does.

```bash
# loudness summary only
ffmpeg -hide_banner -nostats -i in.wav -af ebur128=peak=true:framelog=verbose -f null - 2>&1 | grep -E "^\s+(I|LRA|Peak):"

# two-pass normalise (pass 1 prints JSON; paste its values into pass 2)
ffmpeg -hide_banner -nostats -i in.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null -
ffmpeg -y -i in.wav -af loudnorm=I=-14:TP=-1:LRA=11:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true:print_format=summary -ar 48000 -c:a pcm_s24le out.wav

# strip leading and trailing silence, short fade in, fade out
ffmpeg -y -i in.wav -af "silenceremove=start_periods=1:start_threshold=-60dB,areverse,silenceremove=start_periods=1:start_threshold=-60dB,areverse,afade=t=in:d=0.01,afade=t=out:st=11:d=1" out.wav

# formats
ffmpeg -y -i in.wav -c:a flac out.flac
ffmpeg -y -i in.wav -c:a libvorbis -q:a 6 -metadata LOOPSTART=0 -metadata LOOPLENGTH=480000 out.ogg
ffmpeg -y -i in.wav -c:a libmp3lame -q:a 2 out.mp3      # distribution only, never loops
ffprobe -v error -show_entries stream_tags -of compact out.ogg   # read loop tags back
ffmpeg -y -i in.wav -af aresample=resampler=soxr -ar 48000 -c:a pcm_s24le out.wav   # better resampling (needs libsoxr)

# analysis bundle
ffmpeg -hide_banner -nostats -i in.wav -af silencedetect=n=-60dB:d=0.2 -f null - 2>&1 | grep silence_
ffmpeg -hide_banner -nostats -i in.wav -af astats=measure_perchannel=none:measure_overall=Peak_level+Peak_count+Flat_factor+DC_offset -f null - 2>&1 | grep -E "Peak|Flat|DC"
ffmpeg -hide_banner -nostats -i in.wav -af "pan=mono|c0=0.5*c0+0.5*c1,ebur128=framelog=verbose:dualmono=true" -f null - 2>&1 | grep -E "^\s+I:"
ffmpeg -y -i in.wav -lavfi "showspectrumpic=s=1200x400:legend=0:fscale=log:stop=8000" spec.png

# duck music under a voice
ffmpeg -i music.wav -i voice.wav -filter_complex "[1]asplit[sc][v];[0][sc]sidechaincompress=threshold=0.05:ratio=8:attack=50:release=500[m];[m][v]amix=inputs=2:normalize=0" mix.wav

# crossfade two parts (8 s + 8 s with a 2 s fade gives 14 s)
ffmpeg -i a.wav -i b.wav -filter_complex "acrossfade=d=2:c1=qsin:c2=qsin" ab.wav

# time-stretch 3% without pitch change (quality past about 5% untested)
ffmpeg -i in.wav -af "atempo=1.03" out.wav
```

`afade`'s default curve is linear (`tri`); `qsin` gives equal-power fades. sox equivalents exist
(`sox in.wav -n stats`, `sox in.wav -n spectrogram`) but were not run here.
