import os


def pytest_configure(config):
    os.environ["USE_FALLBACK"] = "1"
    config.option.asyncio_mode = "auto"
