import os

def refactor_files():
    """
    A function that removes all imports of fastcore or nbdev libraries as they include unsupported libraries
    """
    for foldername, subfolders, filenames in os.walk(os.path.join(os.path.dirname(__file__),'content')):
        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(foldername, filename)
                with open(file_path, 'r') as file:
                    file_content = file.readlines()
                with open(file_path, 'w') as file:
                    for line in file_content:
                        if any(unwanted_lib in line for unwanted_lib in ['fastcore', 'nbdev']):
                            continue
                        elif 'patch(*args, **kwargs)(func)' in line:
                            file.write('        setattr(cls, func.__name__, func)')
                        else:
                            file.write(line)

if __name__ == '__main__':
    refactor_files()
