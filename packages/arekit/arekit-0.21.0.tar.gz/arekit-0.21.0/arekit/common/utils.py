import collections
from os import makedirs
from os.path import join, dirname, exists
import numpy as np
from tqdm import tqdm


def get_random_uniform_with_fixed_seed(vector_size, seed):
    """
    Generates random vector by specific initial 'seed' value
    """
    assert(isinstance(vector_size, int))
    assert(isinstance(seed, int))
    np.random.seed(seed)
    return np.random.uniform(-1, 1, vector_size)


def get_random_normal_distribution(vector_size, seed, loc, scale):
    assert(isinstance(vector_size, int))
    assert(isinstance(seed, int))
    np.random.seed(seed)
    return np.random.normal(loc=loc, scale=scale, size=vector_size)


def create_dir_if_not_exists(filepath):
    dir = dirname(filepath)
    if not exists(dir):
        makedirs(dir)


def filter_whitespaces(terms):
    return [term.strip() for term in terms if term.strip()]


def split_by_whitespaces(text):
    """
    Assumes to perform a word separation including a variety of space entries.
    In terms of the latter we consider any whitespace separator.
    """
    assert(isinstance(text, unicode))
    return text.split()


def progress_bar_defined(iterable, total, desc="", unit="it"):
    return tqdm(iterable=iterable,
                total=total,
                desc=desc,
                ncols=120,
                position=0,
                leave=True,
                unit=unit,
                miniters=total / 200)


def progress_bar_iter(iterable, desc="", unit='it'):
    return tqdm(iterable=iterable,
                desc=desc,
                position=0,
                leave=True,
                ncols=120,
                unit=unit)


def join_dir_with_subfolder_name(subfolder_name, dir):
    """ Returns subfolder in in directory
    """
    assert(isinstance(subfolder_name, unicode))
    assert(isinstance(dir, unicode))

    target_dir = join(dir, u"{}/".format(subfolder_name))
    return target_dir


def check_files_existance(filepaths, logger):
    assert(isinstance(filepaths, collections.Iterable))

    result = True
    for filepath in filepaths:
        existed = exists(filepath)
        logger.info("Check existance [{is_existed}]: {fp}".format(is_existed=existed, fp=filepath))
        if not existed:
            result = False

    return result

