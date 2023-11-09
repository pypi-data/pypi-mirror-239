#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'pydewey',
        version = '0.1.0',
        description = 'Dewey — a fast reproducible training automation tool for MLOps pipelines.',
        long_description = 'Dewey — a fast reproducible training automation tool for MLOps pipelines.\n\nDewey is a machine learning automation tool written to create consistent reproducible ways to train models \nin a framework agnostic way. It allows providing a training specification, and the Dewey training framework\ntakes care of all of the standard boilerplate code involving monitoring, metrics, setting up checkpoints, \nremote caching and more. Please note that this tool is in early stages of development and is prone to rapid\nupdates and breaking API changes.\n',
        long_description_content_type = None,
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        keywords = '',

        author = 'David Buzinski',
        author_email = 'davidbuzinski@gmail.com',
        maintainer = 'David Buzinski',
        maintainer_email = 'davidbuzinski@gmail.com',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/dbuzinski/dewey',
        project_urls = {
            'Bug Tracker': 'https://github.com/dbuzinski/dewey/issues',
            'Source Code': 'https://github.com/dbuzinski/dewey'
        },

        scripts = ['scripts/dwy'],
        packages = [],
        namespace_packages = [],
        py_modules = [
            'dewey.DataSpecification',
            'dewey.ModelTrainer',
            'dewey.ModelTrainerPlugin',
            'dewey.TrainingManager',
            'dewey.internal.PluginData',
            'dewey.internal.PluginManager',
            'dewey.internal.RunData',
            'dewey.internal.TrainingOperator',
            'dewey.plugins.core.TensorBoardPlugin',
            'dewey.plugins.core.TrainingProgressPlugin',
            'dewey.plugins.pytorch.PytorchCheckpointPlugin',
            'dewey.plugins.pytorch.PytorchCorePlugin',
            'dewey.plugins.tensorflow.TensorflowCheckpointPlugin',
            'dewey.plugins.tensorflow.TensorflowCorePlugin'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '>=3.11',
        obsoletes = [],
    )
