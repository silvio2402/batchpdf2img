# Batch PDF -> image converter

This is a simple command line utility to convert PDF files to images.

## Requirements

- Python 3
- [pdf2image](https://pypi.org/project/pdf2image/) python package including poppler installed and in PATH

## Installation

```bash
git clone https://github.com/silvio2402/batchpdf2img.git
cd batchpdf2img
pip install -r requirements.txt
```

### Installing poppler

#### Windows

Windows users will have to build or download poppler for Windows. I recommend [@oschwartz10612 version](https://github.com/oschwartz10612/poppler-windows/releases/) which is the most up-to-date. You will then have to add the `bin/` folder to [PATH](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).

#### Linux

Most distros ship with `pdftoppm` and `pdftocairo`. If they are not installed, refer to your package manager to install `poppler-utils`.

#### Mac

Mac users will have to install poppler.

Installing using [Brew](https://brew.sh/):

```bash
brew install poppler
```

## Usage

```bash
python batchpdf2img.py pdfstoconvert/*.pdf -o pageimages/
```

```
usage: batchpdf2img.py [-h] -o OUTPUT [-e EXT] [-t MAX_THREADS] [-w] files

batch convert pdfs to images

positional arguments:
  files                 input files wildcard

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output directory
  -e EXT, --ext EXT     output format extension
  -t MAX_THREADS, --max-threads MAX_THREADS
                        max number of converter threads
  -w, --overwrite       overwrite all document, else only incomplete
```
