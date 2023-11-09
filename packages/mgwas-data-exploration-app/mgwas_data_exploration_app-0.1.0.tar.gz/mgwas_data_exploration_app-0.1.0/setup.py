# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mgwas_data_exploration_app']

package_data = \
{'': ['*'], 'mgwas_data_exploration_app': ['templates/*']}

install_requires = \
['matplotlib>=3.5.2,<4.0.0', 'pandas>=2.1.1,<3.0.0', 'scipy>=1.7.3,<2.0.0']

entry_points = \
{'console_scripts': ['mgwas-data-exploration-app = '
                     'mgwas_data_exploration_app.main:__main__']}

setup_kwargs = {
    'name': 'mgwas-data-exploration-app',
    'version': '0.1.0',
    'description': 'Data exploration app for large phenotypic datasets analyzed using mGWAS, originally developed for Scoary2',
    'long_description': '# mGWAS data exploration app\n\n> [!NOTE]\n> This tool was built for [Scoary2](https://github.com/MrTomRod/scoary-2)!\n\n## Description\n\nThis is a simple, static HTML/JS data exploration that allows you to explore the results of mGWAS software, particularly large phenotypic datasets.\n\n## Output\n\nThe app produces two types of HTML files that can be opened in any browser:\n\n- `overview.html`: A simple overview of all traits in the dataset.\n- `trait.html`: A more detailed view of a single trait.\n\nThe usage of this app is described on the Scoary2 [wiki](https://github.com/MrTomRod/scoary-2/wiki/App).\n\n## Installation\n\n1) Using pip: `pip install mgwas-data-exploration-app`\n2) Using docker: `docker pull troder/scoary-2`\n\n## How to prepare your data\n\n### Expected folder structure\n\nThe app expects the following folder structure:\n\n```\n.\n└── workdir\n    ├── summary.tsv\n    ├── traits.tsv\n    ├── tree.nwk\n    ├── isolate_info.tsv (optional)\n    └── traits\n        ├── trait1\n        │   ├── coverage-matrix.tsv\n        │   ├── meta.json\n        │   ├── result.tsv\n        │   └── values.tsv\n        ├── trait2\n        │   └── ...\n        └── ...\n```\n\n### Input arguments\n\n- `summary_df`: A table with the results of the mGWAS analysis. Rows: traits; columns: genes. (Separator: tab)\n- `traits_df`: A table with the metadata of the traits. Rows: traits; columns: metadata. (Separator: tab)\n- `workdir`: Folder where the mGWAS output must be located, exepect to find a folder \'traits\' with subfolders for each trait.\n- `is_numeric`: Whether the data is numeric or binary.\n- `app_config`: A JSON file that overwrites the default app config. See the default [config.json](mgwas_data_exploration_app/templates/config.json). (Optional)\n- `distance_metric`: The distance metric for the clustering of binary data. See the [scipy documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html).\n  (Binary data only; default: jaccard)\n- `linkage_method`: The linkage method for the clustering. One of [single, complete, average, weighted, ward, centroid, median]. (Default: ward)\n- `optimal_ordering`: Whether to use optimal ordering. See [scipy.cluster.hierarchy.linkage](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html) (Default: True)\n- `corr_scale`: Whether to scale numeric data before clustering. (Numeric data only; default: True)\n- `corr_method`: The correlation method for numeric data. One of [pearson, kendall, spearman]. (Numeric data only; default: pearson)\n- `dendrogram_x_scale`: The x-axis scale for the dendrogram. One of [linear, squareroot, log, symlog, logit]. (Default: linear)\n- `scores_x_scale`: The x-axis scale for the scores plot. One of [linear, manhattan]. (Default: linear)\n\n### Usage\n\nGet help with `mgwas-data-exploration-app --help` or reading the docstring of [main.py](mgwas_data_exploration_app/main.py).\n\n**Python**\n\n<details>\n\n  <summary>Click here to expand.</summary>\n\n```python\nfrom mgwas_data_exploration_app.main import mgwas_app\n\nmgwas_app(\n    summary_df="summary.tsv",  # or a pandas.DataFrame\n    traits_df="traits.tsv",  # or a pandas.DataFrame\n    workdir="out",\n    is_numeric=False,\n    app_config="app_config.json",  # or dict\n    distance_metric="jaccard",\n    linkage_method="ward",\n    optimal_ordering=True,\n    corr_scale=True,\n    corr_method="pearson",\n    dendrogram_x_scale="linear",\n    scores_x_scale="linear",\n)\n```\n\n</details>\n\n**Command line**\n\n<details>\n\n  <summary>Click here to expand.</summary>\n\n```shell\nmgwas-data-exploration-app \\\n    --summary summary.tsv \\\n    --traits traits.tsv \\\n    --workdir out \\\n    --is-numeric False \\\n    --app-config None \\\n    --distance-metric jaccard \\\n    --linkage-method ward \\\n    --optimal-ordering True \\\n    --corr-scale True \\\n    --corr-method pearson \\\n    --dendrogram-x-scale linear \\\n    --scores-x-scale linear\n```\n\n</details>\n\n# Credits\n\nThis project is built using the following libraries:\n\n- [PapaParse](https://www.papaparse.com/) for parsing the CSV files\n- [Bootstrap](https://getbootstrap.com/) for the layout\n- [SlimSelect](https://slimselectjs.com/) for the dropdowns\n- [DataTables](https://datatables.net/) and [jQuery](https://jquery.com/) for the tables\n- [Plotly](https://plotly.com/javascript/) for the plots\n- [Phylocanvas](https://phylocanvas.org/) for the phylogenetic trees\n- [Chroma.js](https://gka.github.io/chroma.js/) for the color scales\n- [Popper.js](https://popper.js.org/) for the tooltips\n',
    'author': 'MrTomRod',
    'author_email': 'roder.thomas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
