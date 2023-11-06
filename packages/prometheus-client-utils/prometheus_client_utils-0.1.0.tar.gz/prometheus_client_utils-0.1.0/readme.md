# Utils for prometheus-client

Poetry plugin to set package version based on git tag.

[![PyPI](https://img.shields.io/pypi/v/poetry-git-version-plugin)](https://pypi.org/project/prometheus-client-utils/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/prometheus-client-utils)](https://pypi.org/project/prometheus-client-utils/)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/prometheus-client-utils)](https://gitlab.com/rocshers/python/prometheus-client-utils)

[![Test coverage](https://codecov.io/gitlab/rocshers:python/prometheus-client-utils/graph/badge.svg?token=3C6SLDPHUC)](https://codecov.io/gitlab/rocshers:python/prometheus-client-utils)
[![Downloads](https://static.pepy.tech/badge/prometheus-client-utils)](https://pepy.tech/project/prometheus-client-utils)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/prometheus-client-utils)](https://gitlab.com/rocshers/python/prometheus-client-utils)

## Functionality

- Push clients
  - pushgateway
  - statsd

## Quick start

```bash
pip install prometheus-client-utils
```

## Example

```python
import asyncio
from random import randint

from prometheus_client import REGISTRY, Counter, Histogram

from prometheus_client_utils.collectors import AsyncioCollector
from prometheus_client_utils.push_clients import PushGatewayClient

m_count = Counter('iters', 'count')
m_histogram = Histogram('iters_time', 'histogram')

semaphore = asyncio.Semaphore(50)


@m_histogram.time()
async def inner():
    async with semaphore:
        m_count.inc()
        await asyncio.sleep(randint(0, 10))


async def main():
    loop = asyncio.get_running_loop()

    REGISTRY.register(AsyncioCollector(loop))

    push_client = PushGatewayClient('localhost', 'test')
    push_client.schedule_push(5, loop)

    for i in range(10000):
        await asyncio.sleep(i / 100)
        loop.create_task(inner())


if __name__ == '__main__':
    asyncio.run(main())
```

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/poetry-git-version-plugin/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/poetry-git-version-plugin>

Before adding changes:

```bash
make install-dev
```

After changes:

```bash
make format test
```
