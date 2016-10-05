import sys, getopt, re

datafile = None

label = "generatetable"

path_prefix = None

template = """\\begin{{table}}[H]
\centering
\caption{{{caption}}}
\\begin{{tabular}}{{llll}}
\\toprule
{header} \\\\ \\midrule
{data}
\\bottomrule
\end{{tabular}}
\end{{table}}
"""

colors = ["CBCEFB", "FFCE93", "C3ECEB", "ECC3E7"]
i = 0


def process_args(argv):
   global datafile, path_prefix
   if len(argv) != 1:
      print "usage: python table_generate.py [LaTeX file name]"
      exit()
   datafile = open(argv[0], 'r+')
   path_prefix = "/".join(argv[0].split("/")[0:-1]) + "/"

def get_color():
   global i
   i = (i + 1) % len(colors)
   return colors[i]

def generate_line(raw_line):
   color = get_color()

   columns = raw_line.split("\t")

   if len(columns) == 1:
      # caption
      return columns[0]
   else:
      return "\\cellcolor[HTML]{" + color + "}" + (" & \\cellcolor[HTML]{" + color + "}").join(columns)

def generate_table(filename):
   input_file = open(path_prefix + filename, 'r')

   lines = [generate_line(line) for line in input_file.read().split("\n")]

   caption = lines[0]

   header = lines[1]

   data = lines[2:]

   data_string = "".join([line + "\\\\ \n" for line in data])

   subs = {'caption': caption, "header": header, "data": data_string}

   return template.format(**subs)

def main(argv):
   global datafile, label

   process_args(argv)

   file_contents = datafile.read()

   input_filename = None
   label_line = None

   for line in file_contents.split("\n"):
      if label in line:
         label_line = line

   first_quote_indices = [pos for pos, char in enumerate(label_line) if char == '\"']

   input_filename = label_line[first_quote_indices[0]+1:first_quote_indices[1]]

   table = generate_table(input_filename)

   file_contents = file_contents.replace(label_line, table)

   print file_contents

   datafile.seek(0)
   datafile.write(file_contents)
   datafile.truncate()
   datafile.close()


if __name__ == "__main__":
   main(sys.argv[1:])