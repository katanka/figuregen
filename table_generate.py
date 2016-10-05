import sys, getopt, re

datafile = None

table_label = "generatetable"

path_prefix = None

table_template = """\\begin{{table}}[H]
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

def get_color():
   global i
   return colors[i]

def get_new_color():
   global i
   i = (i + 1) % len(colors)
   return get_color()

def generate_line(raw_line, standard_length):
   color = get_color()
   print color

   columns = raw_line.split("\t")

   if len(columns) == 1:
      # caption
      return columns[0]
   elif len(columns) > standard_length:
      color = get_new_color()
   
   return "\\cellcolor[HTML]{" + color + "} " + (" & \\cellcolor[HTML]{" + color + "} ").join(columns)

def generate_header(raw_line):
   columns = raw_line.split("\t")
   return " & ".join(columns)

def generate_table(filename):
   input_file = open(filename, 'r')

   input_lines = input_file.read().split("\n")

   standard_length = min(len(line.split("\t")) for line in input_lines[1:])

   print standard_length

   caption = input_lines[0]

   header = input_lines[1]



   data = [generate_line(line, standard_length) for line in input_lines[2:]]

   data_string = "".join([line + "\\\\ \n" for line in data])

   subs = {'caption': caption, "header": header, "data": data_string}

   return table_template.format(**subs)

def replace_line_with_table(path_prefix, line):
   first_quote_indices = [pos for pos, char in enumerate(line) if char == '\"']

   input_filename = line[first_quote_indices[0]+1:first_quote_indices[1]]

   print "Generating table from " + `input_filename` + "..."

   table = generate_table(path_prefix + input_filename)

   print "Done"

   return table

def main(argv):
   # make sure it was called correctly
   if len(argv) != 1:
      print "usage: python table_generate.py [LaTeX file name]"
      exit()

   # read the input file
   datafile = open(argv[0], 'r+')
   path_prefix = "/".join(argv[0].split("/")[0:-1]) + "/"

   file_contents = datafile.read()

   input_filename = None

   lines = file_contents.split("\n")

   for i in range(len(lines)):
      line = lines[i]
      if table_label in line:
         lines[i] = replace_line_with_table(path_prefix, line)
         get_new_color()

   file_contents = "\n".join(lines)
   print file_contents

   datafile.seek(0)
   datafile.write(file_contents)
   datafile.truncate()
   datafile.close()


if __name__ == "__main__":
   main(sys.argv[1:])