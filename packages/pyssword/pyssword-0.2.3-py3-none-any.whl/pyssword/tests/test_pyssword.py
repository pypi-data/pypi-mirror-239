import itertools
import pytest
import re
import string

from .. import pyssword as m


@pytest.mark.parametrize('option', ['-h', '--help'])
def test_run_help(cli_invoker, option):
    result = cli_invoker(m.run, option)
    assert result.exit_code == 0
    assert result.output.startswith('Usage: run <options> <size>')


@pytest.mark.parametrize('option', ['-v', '--version'])
def test_run_version(cli_invoker, option):
    result = cli_invoker(m.run, option)
    assert result.exit_code == 0
    assert re.search(m.run.name + r', version (\d\.?){3}$', result.output.strip(), re.IGNORECASE)


@pytest.mark.parametrize('size', [
    *[pytest.param(i, marks=pytest.mark.xfail) for i in range(0, 10)],
    *range(10, 21),
])
def test_run_size(cli_invoker, size):
    result = cli_invoker(m.run, f'{size}')
    assert result.exit_code == 0
    assert len(result.output.strip()) == size


@pytest.mark.parametrize('option,alphabet_type', itertools.chain(
    # options with full punctuation
    list(itertools.product(
        [''],
        ['full']
    )),
    # options with digits
    list(itertools.product(
        ['-d', '--digits'],
        ['digits']
    )),
    # options with small punctuation
    list(itertools.product(
        ['-s', '--small'],
        ['small']
    )),
    # options with nopunctuation
    list(itertools.product(
        ['-n', '--nopunctuation'],
        ['nopunctuation']
    )),
    # options with small and nopunctuation
    list(itertools.product(
        itertools.product(
            ['-s', '--small'],
            ['-n', '--nopunctuation']
        ),
        ['nopunctuation']
    )),
    # options with digits, small and nopunctuation
    list(itertools.product(
        itertools.product(
            ['-d', '--digits'],
            ['-s', '--small'],
            ['-n', '--nopunctuation']
        ),
        ['digits']
    )),
))
@pytest.mark.parametrize('size', range(10, 30))
def test_run_mixed_options(cli_invoker, option, alphabet_type, size):
    alphabet          = m.ALPHABET[alphabet_type]
    negative_alphabet = ''.join([c for c in string.printable if c not in alphabet])

    option = ' '.join(option) if isinstance(option, (list, tuple, set)) else option
    result = cli_invoker(m.run, f'{option} {size}')
    output = result.output.strip()

    assert result.exit_code == 0
    assert len(output) == size

    assert not any(c not in alphabet for c in output), f"Invalid punctuations --> {tuple(c for c in output if c not in alphabet)} in {output}"
    assert not any(c in negative_alphabet for c in output), f"Invalid punctuations --> {tuple(c for c in output if c in negative_alphabet)} in {output}"


@pytest.mark.parametrize('option', ['-b', '--batch'])
@pytest.mark.parametrize('qty', [
    *[pytest.param(i, marks=pytest.mark.xfail) for i in range(-2, 1)],
    *range(1, 11),
])
@pytest.mark.parametrize('size', range(10, 30))
def test_run_batch(cli_invoker, option, qty, size):
    result = cli_invoker(m.run, f'{option} {qty} {size}')
    output = result.output.split()

    assert result.exit_code == 0
    assert len(output) == qty

    for item in output:
        assert len(item.strip()) == size
