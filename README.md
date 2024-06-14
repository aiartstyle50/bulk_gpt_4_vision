# GPT-4 Vision Bulk Processing

This repository provides a script to run GPT-4 Vision in bulk with images on the web. The script reads a CSV file with prompts and corresponding image URLs, processes the images using GPT-4 Vision, and outputs the results to a new CSV file.

## Features

**Bulk Processing:** Process multiple images in one go by specifying prompts and image file locations in a CSV file.
**CSV Input/Output:** Input CSV contains prompts and image file locations. Output CSV contains image URLs and GPT-4 Vision responses.
**Error Handling:** Includes error handling for unsupported image formats, size limits, and network issues with exponential backoff retry logic.

## Usage

1. Create Input CSV: Create a CSV file with prompts in the first column and URLs images in the second column, and no headers.
2. Add your OpenAI API Key
3. Add locations for input csv and output csv.
4. Run the Script: Execute the script to process the images and generate the output CSV.

## Input CSV Format

Put your prompts in the first column and the file location in the second column.

## Other Notes

- Code has exponential backoff in case you run into API rate limits.
