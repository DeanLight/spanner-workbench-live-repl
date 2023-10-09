import os

supported_ie_funcs = "PREDEFINED_IE_FUNCS = [PYRGX, PYRGX_STRING, JsonPath, JsonPathFull]"
dirname = os.path.dirname(__file__)
def remove_predefined_ie_funcs(file_path):
    with open(file_path, 'r') as file:
        file_content = file.readlines()

    start_index = None
    end_index = None
    for i, line in enumerate(file_content):
        if 'PREDEFINED_IE_FUNCS' in line and start_index is None:
            start_index = i
            print(start_index)
        elif start_index is not None and ']' in line:
            end_index = i
            print(end_index)
            break

    if start_index is not None and end_index is not None:
        del file_content[start_index:end_index + 1]

    with open(file_path, 'w') as file:
        file.writelines(file_content)

def refactor_files():
    """
    A function that removes all imports of fastcore or nbdev libraries as they include unsupported libraries
    """
    for foldername, subfolders, filenames in os.walk(os.path.join(dirname,'content')):
        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(foldername, filename)
                with open(file_path, 'r') as file:
                    file_content = file.readlines()
                with open(file_path, 'w') as file:
                    for line in file_content:
                        if any(unwanted_lib in line for unwanted_lib in ['fastcore', 'nbdev','nlp','rust']):
                            continue
                        elif 'patch(*args, **kwargs)(func)' in line:
                            file.write('        setattr(cls, func.__name__, func)')
                        elif 'class Session' in line:
                            file.write(f"{supported_ie_funcs}\n")
                            file.write(line)
                        else:
                            file.write(line)

if __name__ == '__main__':
    remove_predefined_ie_funcs(os.path.join(dirname,'content','rgxlog','session.py'))
    refactor_files()
