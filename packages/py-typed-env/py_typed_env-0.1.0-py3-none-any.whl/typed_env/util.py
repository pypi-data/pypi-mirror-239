import os


def get_file_descending(name: str):
    root = os.path.abspath(".").split(os.path.sep)[0] + os.path.sep
    curr = os.path.abspath(".")
    while curr != root:
        if name in os.listdir(curr):
            res = os.path.join(curr, name)
            if os.access(res, os.R_OK):
                return res
        curr = os.path.spe.join(curr.split(os.path.sep)[:-2]) + os.path.sep

    return None
