#!/usr/bin/env python3

import json
import os
from dataclasses import dataclass
from typing import Optional

import click

from dataset_sh.core import DatasetFileMeta
from dataset_sh.dep import DatasetDependencies, locate_dep_file, get_dataset_url_for_remote_host
from dataset_sh.io import DatasetStorageManager, read_file, import_remote as io_import_remote
from dataset_sh.typing.codegen import CodeGenerator
from dataset_sh.utils.misc import parse_dataset_name


@dataclass
class AppCtx:
    base: Optional[str] = None


@click.group(name='dataset.sh')
@click.option('--base', '-b', envvar='DATASET_SH_STORAGE_BASE', help='location of base storage folder.',
              type=click.Path())
@click.pass_context
def cli(ctx, base):
    """Simple CLI tool with subcommands"""
    ctx.obj = DatasetStorageManager(store_base=base)


@click.command(name='print')
@click.argument('name')
@click.argument('action', type=click.Choice(['list-collections', 'readme', 'code', 'sample']))
@click.option('--collection', '-c', help='which collection')
@click.pass_obj
def print_info(manager: DatasetStorageManager, name, action, collection):
    """
    print dataset information
    """
    username, dataset_name = parse_dataset_name(name)

    if action in [
        'code',
        'sample',
    ] and (collection is None or collection == ''):
        click.echo('You must provide a collection using --collection/-c')
        raise click.Abort()

    if action == 'list-collections':
        meta = manager.get_dataset_meta(username, dataset_name)
        meta = DatasetFileMeta(**meta)

        click.echo(f'Total collections: {len(meta.collections)}')
        for coll in meta.collections:
            click.echo(coll.name)

    elif action == 'readme':
        readme = manager.get_dataset_readme(username, dataset_name)
        click.echo(readme)

    elif action == 'code':
        code = manager.get_usage_code(username, dataset_name, collection_name=collection)
        click.echo(code)

        meta = manager.get_dataset_meta(username, dataset_name)
        meta = DatasetFileMeta(**meta)
        coll = meta.find_collection(collection)

        if coll is not None:
            loader_code = CodeGenerator.generate_loader_code(
                username,
                dataset_name,
                collection,
                coll.data_schema.entry_point)
            click.echo('\n\n')
            click.echo(loader_code)

    elif action == 'sample':
        sample = manager.get_sample(username, dataset_name, collection)
        click.echo(json.dumps(sample, indent=2))


@click.command(name='inspect-file')
@click.argument('filepath', type=click.Path())
@click.argument('action', type=click.Choice(['list-collections', 'code', 'sample']))
@click.option('--collection', '-c', help='which collection.')
@click.pass_obj
def inspect_file(manager: DatasetStorageManager, filepath, action, collection):
    """
    parse dataset file and print out information
    """

    if action in [
        'code',
        'sample',
    ] and (collection is None or collection == ''):
        click.echo('You must provide a collection using --collection/-c')
        raise click.Abort()

    with read_file(filepath) as reader:
        if action == 'list-collections':
            collections = reader.collections()
            click.echo(f'Total collections: {len(collections)}')
            for coll in collections:
                click.echo(coll)

        elif action == 'code':
            coll = reader.collection(collection)
            code = coll.code_usage()
            schema = coll.config.data_schema
            loader_code = CodeGenerator.generate_file_loader_code(filepath, collection, schema.entry_point)
            click.echo(code)
            click.echo('\n\n')
            click.echo(loader_code)

        elif action == 'sample':
            sample = reader.collection(collection).top()
            click.echo(json.dumps(sample, indent=2))


@click.command(name='remove')
@click.argument('name')
@click.option('--force', '-f', default=False, help='Force remove dataset without confirmation.', is_flag=True)
@click.pass_obj
def remove(manager: DatasetStorageManager, name, force):
    """remove managed dataset"""
    username, dataset_name = parse_dataset_name(name)
    if not force:
        confirmation = click.prompt(f'Are you sure you want to remove dataset {name}? (y/N): ')
        if confirmation.lower() == 'y':
            manager.delete_dataset(username, dataset_name)
    else:
        manager.delete_dataset(username, dataset_name)


@click.command(name='list')
@click.option('--store', '-s', help='select dataset store space to list.')
@click.pass_obj
def list_datasets(manager: DatasetStorageManager, store):
    """list datasets"""
    items = []
    if store:
        items = manager.list_datasets_in_store(store).items
    else:
        items = manager.list_datasets().items

    click.echo(f'\nFound {len(items)} datasets:\n')
    items = sorted(items, key=lambda x: f'{x.datastore} / {x.dataset}')
    for item in items:
        click.echo(f'  {item.datastore}/{item.dataset}')
    click.echo('')


@click.command(name='import')
@click.argument('name')
@click.option('--url', '-u', help='url of the dataset file to import')
@click.option('--file', '-f', help='local file path of the dataset file to import', type=click.Path())
@click.option('--host', '-h', help='host server url', default='https://export.dataset.sh/dataset')
@click.pass_obj
def import_(manager, name, url, file, host):
    """import dataset from url or file"""
    if url is not None and file is not None:
        click.echo('Usage: import [NAME] -u [url]')
        click.echo('Usage: import [NAME] -f [file-path]')
        raise click.Abort()

    username, dataset_name = parse_dataset_name(name)

    if url is not None:
        click.echo(f'importing remote file from {url}')
        manager.import_url(url, username, dataset_name)
    elif file is not None:
        click.echo(f'importing local file from {file}')
        manager.import_file(file, username, dataset_name)
    else:
        remote_url = get_dataset_url_for_remote_host(host, name)
        username, dataset = parse_dataset_name(name)
        manager.import_url(remote_url, username, dataset)


@click.command(name='edit')
@click.argument('name')
@click.pass_obj
def edit(manager, name):
    """Edit readme of a dataset"""
    username, dataset_name = parse_dataset_name(name)
    readme = manager.get_dataset_readme(username, dataset_name)
    editor = os.environ.get('EDITOR', 'vim')
    edited_readme = click.edit(readme, editor=editor)
    if edited_readme:
        manager.update_dataset_readme(username, dataset_name, edited_readme)


@click.command(name='import-remote')
@click.argument('name')
@click.option('--target', '-t', help='local name for the imported dataset', default=None)
@click.pass_obj
def import_remote(manager, name, target):
    """Edit readme of a dataset"""
    if target is None:
        target = name
    io_import_remote(name, rename=target, store_base=manager.base)


@click.command(name='install')
@click.option('--dataset', '-d', help='add a dataset', default=None)
@click.option('--host', '-h', help='host', default='https://export.dataset.sh/dataset')
@click.option('--project', '-p', 'project_file', help='project file', default=None)
@click.pass_obj
def install_project(manager, dataset, host, project_file):
    """import all dataset from a dataset project file"""
    if project_file is None:
        project_file = locate_dep_file(os.getcwd())

    project_def = DatasetDependencies.read_from_file(project_file)

    for g in project_def.groups:
        for name, url in g.to_url_list():
            username, dataset_name = parse_dataset_name(name)
            manager.import_url(url, username, dataset_name, exist_ok=True)

    if dataset is not None:
        remote_url = get_dataset_url_for_remote_host(host, dataset)
        username, dataset_name = parse_dataset_name(dataset)
        manager.import_url(remote_url, username, dataset_name, exist_ok=True)


@click.command(name='init')
@click.option('--project', '-p', 'project_file', help='project file', default=None)
@click.pass_obj
def init_project(manager, project_file):
    """create an empty dataset.list file at current folder"""
    project_def = DatasetDependencies()
    if project_file is None:
        project_file = './dataset.list'
    if os.path.exists('./dataset.list'):
        click.echo('dataset.list already exists.')
        return
    else:
        project_def.write_to_file(project_file)


# Add subcommands to the main command
cli.add_command(print_info)
cli.add_command(remove)
cli.add_command(list_datasets)
cli.add_command(inspect_file)
cli.add_command(import_)
cli.add_command(import_remote)
cli.add_command(edit)

cli.add_command(install_project)
cli.add_command(init_project)

if __name__ == '__main__':  # pragma: no cover
    cli()
