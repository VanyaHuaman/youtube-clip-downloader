# YouTube Clip Downloader (CLI)

A simple, standalone Python script to download YouTube clips in the highest quality (1080p 60fps).

## Features

- 🎬 Download YouTube clips and videos in highest quality (1080p 60fps by default)
- ⚡ Smart format selection (prioritizes HLS format 301 for best clip support)
- 📁 Custom output directory support
- 🎯 Quality selection options (1080p, 720p, 480p, 360p, etc.)
- 🔄 Automatic fallback to best available quality
- ⚠️ Live stream detection with helpful warnings

## Requirements

- Python 3.7 or higher
- yt-dlp

## Installation

1. **Install yt-dlp:**

```bash
# Using pip
pip install yt-dlp

# OR using Homebrew (macOS)
brew install yt-dlp
```

2. **Download the script:**

```bash
# Clone this repo or download youtube_clip_downloader.py directly
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/youtube-clip-downloader/main/youtube_clip_downloader.py
chmod +x youtube_clip_downloader.py
```

## Usage

### Basic Usage

```bash
# Download a clip (highest quality by default)
python3 youtube_clip_downloader.py "https://youtube.com/clip/CLIP_ID"

# Download to a specific folder
python3 youtube_clip_downloader.py "https://youtube.com/clip/CLIP_ID" -o ~/Downloads

# Choose specific quality
python3 youtube_clip_downloader.py "https://youtube.com/clip/CLIP_ID" -q 720p
```

### All Options

```bash
python3 youtube_clip_downloader.py --help
```

```
usage: youtube_clip_downloader.py [-h] [-o OUTPUT] [-q {best,worst,2160p,1440p,1080p,720p,480p,360p}] 
                                    [-f {mp4,webm,mkv}] url

Download YouTube videos and clips easily

positional arguments:
  url                   YouTube video or clip URL

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory (default: current directory)
  -q {best,worst,2160p,1440p,1080p,720p,480p,360p}, --quality {best,worst,2160p,1440p,1080p,720p,480p,360p}
                        Video quality (default: best)
  -f {mp4,webm,mkv}, --format {mp4,webm,mkv}
                        Output format (default: mp4)
```

## Examples

```bash
# Download clip to current directory
python3 youtube_clip_downloader.py "https://www.youtube.com/clip/UgkxPMkyUyfaEruuGeAdRx8xzfixa4iJd9zj"

# Download to Downloads folder in highest quality
python3 youtube_clip_downloader.py "https://www.youtube.com/clip/UgkxPMkyUyfaEruuGeAdRx8xzfixa4iJd9zj" -o ~/Downloads

# Download in 720p
python3 youtube_clip_downloader.py "https://www.youtube.com/clip/UgkxPMkyUyfaEruuGeAdRx8xzfixa4iJd9zj" -q 720p -o ~/Downloads

# Download full video (not just clip)
python3 youtube_clip_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" -o ~/Downloads

# Download as WebM format
python3 youtube_clip_downloader.py "https://www.youtube.com/clip/CLIP_ID" -f webm
```

## Quality Information

**Default Quality:**
- The script defaults to the highest quality available (typically 1080p 60fps)
- Uses HLS format 301 for best results with clips
- Automatically falls back to other high-quality formats if unavailable

**Format Priority:**
1. Format 301 - HLS 1080p 60fps (best for clips)
2. Format 300 - HLS 720p 60fps
3. Format 299+140 - DASH 1080p 60fps + audio
4. bestvideo+bestaudio - Best available
5. best - Ultimate fallback

**Typical File Sizes (54-second clip):**
- 1080p 60fps: ~8-21 MB
- 720p 60fps: ~5-10 MB
- 360p 30fps: ~2-3 MB

## Live Stream Clips

If you try to download a clip from a **currently live stream**, you'll see a warning:

```
⚠️  WARNING: This clip is from a LIVE STREAM that is currently broadcasting.
   Clip timestamp: 3076.9s into the stream
   Current issue: yt-dlp cannot download past segments from active live streams.
   
   Options:
   1. Wait for the stream to end and be archived, then try again
   2. Download will proceed but may only capture recent stream content
   
   Continue anyway? (y/n):
```

**Why?** YouTube live streams only buffer recent content (30-60 seconds). Historical segments aren't available until the stream ends and is archived.

**Solution:** Wait for the stream to end, then download the clip.

## Troubleshooting

**"yt-dlp not found"**
```bash
pip install yt-dlp
# or
brew install yt-dlp
```

**"Permission denied" when running script**
```bash
chmod +x youtube_clip_downloader.py
```

**Download fails or gets wrong quality**
- Update yt-dlp: `pip install --upgrade yt-dlp`
- Check the URL is correct (should contain `/clip/` for clips)
- Try running yt-dlp directly to see detailed errors: `yt-dlp -F "YOUR_URL"`

**Script hangs or is very slow**
- Check your internet connection
- Some clips may be large (1080p60 can be 20+ MB for a 1-minute clip)
- Try with a lower quality: `-q 720p`

## How It Works

The script uses yt-dlp (a youtube-dl fork) to:

1. Extract clip metadata from YouTube
2. Detect if it's from a live stream
3. Select the best available format based on your preferences
4. Download and merge video + audio streams
5. Save to your specified location with a clean filename

## Technical Details

- **Format Selection:** Prioritizes HLS formats (301, 300) over DASH (299+140) because they work better with YouTube's clip system
- **Filename Sanitization:** Uses `--restrict-filenames` to remove special characters
- **Live Detection:** Checks `is_live` and `section_start` metadata to warn about live stream limitations

## Privacy & Security

- Everything runs locally on your computer
- No data sent to external servers (except YouTube to download)
- Open source - you can review all code
- No tracking or analytics

## License

Free to use and modify. Share with friends! 🎉

## Related Projects

Looking for a browser extension instead? Check out [YouTube Clip Downloader Extension](https://github.com/YOUR_USERNAME/youtube-clip-downloader-extension)

## Credits

Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp)
