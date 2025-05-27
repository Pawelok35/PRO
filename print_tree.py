import os

def print_tree(startpath, max_depth=3, prefix=''):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        if level > max_depth:
            continue
        indent = '│   ' * level + '├── '
        print(f"{indent}{os.path.basename(root)}/")
        subindent = '│   ' * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

if __name__ == "__main__":
    print_tree(os.getcwd())
