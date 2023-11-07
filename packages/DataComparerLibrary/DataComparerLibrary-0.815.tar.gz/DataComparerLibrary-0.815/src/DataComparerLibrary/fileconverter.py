import os
import re


class FileConverter:
    def remove_separate_lf(self, input_file, output_file):
        # Remove separate linefeed (LF), so carriage return linefeed (CRLF) remains.
        if not os.path.exists(input_file):
            raise Exception("Input file doesn't exists: ", input_file)
        #
        print("input_file: ", input_file)
        print("output_file: ", output_file)
        #
        with open(input_file, "rb") as input_file:
            with open(output_file, "wb") as output_file:
                output_file.write(re.sub(b"(?<!\r)\n", b"", input_file.read()))


    def replace_separate_lf(self, input_file, output_file, replacement_string, encoding='utf-8'):
        # Replace separate linefeed (LF), so carriage return linefeed (CRLF) remains.
        if not os.path.exists(input_file):
            raise Exception("Input file doesn't exists: ", input_file)
        #
        print("input_file: ", input_file)
        print("output_file: ", output_file)
        print("replacement_string: ", replacement_string)
        print("encoding: ", encoding)
        #
        with open(input_file, "rb") as input_file:
            with open(output_file, "wb") as output_file:
                output_file.write(re.sub(b"(?<!\r)\n", replacement_string.encode(encoding), input_file.read()))

