import subprocess
from docassemble.base.util import DAFile, DAFileCollection, DAFileList

__all__ = ['pdf_from_pages']


def pdf_from_pages(input_file, first=None, last=None):
    if first is None:
        first = 1
    elif not isinstance(first, int):
        raise Exception("pdf_from_pages: first must be an integer")
    if first < 1:
        raise Exception("pdf_from_pages: first must be 1 or greater")
    if last is None:
        last = ''
    elif not isinstance(last, int):
        raise Exception("pdf_from_pages: last must be an integer")
    elif last < first:
        raise Exception("pdf_from_pages: last must greater than or equal to first")
    if isinstance(input_file, DAFileCollection):
        input_file = input_file.pdf
    elif isinstance(input_file, DAFileList):
        input_file = input_file[0]
    if not isinstance(input_file, DAFile):
        raise Exception("pdf_from_pages: input_file must be a DAFile, DAFileCollection, or DAFileList")
    output_file = DAFile()
    output_file.set_random_instance_name()
    output_file.initialize(filename=input_file.filename)
    subprocess_arguments = ['pdftk', input_file.path(), 'cat', str(first) + '-' + str(last), 'output', output_file.path()]
    try:
        result = subprocess.run(subprocess_arguments, timeout=60, check=False).returncode
    except subprocess.TimeoutExpired:
        raise Exception("pdf_from_pages: call to pdftk took too long where arguments were " + " ".join(subprocess_arguments))
    if result != 0:
        raise Exception("pdf_from_pages: call to pdftk failed where arguments were " + " ".join(subprocess_arguments))
    output_file.retrieve()
    output_file.commit()
    return output_file
