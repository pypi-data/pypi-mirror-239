import os

import yaml

from .constant import def_logger
from .main_util import import_get, import_call

logger = def_logger.getChild(__name__)


def yaml_join(loader, node):
    """
    Joins a sequence of strings.

    :param loader: yaml loader.
    :type loader: yaml.loader.FullLoader
    :param node: node.
    :type node: yaml.nodes.Node
    :return: joined string.
    :rtype: str
    """
    seq = loader.construct_sequence(node)
    return ''.join([str(i) for i in seq])


def yaml_pathjoin(loader, node):
    """
    Joins a sequence of strings as a (file) path.

    :param loader: yaml loader.
    :type loader: yaml.loader.FullLoader
    :param node: node.
    :type node: yaml.nodes.Node
    :return: joined (file) path.
    :rtype: str
    """
    seq = loader.construct_sequence(node)
    return os.path.expanduser(os.path.join(*[str(i) for i in seq]))


def yaml_import_get(loader, node):
    """
    Imports module and get its attribute.

    :param loader: yaml loader.
    :type loader: yaml.loader.FullLoader
    :param node: node.
    :type node: yaml.nodes.Node
    :return: module attribute.
    :rtype: Any
    """
    entry = loader.construct_mapping(node, deep=True)
    return import_get(**entry)


def yaml_import_call(loader, node):
    """
    Imports module and call the module/function e.g., instantiation.

    :param loader: yaml loader.
    :type loader: yaml.loader.FullLoader
    :param node: node.
    :type node: yaml.nodes.Node
    :return: result of callable module.
    :rtype: Any
    """
    entry = loader.construct_mapping(node, deep=True)
    return import_call(**entry)


def yaml_getattr(loader, node):
    """
    Gets an attribute of the first argument.

    :param loader: yaml loader.
    :type loader: yaml.loader.FullLoader
    :param node: node.
    :type node: yaml.nodes.Node
    :return: module attribute.
    :rtype: Any
    """
    args = loader.construct_sequence(node, deep=True)
    return getattr(*args)


def yaml_simple_access(loader, node):
    """
    Obtains a value from a specified data

    :param loader: yaml loader.
    :type loader: yaml.loader.FullLoader
    :param node: node.
    :type node: yaml.nodes.Node
    :return: accessed object.
    :rtype: Any
    """
    entry = loader.construct_mapping(node, deep=True)
    data = entry['data']
    index_or_key = entry['index_or_key']
    return data[index_or_key]


def load_yaml_file(yaml_file_path, custom_mode=True):
    """
    Loads a yaml file optionally with convenient constructors.

    :param yaml_file_path: yaml file path.
    :type yaml_file_path: str
    :param custom_mode: if True, uses convenient constructors.
    :type custom_mode: bool
    :return: loaded PyYAML object.
    :rtype: Any
    """
    if custom_mode:
        yaml.add_constructor('!join', yaml_join, Loader=yaml.FullLoader)
        yaml.add_constructor('!pathjoin', yaml_pathjoin, Loader=yaml.FullLoader)
        yaml.add_constructor('!import_get', yaml_import_get, Loader=yaml.FullLoader)
        yaml.add_constructor('!import_call', yaml_import_call, Loader=yaml.FullLoader)
        yaml.add_constructor('!getattr', yaml_getattr, Loader=yaml.FullLoader)
        yaml.add_constructor('!simple_access', yaml_simple_access, Loader=yaml.FullLoader)
    with open(yaml_file_path, 'r') as fp:
        return yaml.load(fp, Loader=yaml.FullLoader)
