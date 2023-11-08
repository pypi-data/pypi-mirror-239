import os

from flask import Flask, jsonify, send_file, g
from head_switcher import install_to_flask, load_from_package_resources

from dataset_sh.io import DatasetStorageManager
from dataset_sh.utils.files import filesize


def load_frontend_assets():
    try:
        return load_from_package_resources('dataset_sh.assets', 'app-ui.frontend')
    except FileNotFoundError as e:
        return {
            'index.html': 'dataset.sh web interface is disabled.'
        }


DISABLE_UI = os.environ.get('DISABLE_DATASET_APP_UI', '0').lower() in ['true', '1']


def create_app(manager=None, frontend_assets=None):
    if manager is None:
        manager = DatasetStorageManager()

    if frontend_assets is None and not DISABLE_UI:
        frontend_assets = load_frontend_assets()

    app = Flask(__name__, static_folder=None)

    @app.route('/api/dataset', methods=['GET'])
    def list_datasets():
        items = manager.list_datasets()
        return jsonify(items.model_dump(mode='json')), 200

    @app.route('/api/store', methods=['GET'])
    def list_stores():
        items = manager.list_dataset_stores()
        return jsonify(items.model_dump(mode='json')), 200

    @app.route('/api/dataset/<store_name>', methods=['GET'])
    def list_datasets_in_store(store_name):
        items = manager.list_datasets_in_store(store_name)
        return jsonify(items.model_dump(mode='json')), 200

    @app.route('/api/dataset/<store_name>/<dataset_name>/readme', methods=['GET'])
    def get_dataset_readme(store_name, dataset_name):
        return manager.get_dataset_readme(store_name, dataset_name), 200

    @app.route('/api/dataset/<store_name>/<dataset_name>/remote-source', methods=['GET'])
    def get_dataset_remote_source(store_name, dataset_name):
        source = manager.get_dataset_source_info(store_name, dataset_name)
        return jsonify(source.model_dump(mode='json')), 200

    @app.route('/api/dataset/<store_name>/<dataset_name>/meta', methods=['GET'])
    def get_dataset_meta(store_name, dataset_name):
        meta = manager.get_dataset_meta(store_name, dataset_name)
        fp = manager.get_dataset_file_path(store_name, dataset_name)
        meta['fileSize'] = filesize(fp)
        return jsonify(meta), 200

    @app.route('/api/dataset/<store_name>/<dataset_name>/collection/<collection_name>/sample', methods=['GET'])
    def get_collection_sample(store_name, dataset_name, collection_name):
        sample = manager.get_sample(store_name, dataset_name, collection_name)
        return jsonify(sample), 200

    @app.route('/api/dataset/<store_name>/<dataset_name>/collection/<collection_name>/code', methods=['GET'])
    def get_collection_code(store_name, dataset_name, collection_name):
        code = manager.get_usage_code(store_name, dataset_name, collection_name)
        return {'code': code}, 200

    @app.route('/api/dataset/<store_name>/<dataset_name>/file', methods=['GET'])
    def get_dataset_file(store_name, dataset_name):
        return send_file(
            manager.get_dataset_file_path(store_name, dataset_name),
            as_attachment=True,
            download_name=f"{store_name}_{dataset_name}.dataset"
        )

    install_to_flask(frontend_assets, app)

    return app


if __name__ == '__main__':  # pragma: no cover
    _frontend_assets = {
        'index.html': "dataset.sh web ui is disabled"
    }
    if not DISABLE_UI:
        _frontend_assets = load_frontend_assets()

    app = create_app(frontend_assets=_frontend_assets)
