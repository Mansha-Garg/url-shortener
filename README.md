# URL Shortener

A simple command-line URL shortener built using Python.

## Features

- Shorten long URLs
- Resolve short codes
- List all shortened URLs
- Store data permanently

## Requirements

- Python 3.x

## How to Run

1. Open Command Prompt in the project folder.
2. Run the commands below.

### Shorten a URL

```bash
python main.py shorten https://www.google.com

### Resolve a short code

```bash
python main.py resolve KSFE67

### List all shortened URLs

```bash
python main.py list

## Error Handling

If the URL is invalid:

```bash
python main.py shorten hello

## Data Storage

The shortened URL mappings are stored in `data.json`. This allows the data to remain available even after the program is closed and run again.