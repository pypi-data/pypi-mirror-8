# pdfmerge [![Build Status][ci-image]][ci-status]
`pdfmerge` is a command-line utility for manipulating PDF files.

## Questions & Issues
If no one [has mentioned it before][gh-issues-all], [let us know][gh-issues].

## Getting Started
### Install
The fastest way to install `pdfmerge` started is to use `pip`:

    $ pip install pdfmerge

On Windows, you can use the [Windows installer][gh-setup] if you don't
have `python`.

### Contribute
If you want to play around with [the latest code][gh-code], start by cloning
the repository:

    $ git clone git://github.com/metaist/pdfmerge.git

Install the dependencies (specifically [pyPdf][pypdf]) using `ant` or `pip`:

    $ ant resolve
    $ pip install -r requirements.txt --use-mirrors

Optionally, test the package using `ant`:

    $ ant test

Install `pdfmerge` as a `python` library:

    $ python setup.py install

All of the magic happens in [pdfmerge.py][gh-pdfmerge].

## Usage

    $ pdfmerge [-h] [--version] [-o FILE|--output FILE] [-p PASSWORD|--password PASSWORD] PATH[RULE[, RULE ...]] [PATH[RULE, ...]] ...]

  * `-o`, `--output` output file (default: `output.pdf`).
    **Must not be any of the input files.**
  * `-p`, '--password` password for encrypted files (default: empty string).
  * `PATH` a file, directory, or wildcard string (e.g., `file*.pdf`) of files
    to merge.
  * `RULE` an optional string indicating which pages to extract and rotate.
    The syntax for each rule is:

        [START][..][END][ROTATE]

    Where `START` and `END` are positive (1-based) or negative page numbers and
    `ROTATE` is one of `>`, `V`, or `<` indicating a clockwise rotation of
    90, 180, 270 degrees, respectively.

## Command-line Example

    $ pdfmerge -o out.pdf file1.pdf file2.pdf[3,3] file2.pdf[1V,2..-1] "other*.pdf[<]" "/path/pdf[1..4>,5]"

This example illustrates several features:
  * specifying an output file (must not be any of the input files)
  * merging multiple files, some more than once
  * splicing parts of file using indicies (1-based; negatives allowed)
  * including the same page multiple times
  * rotating a page or page range
  * merging all the PDFs in a directory

## Features
### Choose an output file.
_Optional_. Specify a path to write the result of the merge.

    $ pdfmerge -o merged.py file1.py file2.py

  * **The output file must not be any of the input files.**
  * By default, the output file is `output.pdf`.
  * You may specify only one output file.

### Merge one or more files.
_Required_. Specify one or more file `PATH`s using wildcards or point to a
directory.

    $ pdfmerge file1.pdf file2.pdf file1.pdf
    $ pdfmerge file*.pdf
    $ pdfmerge /path/pdf

  * You must specify at least one file.
  * You may specifying the same file multiple times.
  * Wildcards are okay (e.g., `file*.pdf`).
  * If you specify a directory, all of the PDFs in that directory will be
    included (i.e. equivalent to appending `*.pdf` to the path).

### Use index-like notation to choose page ranges.
_Optional_. After each `PATH`, specify which parts of the file should be
spliced.

    $ pdfmerge file1.pdf[1] file2.pdf[2]
    $ pdfmerge file*.pdf[7]
    $ pdfmerge file.pdf[3..1]
    $ pdfmerge "file.pdf[1..3, 7..10]"
    $ pdfmerge "file.pdf[2, 1, 3]"
    $ pdfmerge "file.pdf[1, 4..]"

  * If indicies are omitted, all pages are included.
  * Use commas to separate multiple ranges.
  * Whitespace is ignored (e.g., `[1 .. 2, 3]` is the same as `[1..2,3]`), but
    remember to enclose parameters with whitespace.
  * **Indicies start at 1** (1-based), but negative indicies are okay
    (i.e. the first page is `1`, not `0`; `-1` is the last page).
  * Reverse ranges are okay (e.g., `[2..1]` is the reverse of `[1..2]`).
  * Open-ended ranges are okay (e.g., `[2..]` and `[..3]`).
  * Ranges outside of bounds are _quietly_ forced into bounds
    (e.g., `[2..7]` for a 3-page file is treated like `[2..3]`).

### Rotate individual pages or page ranges.
_Optional_. After each range, use a rotator (`>`, `V`, and `<`) to
rotate the range by 90, 180, and 270 degrees clockwise.

    $ pdfmerge "file.pdf[1..3>]"
    $ pdfmerge "file.pdf[1<]"
    $ pdfmerge file.pdf[1..2, 4V]
    $ pdfmerge "*.pdf[>]"

  * When using the `<` and `>` rotators, surround the entire string
    with quotes to avoid conflicts with the command-line's use of
    those operators.
  * The rotator is case-sensitive (i.e. it's a capital `V`).
  * You cannot specify more than one rotator. (Why would you want that?)
  * The rotator comes right after the range (e.g., `[1>,2..3]` not `[1>..3]`).
  * You can still specify a rotator if there's no range (e.g., `[<]` is the
    same as `[1..<]`).

### Specify options in an external file.
_Optional._ You can specify some or all of the options to `pdfmerge` using an
external file. For example, if you have a file `opts.txt`:

    -o myoutput.pdf
    file.pdf[1,3..5>]
    file.pdf[2<]

You can provide it on the command line with a special `@` prefix:

    $ pdfmerge @opts.txt

## Python Module Usage
`pdfmerge` can also be imported into python scripts.

    import pdfmerge
    pdfmerge.merge(['pdf-1.pdf', 'pdf-2.pdf[2>]'], 'output.pdf')

## License
Licensed under the [MIT License][osi-mit].

[ci-image]: https://travis-ci.org/metaist/pdfmerge.png?branch=master
[ci-status]: http://travis-ci.org/metaist/pdfmerge
[gh-code]: https://github.com/metaist/pdfmerge/zipball/master
[gh-issues]: https://github.com/metaist/pdfmerge/issues
[gh-issues-all]: https://github.com/metaist/pdfmerge/issues/search?q=
[gh-pdfmerge]: https://github.com/metaist/pdfmerge/blob/master/pdfmerge.py
[gh-setup]: https://github.com/metaist/pdfmerge/blob/master/releases/pdfmerge-latest-setup.exe
[osi-mit]: http://opensource.org/licenses/MIT
[pypdf]: https://pypi.python.org/pypi/pyPdf
