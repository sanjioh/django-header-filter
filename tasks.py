import logging
import shutil
import sys
from pathlib import Path

from invoke import task

logging.getLogger().level = logging.DEBUG


@task
def cleanup_build_artifacts(c):
    for path in [
        *Path('.').glob('build'),
        *Path('.').glob('dist'),
        *Path('src').glob('*.egg-info'),
    ]:
        _rm_rf(path)


def _rm_rf(path):
    logging.info('removing %s', path)
    try:
        shutil.rmtree(path)
    except Exception:
        logging.exception('unexpected error')
        sys.exit(1)
