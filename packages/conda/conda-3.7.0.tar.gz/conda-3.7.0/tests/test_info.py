from __future__ import print_function, absolute_import, division

from conda import config

from tests.helpers import run_conda_command


def test_info():
    conda_info_out, conda_info_err = run_conda_command('info')
    assert conda_info_err == ''
    for name in ['platform', 'conda version', 'root environment',
        'default environment', 'envs directories', 'package cache',
        'channel URLs', 'config file', 'is foreign system']:
        assert name in conda_info_out

    conda_info_e_out, conda_info_e_err = run_conda_command('info', '-e')
    assert 'root' in conda_info_e_out
    assert conda_info_e_err == ''

    conda_info_s_out, conda_info_s_err = run_conda_command('info', '-s')
    assert conda_info_s_err == ''
    for name in ['sys.version', 'sys.prefix', 'sys.executable', 'conda location',
        'conda-build', 'CIO_TEST', 'CONDA_DEFAULT_ENV', 'PATH', 'PYTHONPATH']:
        assert name in conda_info_s_out
    if config.platform == 'linux':
        assert 'LD_LIBRARY_PATH' in conda_info_s_out
    if config.platform == 'osx':
        assert 'DYLD_LIBRARY_PATH' in conda_info_s_out

    conda_info_all_out, conda_info_all_err = run_conda_command('info', '--all')
    assert conda_info_all_err == ''
    assert conda_info_out in conda_info_all_out
    assert conda_info_e_out in conda_info_all_out
    assert conda_info_s_out in conda_info_all_out
