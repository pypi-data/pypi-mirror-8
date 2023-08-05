__author__ = 'yarnaid'


import utils
import copy
import model

config = utils.load_config()


def get_ft(input_row):
    centered_row = utils.center_row(input_row)
    centered_row.time_var = utils.get_fft_freqs(centered_row)
    return utils.get_ft_final(centered_row)


def get_ft_level(input_row):
    if input_row.X_q is None:
        input_row.X_q = utils.get_X_q(input_row.time_var)
    return utils.get_fft_level(input_row)


def get_pg_level(input_row):
    return utils.get_fft_level(input_row)

def get_pg(input_row):
    centered_row = get_ft(input_row)
    res_pg = centered_row.values.size ** (-2) * abs(centered_row.values) ** 2
    res = copy.deepcopy(input_row)
    res.values = res_pg
    return res


def get_acf(input_row):
    res = utils.get_acf(input_row)
    return res


def get_acf_level(input_row):
    return utils.get_acf_level(input_row)


def get_scalogram(input_row):
    return utils.get_scalogram_final(input_row)


def get_scales(input_row):
    return utils.get_scalogram_scales(input_row)


def get_sf(input_row):
    return utils.get_sf(input_row)


def get_scalogram_levels(input_row):
    return utils.get_scalogram_level(input_row)


def get_sf_level(input_row):
    return utils.get_sf_level(input_row)

