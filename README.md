# imdb-photo-downloader

This Python script scrapes data from [IMDb](https://www.imdb.com/) (a popular movie database) to get all the photos from a page chosen by the user, which can be about a person or a movie.

Images are saved in a folder with the name of the person / movie the photos are about.

## Installation

You can install the tool by downloading the release binary (currently available only for Windows):

[imdb-photo-downloader.exe](https://github.com/giovanni-cutri/imdb-photo-downloader/releases/download/latest/imdb.exe)

## Dependencies

All the necessary libraries are listed in the *requirements.txt* file.

You can install them by running:

```
pip install -r requirements.txt
```

In addition to them, you will need the Chrome Web Driver for Selenium to work. You can find it [here](https://googlechromelabs.github.io/chrome-for-testing/).

## Usage

```
imdb-photo-downloader [url]
```

Replace *[url]* with the URL of the IMDb page of which you want to download the photos.

Type ```--help``` for further details.


## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/giovanni-cutri/imdb-photo-downloader/blob/main/LICENSE) file for details.
