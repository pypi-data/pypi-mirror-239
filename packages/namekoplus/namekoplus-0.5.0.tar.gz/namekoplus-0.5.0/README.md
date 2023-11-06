# namekoplus

[![Upload Python Package](https://github.com/Bryanthelol/namekoplus/actions/workflows/python-publish.yml/badge.svg?event=release)](https://github.com/Bryanthelol/namekoplus/actions/workflows/python-publish.yml)

A lightweight Python distributed microservice solution

## Installation

```shell
python3 -m pip install namekoplus
```


## CLI Usage

### Checkout Command

```shell
namekoplus --help
```

### Start a middleware that nameko depends on

```shell
namekoplus start -m rabbitmq
```

### Initialize a nameko service from templates

```shell
namekoplus init --directory <dir_name> --type <template_type>
```


## Detailed Usage

See Documents: 

- [English](https://legendary-sopapillas-e2626d.netlify.app/)
- [中文](https://doc.bearcatlog.com/)