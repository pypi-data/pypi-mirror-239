import os
from typing import Union, Any, Mapping

import yaml
from omegaconf import OmegaConf

__all__ = [
  'read_config'
]

def expand(value: Any, root: Union[None, bytes, str, os.PathLike]) -> Any:
  if root is None:
    return value

  if not os.path.isdir(root):
    return value

  if isinstance(value, Mapping):
    return OmegaConf.create({
      k: expand(v, os.path.join(root, k))
      for k, v in value.items()
    })

  elif isinstance(value, str):
    path = os.path.join(root, f'{value}.yaml')
    return expand(OmegaConf.load(path), root)

  else:
    raise ValueError(f'Value for the hierarchical config ({root}) must be a string, got {value}.')

def cli_list(arguments: list[str], root):
  args = list()
  kwargs = list()

  for arg in arguments:
    if '=' in arg:
      k, arg = arg.split('=', maxsplit=1)
      value = yaml.load(arg, Loader=yaml.SafeLoader)
      ks = k.split('.')
      kwargs.append((ks, value))
    else:
      value = yaml.load(arg, Loader=yaml.SafeLoader)
      args.append(value)

  config = dict()
  kwargs_sorted = sorted(kwargs, key=lambda e: len(e[0]))

  for ks, value in kwargs_sorted:
    current = config

    *oks, key = ks
    for k in oks:
      if k not in current:
        current[k] = dict()

      assert isinstance(current[k], Mapping), f'key {k} exists and it is not a dict.'
      current = current[k]

    current[key] = expand(value, None if root is None else os.path.join(root, *ks))

  return args, config

def read_config(arguments, config: Union[None, bytes, str, os.PathLike]):
  if config is None:
    root = None
    config = OmegaConf.create()
  else:
    root = os.path.dirname(os.path.abspath(config))
    config = expand(OmegaConf.load(config), root)

  args, cli_arguments = cli_list(arguments, root)
  ### CLI arguments have priority
  merged = OmegaConf.merge(config, cli_arguments)

  return args, merged