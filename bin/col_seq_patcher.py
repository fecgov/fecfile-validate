import argparse

parser = argparse.ArgumentParser(
    prog='Column Sequence Patcher',
    description='Creates a copy of a JSON schema file where\n'+
        'all COL_SEQ attributes have been updated to\n'+
        'be sequential in order of appearance within\n'+
        'the file.'
)

parser.add_argument('filename')
args = parser.parse_args()

og_file = open(args.filename, 'r')
new_file = open("patched_"+args.filename, 'w')

col_seq_count = 1
for line in og_file:
    out_line = line
    indentation = line.split('"')[0]
    key = line.strip().split(":")[0]
    if key and key == '"COL_SEQ"':
        new_value = col_seq_count
        col_seq_count += 1
        out_line = indentation+key+": "+str(new_value)+",\n"
    new_file.write(out_line)

print(f'Columns 1-{col_seq_count} found')
og_file.close()
new_file.close()
