# RSS Reader with Text-to-Speech (TTS)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://spdx.org/licenses/MIT.html)

This Python RSS reader utilizes text-to-speech (TTS) to read articles from RSS feeds aloud. It allows you to listen to the latest news and updates from your favorite sources, making it an excellent tool for staying informed while on the go.

<p align="center">
  <img src="https://github.com/ruitcatarino/rss2tts/blob/main/rss2tts.png?raw=true" alt="RSS news aggregator."/>
</p>

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Contributing](#contributing)
  - [Todo](#todo)
- [License](#license)

## Features

- Read articles from RSS feeds using text-to-speech (TTS).
- Support for multiple languages with automatic language detection.
- Customizable TTS reading rate.
- Navigate through articles with ease.
- Cross-platform support for clearing the terminal screen.

## Installation

Clone this repository to your local machine:
   ```shell
   git clone https://github.com/ruitcatarino/rss2tts.git
   cd rss2tts
   ```

### Python
  ```shell
  pip3 install -r requirements.txt
  python3 rss2tts.py
  ```

### Poetry
  ```shell
  poetry run python3 rss2tts.py
  ```

## Contributing

Contributions are welcome! If you'd like to improve this RSS reader, feel free to open an issue, submit a pull request, or provide suggestions for enhancements.

### Todo

Here are some tasks and improvements that can be addressed in future updates:

- Test in different environments (e.g., Linux, macOS) to ensure cross-platform compatibility.
- Add support for more TTS voices and languages.
- Create a user-friendly configuration file for RSS feed URLs.
- Enhance the user interface for a more intuitive experience.
- Improve documentation and add usage examples.

## License

This project is open-source and available under the [MIT License](LICENSE). You are free to use, modify, and distribute it in accordance with the license terms.
