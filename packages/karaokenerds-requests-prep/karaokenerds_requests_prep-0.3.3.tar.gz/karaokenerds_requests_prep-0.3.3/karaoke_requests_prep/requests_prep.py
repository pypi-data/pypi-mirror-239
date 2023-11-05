import requests
import os
import re
import glob
from bs4 import BeautifulSoup
import yt_dlp
import logging
import lyricsgenius
from slugify import slugify
from audio_separator import Separator

BASE_URL = "https://karaokenerds.com/Request/"
CACHE_FILE = "karaokenerds_cache.html"


class KaraokeNerdsRequestsPrep:
    def __init__(
        self,
        limit=5,
        log_level=logging.DEBUG,
        log_formatter=None,
        model_name="UVR_MDXNET_KARA_2",
        model_name_2="UVR-MDX-NET-Inst_HQ_3",
        model_file_dir="/tmp/audio-separator-models/",
        output_dir="karaoke",
        use_cuda=False,
        use_coreml=False,
        normalization_enabled=True,
        denoise_enabled=True,
        create_track_subfolders=False,
        skip_num=0,
        sort_order="votes",
    ):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.log_level = log_level
        self.log_formatter = log_formatter

        self.log_handler = logging.StreamHandler()

        if self.log_formatter is None:
            self.log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")

        self.log_handler.setFormatter(self.log_formatter)
        self.logger.addHandler(self.log_handler)

        self.logger.debug(f"RequestsPrep instantiating with limit: {limit}")

        self.limit = int(limit)
        self.model_name = model_name
        self.model_name_2 = model_name_2
        self.model_file_dir = model_file_dir
        self.output_dir = output_dir
        self.use_cuda = use_cuda
        self.use_coreml = use_coreml
        self.normalization_enabled = normalization_enabled
        self.denoise_enabled = denoise_enabled
        self.create_track_subfolders = create_track_subfolders
        self.skip_num = skip_num
        self.sort_order = sort_order

        if not os.path.exists(self.output_dir):
            self.logger.debug(f"Overall output dir {self.output_dir} did not exist, creating")
            os.makedirs(self.output_dir)
        else:
            self.logger.debug(f"Overall output dir {self.output_dir} already exists")

    def fetch_top_requests(self):
        url = f"{BASE_URL}?sort={self.sort_order}"
        self.logger.info(f"Fetching {self.limit} top requests from %s", url)
        html_content = self.fetch_content_from_url(url)
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table", id="requests")
        rows = table.find("tbody").find_all("tr")

        clip = self.limit + self.skip_num
        top_requests = [(row.find_all("td")[0].span.text, row.find_all("td")[1].a.text, row.find_all("td")[2].a.text) for row in rows][
            :clip
        ]

        if self.skip_num > 0:
            self.logger.info(f"Skipping first {self.skip_num} requests based on --skip parameter")
            top_requests = top_requests[self.skip_num :]  # Skip the first X results based on the --skip parameter

        return top_requests

    def fetch_content_from_url(self, url):
        """Fetch content from URL and cache it in a file."""
        if os.path.exists(CACHE_FILE):
            self.logger.info(f"Reading content from cache: {CACHE_FILE}")
            with open(CACHE_FILE, "r", encoding="utf-8") as file:
                return file.read()
        else:
            self.logger.info(f"Fetching content from {url}")
            response = requests.get(url)
            response.raise_for_status()
            content = response.text
            with open(CACHE_FILE, "w", encoding="utf-8") as file:
                file.write(content)
            return content

    def get_youtube_id_for_top_search_result(self, query):
        ydl_opts = {"quiet": "True", "format": "bestaudio", "noplaylist": "True", "extract_flat": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video = ydl.extract_info(f"ytsearch1:{query}", download=False)["entries"][0]

            if video:
                youtube_id = video.get("id")
                return youtube_id
            else:
                self.logger.warning(f"No YouTube results found for query: {query}")
                return None

    def download_audio(self, youtube_id, filename):
        ydl_opts = {
            "format": "ba",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": f"{filename}",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as youtube_dl_instance:
            youtube_dl_instance.download([f"https://www.youtube.com/watch?v={youtube_id}"])

    def write_lyrics_from_genius(self, artist, title, filename):
        genius = lyricsgenius.Genius(os.environ["GENIUS_API_TOKEN"])
        song = genius.search_song(title, artist)
        if song:
            lyrics = self.clean_genius_lyrics(song.lyrics)

            with open(filename, "w") as f:
                f.write(lyrics)

            self.logger.info("Lyrics for %s by %s fetched successfully", title, artist)
        else:
            self.logger.warning("Could not find lyrics for %s by %s", title, artist)

    def clean_genius_lyrics(self, lyrics):
        lyrics = lyrics.replace("\\n", "\n")
        lyrics = re.sub(r"You might also like", "", lyrics)
        lyrics = re.sub(
            r".*?Lyrics([A-Z])", r"\1", lyrics
        )  # Remove the song name and word "Lyrics" if this has a non-newline char at the start
        lyrics = re.sub(r"[0-9]+Embed$", "", lyrics)  # Remove the word "Embed" at end of line with preceding numbers if found
        lyrics = re.sub(r"(\S)Embed$", r"\1", lyrics)  # Remove the word "Embed" if it has been tacked onto a word at the end of a line
        lyrics = re.sub(r"^Embed$", r"", lyrics)  # Remove the word "Embed" if it has been tacked onto a word at the end of a line
        lyrics = re.sub(r".*?\[.*?\].*?", "", lyrics)  # Remove lines containing square brackets
        # add any additional cleaning rules here
        return lyrics

    def sanitize_filename(self, filename):
        """Replace or remove characters that are unsafe for filenames."""
        # Replace problematic characters with underscores
        for char in ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]:
            filename = filename.replace(char, "_")
        # Remove any trailing periods or spaces
        filename = filename.rstrip(". ")
        return filename

    def separate_audio(self, audio_file, model_name, instrumental_path, vocals_path):
        if audio_file is None or not os.path.isfile(audio_file):
            raise Exception("Error: Invalid audio source provided.")

        self.logger.debug(f"audio_file is valid file: {audio_file}")

        self.logger.debug(f"instantiating Separator with model_name: {model_name} and instrumental_path: {instrumental_path}")
        separator = Separator(
            audio_file,
            log_level=self.log_level,
            log_formatter=self.log_formatter,
            model_name=model_name,
            model_file_dir=self.model_file_dir,
            output_format="MP3",
            primary_stem_path=instrumental_path,
            secondary_stem_path=vocals_path,
        )
        _, _ = separator.separate()
        self.logger.debug(f"Separation complete!")

    def setup_output_paths(self, artist, title):
        sanitized_artist = self.sanitize_filename(artist)
        sanitized_title = self.sanitize_filename(title)
        artist_title = f"{sanitized_artist} - {sanitized_title}"

        track_output_dir = self.output_dir
        if self.create_track_subfolders:
            track_output_dir = os.path.join(self.output_dir, f"{artist_title}")

        if not os.path.exists(track_output_dir):
            self.logger.debug(f"Output dir {track_output_dir} did not exist, creating")
            os.makedirs(track_output_dir)

        return track_output_dir, artist_title

    def prep(self):
        processed_tracks = {}

        top_requests = self.fetch_top_requests()

        self.logger.info(f"Fetched {len(top_requests)} song requests, factoring in skip, sort and limit params")

        # Process all downloads (audio, lyrics) first before doing audio separation,
        # to prioritize operations requiring internet in case we're prepping in a hurry before an offline period such as a flight
        for votes, artist, title in top_requests:
            self.logger.info(f"Downloading inputs for track: {title} by {artist} with votes: {votes}")
            track_output_dir, artist_title = self.setup_output_paths(artist, title)
            processed_tracks[artist_title] = {
                "track_output_dir": track_output_dir,
                "artist": artist,
                "title": title,
                "votes": votes,
            }

            yt_filename_pattern = os.path.join(track_output_dir, f"{artist_title} (YouTube *.wav")
            youtube_audio_files = glob.glob(yt_filename_pattern)
            youtube_audio_file = None

            if youtube_audio_files:
                youtube_audio_file = youtube_audio_files[0]
                self.logger.debug(f"Youtube audio already exists, skipping download: {youtube_audio_file}")
            else:
                self.logger.info("Searching YouTube for video ID...")
                query = f"{artist} {title}"
                youtube_id = self.get_youtube_id_for_top_search_result(query)
                if youtube_id:
                    youtube_audio_file = os.path.join(track_output_dir, f"{artist_title} (YouTube {youtube_id})")

                    self.logger.info("Downloading original audio from YouTube to filename {original_audio_filename}")
                    self.download_audio(youtube_id, youtube_audio_file)
                    youtube_audio_file = youtube_audio_file + ".wav"
                else:
                    self.logger.warning(f"Skipping {title} by {artist} due to missing YouTube ID.")

            processed_tracks[artist_title]["youtube_audio"] = youtube_audio_file

            lyrics_file = os.path.join(track_output_dir, f"{artist_title} (Lyrics).txt")
            if os.path.exists(lyrics_file):
                self.logger.debug(f"Lyrics file already exists, skipping fetch: {lyrics_file}")
            else:
                self.logger.info("Fetching lyrics from Genius...")
                self.write_lyrics_from_genius(artist, title, lyrics_file)

            processed_tracks[artist_title]["lyrics"] = lyrics_file

        self.logger.info(f"All downloads complete! Beginning offline processes")

        for artist_title, track in processed_tracks.items():
            self.logger.info(f"Separating audio twice for track: {track['title']} by {track['artist']} with votes: {track['votes']}")

            instrumental_path = os.path.join(track_output_dir, f"{artist_title} (Instrumental {self.model_name}).mp3")
            vocals_path = os.path.join(track_output_dir, f"{artist_title} (Vocals {self.model_name}).mp3")

            if os.path.isfile(instrumental_path) and os.path.isfile(vocals_path):
                self.logger.debug(f"Separated audio files already exist in output paths, skipping separation: {instrumental_path}")
            else:
                self.separate_audio(processed_tracks[artist_title]["youtube_audio"], self.model_name, instrumental_path, vocals_path)

            processed_tracks[artist_title]["instrumental_audio"] = instrumental_path
            processed_tracks[artist_title]["vocals_audio"] = vocals_path

            instrumental_path_2 = os.path.join(track_output_dir, f"{artist_title} (Instrumental {self.model_name_2}).mp3")
            vocals_path_2 = os.path.join(track_output_dir, f"{artist_title} (Vocals {self.model_name_2}).mp3")

            if os.path.isfile(instrumental_path_2) and os.path.isfile(vocals_path_2):
                self.logger.debug(f"Separated audio files already exist in output paths, skipping separation: {instrumental_path_2}")
            else:
                self.separate_audio(processed_tracks[artist_title]["youtube_audio"], self.model_name_2, instrumental_path_2, vocals_path_2)

            processed_tracks[artist_title]["instrumental_audio_2"] = instrumental_path_2
            processed_tracks[artist_title]["vocals_audio_2"] = vocals_path_2

        self.logger.info("Script finished, all songs downloaded, lyrics fetched and audio separated!")

        return processed_tracks
