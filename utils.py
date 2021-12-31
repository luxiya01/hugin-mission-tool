import sys


def convert_icefront_to_huginos_format(filenames):
    output = []
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if len(output) == 0:
                    output.append(''.join([line.strip(), '\t10']))
                else:
                    output.append(''.join([line.strip(), '\t15']))

    date = filenames[0].split('.')[0].split('_')[-1]
    output_file = f'icefront-{date}.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines('\n'.join(output))


if __name__ == '__main__':
    files = [x for x in sys.argv[1:]]
    print(files)
    convert_icefront_to_huginos_format(files)
