# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rossmann_toolbox', 'rossmann_toolbox.models', 'rossmann_toolbox.utils']

package_data = \
{'': ['*'],
 'rossmann_toolbox': ['weights/0.pt',
                      'weights/0.pt',
                      'weights/0.pt',
                      'weights/0.pt',
                      'weights/0.pt',
                      'weights/0.pt',
                      'weights/1.pt',
                      'weights/1.pt',
                      'weights/1.pt',
                      'weights/1.pt',
                      'weights/1.pt',
                      'weights/1.pt',
                      'weights/2.pt',
                      'weights/2.pt',
                      'weights/2.pt',
                      'weights/2.pt',
                      'weights/2.pt',
                      'weights/2.pt',
                      'weights/3.pt',
                      'weights/3.pt',
                      'weights/3.pt',
                      'weights/3.pt',
                      'weights/3.pt',
                      'weights/3.pt',
                      'weights/4.pt',
                      'weights/4.pt',
                      'weights/4.pt',
                      'weights/4.pt',
                      'weights/4.pt',
                      'weights/4.pt',
                      'weights/coredetector.pt',
                      'weights/coredetector.pt',
                      'weights/coredetector.pt',
                      'weights/coredetector.pt',
                      'weights/coredetector.pt',
                      'weights/coredetector.pt',
                      'weights/seqvec/uniref50_v2/options.json',
                      'weights/struct_ensemble/*'],
 'rossmann_toolbox.utils': ['hhdb/*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'atomium==1.0.9',
 'biopython==1.78',
 'captum==0.3.1',
 'conditional>=1.3,<2.0',
 'csb>=1.2.5,<2.0.0',
 'dgl==0.6.1',
 'greenlet<1',
 'overrides>=3.0,<4.0',
 'pandas==1.1.5',
 'seqvec==0.4.1',
 'torch>=1.13,<2.0']

setup_kwargs = {
    'name': 'rossmann-toolbox',
    'version': '0.1.1',
    'description': 'Prediction and re-engineering of the cofactor specificity of Rossmann-fold proteins',
    'long_description': '# Rossmann Toolbox\n\n<img src="https://github.com/labstructbioinf/rossmann-toolbox/blob/main/logo.png" align="center">\n\nThe Rossmann Toolbox provides two deep learning models for predicting the cofactor specificity of Rossmann enzymes based on either the sequence or the structure of the beta-alpha-beta cofactor binding motif.\n\n## Table of contents\n* [ Installation ](#Installation)\n* [ Usage ](#Usage)\n    + [Sequence-based approach](#sequence-based-approach)\n    + [Structure-based approach](#structure-based-approach)\n    + [EGATConv layer](#EGATConv-layer)\n* [ Remarks ](#Remarks)\n    + [How to cite](#how-to-cite)\n    + [Contact](#contact)\n    + [Funding](#funding)\n\n# Installation\n\nCreate a conda environment:\n```bash\nconda create --name rtb python=3.6.2\nconda activate rtb\n```\n\nInstall pip in the environment:\n```bash\nconda install pip\n```\n\nInstall rtb using `requirements.txt`:\n```bash\npip install -r requirements.txt\n```\n\n# Usage\n\n## Sequence-based approach\nThe input is a full-length sequence. The algorithm first detects <b>Rossmann cores</b> (i.e. the β-α-β motifs that interact with the cofactor) in the sequence and later evaluates their cofactor specificity:\n```python\nimport matplotlib.pylab as plt\nfrom rossmann_toolbox import RossmannToolbox\nrtb = RossmannToolbox(use_gpu=True)\n\n# Eample 1\n# The b-a-b core is predicted in the full-length sequence\n\ndata = {\'3m6i_A\': \'MASSASKTNIGVFTNPQHDLWISEASPSLESVQKGEELKEGEVTVAVRSTGICGSDVHFWKHGCIGPMIVECDHVLGHESAGEVIAVHPSVKSIKVGDRVAIEPQVICNACEPCLTGRYNGCERVDFLSTPPVPGLLRRYVNHPAVWCHKIGNMSYENGAMLEPLSVALAGLQRAGVRLGDPVLICGAGPIGLITMLCAKAAGACPLVITDIDEGRLKFAKEICPEVVTHKVERLSAEESAKKIVESFGGIEPAVALECTGVESSIAAAIWAVKFGGKVFVIGVGKNEIQIPFMRASVREVDLQFQYRYCNTWPRAIRLVENGLVDLTRLVTHRFPLEDALKAFETASDPKTGAIKVQIQSLE\'}\n\npreds = rtb.predict(data, mode=\'seq\', core_detect_mode=\'dl\', importance=False)\n\n# Eample 2\n# The b-a-b cores are provided by the user (WT vs mutant)\n\ndata = {\'seq_wt\': \'AGVRLGDPVLICGAGPIGLITMLCAKAAGACPLVITDIDEGR\', # WT, binds NAD\n        \'seq_mut\': \'AGVRLGDPVLICGAGPIGLITMLCAKAAGACPLVITSRDEGR\'} # D211S, I212R mutant, binds NADP\n\npreds, imps = rtb.predict(data, mode=\'core\', importance=True)\n\n# Example 3\n# Which residues contributed most to the prediction of WT as NAD-binding?\nseq_len = len(data[\'seq_wt\'])\nplt.errorbar(list(range(1, seq_len+1)),\n             imps[\'seq_wt\'][\'NAD\'][0], yerr=imps[\'seq_wt\'][\'NAD\'][1], ecolor=\'grey\')\n\n```\n\nFor more examples of how to use the sequence-based approach, see [example_minimal.ipynb](https://github.com/labstructbioinf/rossmann-toolbox/blob/main/examples/example_minimal.ipynb).\n\n## Structure-based approach\nStructure-based predictions are not currently available. We are working on a new version that will not only provide predictions, but also the ability to make specificity-shifting mutations.\n\n## EGATConv layer\n\nThe structure-based predictor includes an EGAT layer that deals with graph neural networks supporting edge features. The EGAT layer is available from DGL, and you can find more details about it in the [DGL documentation](https://docs.dgl.ai/en/0.8.x/generated/dgl.nn.pytorch.conv.EGATConv.html). For a detailed description of the EGAT layer and its usage, please refer to the supplementary materials of the [Rossmann Toolbox paper](https://academic.oup.com/bib/article/23/1/bbab371/6375059).\n\n# Remarks\n## How to cite?\nIf you find the `rossmann-toolbox` useful, please cite the paper:\n\n*Rossmann-toolbox: a deep learning-based protocol for the prediction and design of cofactor specificity in Rossmann fold proteins*\nKamil Kamiński, Jan Ludwiczak, Maciej Jasiński, Adriana Bukala, Rafal Madaj, Krzysztof Szczepaniak, Stanisław Dunin-Horkawicz\n*Briefings in Bioinformatics*, Volume 23, Issue 1, January 2022, [bbab371](https://doi.org/10.1093/bib/bbab371)\n\n## Contact\nIf you have any questions, problems or suggestions, please contact [us](https://ibe.biol.uw.edu.pl/en/835-2/research-groups/laboratory-of-structural-bioinformatics/).\n\n## Funding\nThis work was supported by the First TEAM program of the Foundation for Polish Science co-financed by the European Union under the European Regional Development Fund.\n',
    'author': 'Kamil Kaminski',
    'author_email': 'k.kaminski@cent.uw.edu.pl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/labstructbioinf/rossmann-toolbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
