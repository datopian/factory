import os
from shutil import copyfile


def copy_configs(config_path=os.path.expanduser('~/.config/datahub')):
    if not os.path.exists(config_path):
        os.makedirs(config_path)

    def walklevel(some_dir, level=1):
        some_dir = some_dir.rstrip(os.path.sep)
        assert os.path.isdir(some_dir)
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]

    for root, dirs, files in walklevel('datasets'):
        if files:
            file = files[0]
            username = root.split('/')[-1]
            if not file.endswith('.enc'):
                copyfile(os.path.join(root,file), os.path.join(config_path, '%s.%s' %(file, username)))
                # Default config for core
                if username == 'core':
                    copyfile(os.path.join(root,file), os.path.join(config_path, file))

if __name__ == '__main__':
    copy_configs()
