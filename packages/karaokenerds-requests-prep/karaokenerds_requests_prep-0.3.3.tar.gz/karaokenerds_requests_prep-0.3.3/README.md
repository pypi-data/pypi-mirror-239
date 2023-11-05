# KaraokeNerds Requests Prep 🎶

[![PyPI version](https://badge.fury.io/py/karaokenerds-requests-prep.svg)](https://badge.fury.io/py/karaokenerds-requests-prep)

Prepare for bulk karaoke video creation, by downloading audio from YouTube and lyrics from Genius for [top requests on karaokenerds](https://karaokenerds.com/Request/?sort=votes).

This was created with a single use case in mind - to make it easier for me to prepare for bulk creation of karaoke videos while I'm offline (e.g. on a flight or train).
It makes it easy to bulk prepare the top X requests by votes, tips, views, spotify rank etc. so I can then do the actual karaoke creation in a focused batch without internet.

## Features

- Audio Fetching: Automatically searches YouTube for each song, downloads the top result and extracts the best quality audio in WAV format.
- Lyrics Fetching: Automatically fetches song lyrics from Genius.com using [LyricsGenius](https://github.com/johnwmillr/LyricsGenius).
- Audio Separation: Separates the downloaded audio into instrumental and vocal tracks, using [audio-separator](https://github.com/karaokenerds/python-audio-separator/).
- Multiple Audio Models: Runs audio separation with 2 different models (by default, `UVR_MDXNET_KARA_2` and `UVR-MDX-NET-Inst_HQ_3`) to give you options for the backing track.
- Easy Configuration: Control the tool's behavior using command-line arguments.
- Organized Outputs: Creates structured output directories for easy access to generated tracks and lyrics.
- Internet First: Completes all operations which require internet first (quickly), in case user is preparing last-minute before a period of being offline!

## Installation 🛠️

You can install KaraokeNerds Requests Prep using pip:

`pip install karaokenerds-requests-prep`


## Usage 🚀

### Command Line Interface (CLI)

You can use Audio Separator via the command line:

```sh
usage: karaokenerds-requests-prep [-h] [-v] [--log_level LOG_LEVEL] [--model_name MODEL_NAME] [--model_file_dir MODEL_FILE_DIR] [--output_dir OUTPUT_DIR] [--use_cuda] [--use_coreml] [--denoise DENOISE] [--normalize NORMALIZE]
                                  [--create_track_subfolders] [--skip SKIP_NUM] [--sort {votes,tip,views,spotify,date}]
                                  [limit]

Fetch audio and lyrics for requests from karaokenerds, to prepare for bulk karaoke video creation.

positional arguments:
  limit                                  Number of requests to fetch.

options:
  -h, --help                             show this help message and exit
  -v, --version                          show program's version number and exit
  --log_level LOG_LEVEL                  Optional: logging level, e.g. info, debug, warning (default: info). Example: --log_level=debug
  --model_name MODEL_NAME                Optional: model name to be used for separation (default: UVR_MDXNET_KARA_2). Example: --model_name=UVR-MDX-NET-Inst_HQ_3
  --model_file_dir MODEL_FILE_DIR        Optional: model files directory (default: /tmp/audio-separator-models/). Example: --model_file_dir=/app/models
  --output_dir OUTPUT_DIR                Optional: directory to write output files (default: <current dir>/karaoke). Example: --output_dir=/app/karaoke
  --use_cuda                             Optional: use Nvidia GPU with CUDA for separation (default: False). Example: --use_cuda=true
  --use_coreml                           Optional: use Apple Silicon GPU with CoreML for separation (default: False). Example: --use_coreml=true
  --denoise DENOISE                      Optional: enable or disable denoising during separation (default: True). Example: --denoise=False
  --normalize NORMALIZE                  Optional: enable or disable normalization during separation (default: True). Example: --normalize=False
  --create_track_subfolders              Optional: create subfolders in the output folder for each track (default: False). Example: --create_track_subfolders=true
  --skip SKIP_NUM                    Optional: skip the first X number of results. Example: --skip=10
  --sort {votes,tip,views,spotify,date}  Optional: choose the order for the sort parameter (default: votes). Valid options: votes, tip, views, spotify, date
  ```

  Example:

```
karaokenerds-requests-prep --sort votes 10
```

This command will process the top 10 requests with the highest votes on Karaoke Nerds, downloading audio and lyrics for each and separating audio, ready for all 10 tracks to be created by whatever process you prefer for creating karaoke tracks!

By default, you'll then end up with a folder called `karaoke` with all of the input files ready for bulk karaoke track creation, neatly organised e.g.

```
├── Artist - Title (Instrumental UVR-MDX-NET-Inst_HQ_3).flac
├── Artist - Title (Instrumental UVR_MDXNET_KARA_2).flac
├── Artist - Title (Lyrics).txt
├── Artist - Title (Vocals UVR-MDX-NET-Inst_HQ_3).flac
├── Artist - Title (Vocals UVR_MDXNET_KARA_2).flac
└── Artist - Title (YouTube CNUgemJBLTw).wav
```

## Requirements 📋

Python >= 3.9

Libraries: onnx, onnxruntime, numpy, soundfile, librosa, torch, wget, six

## Developing Locally

This project uses Poetry for dependency management and packaging. Follow these steps to setup a local development environment:

### Prerequisites

- Make sure you have Python 3.9 or newer installed on your machine.
- Install Poetry by following the installation guide here.

### Clone the Repository

Clone the repository to your local machine:

```
git clone https://github.com/YOUR_USERNAME/karaokenerds-requests-prep.git
cd karaokenerds-requests-prep
```

Replace YOUR_USERNAME with your GitHub username if you've forked the repository, or use the main repository URL if you have the permissions.

### Install Dependencies

Run the following command to install the project dependencies:

```
poetry install
```

### Activate the Virtual Environment

To activate the virtual environment, use the following command:

```
poetry shell
```

### Running the Command-Line Interface Locally

You can run the CLI command directly within the virtual environment. For example:

```
karaokenerds-requests-prep 1
```

### Deactivate the Virtual Environment

Once you are done with your development work, you can exit the virtual environment by simply typing:

```
exit
```

### Building the Package

To build the package for distribution, use the following command:

```
poetry build
```

This will generate the distribution packages in the dist directory - but for now only @beveradb will be able to publish to PyPI.

## Contributing 🤝

Contributions are very much welcome! Please fork the repository and submit a pull request with your changes, and I'll try to review, merge and publish promptly!

- This project is 100% open-source and free for anyone to use and modify as they wish. 
- If the maintenance workload for this repo somehow becomes too much for me I'll ask for volunteers to share maintainership of the repo, though I don't think that is very likely

## License 📄

This project is licensed under the MIT [License](LICENSE).

- **Please Note:** If you choose to integrate this project into some other project using the default model or any other model trained as part of the [UVR](https://github.com/Anjok07/ultimatevocalremovergui) project, please honor the MIT license by providing credit to UVR and its developers!

## Credits 🙏

- [karaokenerd](https://github.com/karaokenerd) - Creator of [KaraokeNerds.com](https://karaokenerds.com/), without which we wouldn't even have a way to request karaoke tracks for creation! Huge thank you for the creation of the website which helps karaoke community creators keep organised and focused!
- [Anjok07](https://github.com/Anjok07) - Author of [Ultimate Vocal Remover GUI](https://github.com/Anjok07/ultimatevocalremovergui), which was essential for the creation of [audio-separator](https://github.com/karaokenerds/python-audio-separator/)! Thank you!

## Contact 💌

For questions or feedback, please raise an issue or reach out to @beveradb ([Andrew Beveridge](mailto:andrew@beveridge.uk)) directly.
