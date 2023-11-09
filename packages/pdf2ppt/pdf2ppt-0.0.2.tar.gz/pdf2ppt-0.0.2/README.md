# PDF to PPTX Converter (pdf2ppt)

`pdf2ppt` is a convenient command-line tool for converting PDF files to the PPTX format, enabling easy adjustments to image resolution with customizable DPI settings.

## Key Features

- Simple CLI for quick PDF to PPTX conversions.
- Adjustable DPI for image quality control.
- Progress bar for conversion status tracking.

## Installation

```bash
pip install pdf2ppt
```

## How to Use

Convert a PDF file to PPTX:

```bash
pdf2ppt input.pdf
```

To specify an output file and DPI:

```bash
pdf2ppt input.pdf --output_path output.pptx --dpi 300
```

## Dependencies

- python-pptx
- pdf2image
- tqdm

## Contributing

We welcome contributions to `pdf2ppt`. If you have suggestions or issues, please open an issue or create a pull request.

## License

`pdf2ppt` is open-source software licensed under the MIT license.