import ast
import sys
import os
import re
from checks import *
from pep_analyzer import *


errors = {'S001': 'Too long',
          'S002': 'Indentation is not a multiple of four',
          'S003': 'Unnecessary semicolon',
          'S004': 'At least two spaces required before inline comments',
          'S005': 'TODO found',
          'S006': 'More than two blank lines used before this line',
          'S007': 'Too many spaces after \'{}\'',
          'S008': 'Class name \'{}\' should use CamelCase',
          'S009': 'Function name \'{}\' should use snake_case',
          'S010': 'Argument name \'{}\' should be snake_case',
          'S011': 'Variable \'{}\' in function should be snake_case',
          'S012': 'Default argument value is mutable'}

if len(sys.argv) == 2:
    python_paths = []

    if os.path.isdir(sys.argv[1]):
        for root, dirs, files in os.walk(sys.argv[1]):
            for file in files:
                if file.endswith('.py'):
                    python_paths.append(os.path.join(root, file))
    elif sys.argv[1].endswith('.py'):
        python_paths.append(sys.argv[1])

    python_paths.sort()

    for path in python_paths:
        file = open(path, 'r')

        tree = ast.parse(file.read())
        pep_analyzer = PepAnalyzer()
        pep_analyzer.visit(tree)

        file.seek(0)  # Reset file pointer to the start of the file

        empty_lines_cnt = 0

        for i, line in enumerate(file):
            issues = []
            if len(line.strip()) == 0:  # Using strip() to handle lines with spaces as 'empty'
                empty_lines_cnt += 1
            else:
                if empty_lines_cnt > 2:
                    issues.append(f'{path}: Line {i+1}: S006 {errors["S006"]}')
                empty_lines_cnt = 0  # Reset the counter whether an issue was detected or not

            if len(line) > 79:
                issues.append(f'{path}: Line {i+1}: S001 {errors["S001"]}')
            if not valid_indentation(line):
                issues.append(f'{path}: Line {i+1}: S002 {errors["S002"]}')
            if unnecessary_semicolon(line):
                issues.append(f'{path}: Line {i+1}: S003 {errors["S003"]}')
            if not valid_inline_comment(line):
                issues.append(f'{path}: Line {i+1}: S004 {errors["S004"]}')
            if find_todo(line):
                issues.append(f'{path}: Line {i+1}: S005 {errors["S005"]}')
            if too_many_spaces(line)[0]:
                detail = str(too_many_spaces(line)[1])
                issues.append(f'{path}: Line {i+1}: S007 {errors["S007"].format(detail)}')
            if not_camel_case_class(line)[0]:
                detail = str(not_camel_case_class(line)[1])
                issues.append(f'{path}: Line {i+1}: S008 {errors["S008"].format(detail)}')
            if not_snake_case_func(line)[0]:
                detail = str(not_snake_case_func(line)[1])
                issues.append(f'{path}: Line {i+1}: S009 {errors["S009"].format(detail)}')

            for parameter in pep_analyzer.get_parameters(i+1):
                if not re.match(r'[a-z_]+', parameter):
                    issues.append(f'{path}: Line {i+1}: S010 {errors["S010"].format(parameter)}')
                    break

            for variable in pep_analyzer.get_variables(i):
                if not re.match(r"[a-z_]+", variable):
                    issues.append(f'{path}: Line {i}: S011 {errors["S011"].format(variable)}')
                    break

            if pep_analyzer.get_mutable_defaults(i+1):
                issues.append(f'{path}: Line {i+1}: S012 {errors["S012"]}')

            if len(issues) > 0:
                for issue in sorted(issues):
                    print(issue)

        file.close()

else:
    print('Invalid number of command line arguments!')
