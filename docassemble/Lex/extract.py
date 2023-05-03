import subprocess
import tempfile
import pathlib
import shutil
import os
import os.path
def extract_writing(input_file, output_file):
  tempdir = tempfile.mkdtemp()
  from_file = os.path.join(tempdir, 'file'+ pathlib.Path(input_file).suffix)
  to_file = os.path.join(tempdir, 'file.png')
  shutil.copyfile(input_file, from_file)
  argument_list = ['convert', from_file, '(', '-fuzz', '20%', '-transparent', 'LightGray', ')', '-trim', to_file]
  subprocess.run(argument_list)
  shutil.copyfile(to_file, output_file)
  if tempdir is not None:
    shutil.rmtree(tempdir)
    return True
