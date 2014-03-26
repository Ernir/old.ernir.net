import os, re


def get_old_vtp_files():
    module_dir = os.path.dirname(os.path.abspath(__file__))
    vtp_dir = os.path.join(module_dir, "static/content/VtP/")
    file_names = natural_sort_reverse(os.listdir(vtp_dir))
    return file_names[1:]


# 95% based on http://stackoverflow.com/a/4836734/1675015
def natural_sort_reverse(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key, reverse=True)