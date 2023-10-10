import os
modules_to_remove = ['fastcore', 'nbdev', 'nlp', 'rust']
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
        elif start_index is not None and ']' in line:
            end_index = i
            break

    if start_index is not None and end_index is not None:
        # Delete the old list of PREDEFINED_IE_FUNCS and replace with new one
        del file_content[start_index:end_index + 1]
        file_content.insert(start_index,supported_ie_funcs)

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
                        # Don't include any imports of unwanted libraries e.g nbdev/fastcore...
                        if 'import' in line and any(module in line for module in modules_to_remove):
                            continue
                        # Override the patch line in `patch_method` as we don't import fastcore anymore
                        elif 'patch(*args, **kwargs)(func)' in line:
                            file.write('        setattr(cls, func.__name__, func)')
                        else:
                            file.write(line)

if __name__ == '__main__':
    remove_predefined_ie_funcs(os.path.join(dirname,'content','rgxlog','session.py'))
    refactor_files()
