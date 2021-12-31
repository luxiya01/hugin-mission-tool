import sys

def convert_icefront_to_huginos_format(filename):
    output = []
    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i == 0:
                output.append(''.join([line.strip(), '\t10']))
            else:
                output.append(''.join([line.strip(), '\t15']))
    output_file = f'{filename.split(".")[0]}-huginos.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines('\n'.join(output))

if __name__ == '__main__':
    convert_icefront_to_huginos_format(sys.argv[1])
