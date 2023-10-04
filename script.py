"""Module that will extract the class names from valid *.css files."""

import re
import os
from pathlib import Path
import tinycss2

log_file = 'log.txt'


# Uses tinycss2
def get_css_classes(contents, filename):
    """Gets classes and writes to filename.

    Args:
        contents: the contents of the *.css file.
        filename: the file to output class names.
    Returns:
        None.

    """
    make_err = filename

    # A list of QualifiedRules, AtRules and Comments
    # TODO: Fix
    rules = tinycss2.parse_stylesheet(contents)

    for rule in rules:
        if rule.type != 'qualified-rule':
            continue
    # 'prelude' means the tokens preceding '{'
    # See https://doc.courtbouillon.org/tinycss2/stable/api_reference.html#tinycss2.ast.QualifiedRule
    prelude_tokens = rule.prelude
    for index, token in enumerate(prelude_tokens[1:], 1):
        previous_token = prelude_tokens[index - 1]
        if token.type == 'ident' and previous_token == '.':
            yield token.value


def main():
    print('Hello World!')

    # Obtain all valid *.css files:
    # Ignore files in third_party/, node_modules/, dist/, scripts/ and .direnv/
    # Only those in /core/ and /extensions/ are fair game.
    css_files = []
    with os.popen("find '/Users/kaka/OpenSource/oppia' -name '*.css' ! -path '*/webpack_bundles/*' ! -path '*/node_modules/*' \
                  ! -path '*/third_party/*' ! -path '*/dist/*' ! -path '*/scripts/*' \
                  ! -path '*/.direnv/*'") as pipe:
        for line in pipe:
            css_files.append(line.strip('\n'))

    # Delete & re-write to log.txt
    if os.path.exists(log_file):
        os.system('rm ' + log_file)
    with open(log_file, 'a', encoding='UTF-8') as f:
        print('# total valid css_files:', len(css_files), file=f)

    # Obtain classes from each *.css file
    for f in css_files:
        # Create corresponding output filename
        filename = Path(f).name
        output_filename = filename[0:filename.find('.')] + '_classes.txt'

        with open(f, 'r', encoding='UTF-8') as file:
            file_contents = file.read()
            get_css_classes(file_contents, output_filename)
            with open(log_file, 'a') as log:
                print('==================================', file=log)
                print(f, file=log)

    # Grep for each class in all the .html files


if __name__ == '__main__':
    main()
