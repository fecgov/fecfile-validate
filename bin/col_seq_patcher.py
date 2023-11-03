import argparse

# Column Sequence Patcher
#
#   Creates a copy of an existing JSON schema file
#   where all COL_SEQ attributes have been updated
#   to be sequential in order of appearance within
#   the file.

parser = argparse.ArgumentParser(
    prog='Column Sequence Patcher',
    description='Creates a copy of an existing JSON schema file\n' +
                'where all COL_SEQ attributes have been updated\n' +
                'to be sequential in order of appearance within\n' +
                'the file.'
)

parser.add_argument('filename')
args = parser.parse_args()

old_file = open(args.filename, 'r')
new_file = open("patched_"+args.filename, 'w')

col_seq_count = 0
for line in old_file:
    out_line = line
    if "COL_SEQ" in line:
        indentation = line.split('"')[0]
        key = line.strip().split(":")[0]
        if key and key == '"COL_SEQ"':
            col_seq_count += 1
            new_value = col_seq_count
            out_line = indentation+key+": "+str(new_value)+",\n"
    new_file.write(out_line)

print(f'COL_SEQ values 1 -> {col_seq_count} found and updated')
old_file.close()
new_file.close()
