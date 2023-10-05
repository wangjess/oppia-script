"""Module that will extract the class names from valid *.css files."""

import os
import shutil
from pathlib import Path
import tinycss2
log_file = 'output/log.txt'

def get_classes(contents, filename):
    """Gets classes and writes to filename.

    Args:
        contents: the contents of the *.css file.
        filename: the file to output class names.
    Returns:
        Number of classes found.

    """
    exclusions = ['a', 'li', 'ul', 'p', 'focus']
    classes = []

    # A list of QualifiedRules
    rules = tinycss2.parse_stylesheet(contents, skip_comments=True, skip_whitespace=True)
    for rule in rules:
        if rule.type == 'qualified-rule':
            for i, val in enumerate(rule.prelude):
                if val.type == 'ident':
                    if val.value not in exclusions:
                        classes.append(val.value)

    # Get unique set
    new_classes = set(list(set(classes)))
    with open(filename, 'a') as log:
        for val in new_classes:
            print(val, file=log)

    return len(new_classes)

def main():
    print('Start!')

    # Obtain all valid *.css files:
    # Ignore files in third_party/, node_modules/, dist/, scripts/ and .direnv/
    # Only those in /core/ and /extensions/ are fair game.
    css_files = []
    with os.popen("find '/Users/kaka/OpenSource/oppia' -name '*.css' ! -path '*/webpack_bundles/*' ! -path '*/node_modules/*' \
                  ! -path '*/third_party/*' ! -path '*/dist/*' ! -path '*/scripts/*' \
                  ! -path '*/.direnv/*'") as pipe:
        for line in pipe:
            css_files.append(line.strip('\n'))

    # Delete & re-create output/ folder
    if os.path.isdir("output"):
        shutil.rmtree("output", ignore_errors=True)
        os.mkdir("output")
    else:
        os.mkdir("output")

    with open(log_file, 'a', encoding='UTF-8') as f:
        print('# total valid css_files:', len(css_files), file=f)

    # Obtain classes from each *.css file
    for f in css_files:
        # Create corresponding output files
        filename = Path(f).name
        out_f = filename[0:filename.find('.')] + '_classes.txt'
        final_out = "output/" + out_f

        with open(f, 'r', encoding='UTF-8') as file:
            file_contents = file.read()
            num_classes = get_classes(file_contents, final_out)
            with open(log_file, 'a') as log:
                print('==================================', file=log)
                print(f, file=log)
                print(num_classes, file=log)

    # Grep for each class in all the .html files


if __name__ == '__main__':
    main()
