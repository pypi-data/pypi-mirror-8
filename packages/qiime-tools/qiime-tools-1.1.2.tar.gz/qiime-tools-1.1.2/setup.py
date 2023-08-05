from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

requires = ['fuzzpy >= 0.4.2', 'matplotlib >= 1.0.0', 'biopython >= 1.60']

scripts = ['bin/PCoA_bubble.py', 'bin/biom_relative_abundance.py', 'bin/filter_rep_set.py',
           'bin/biom_phyla_summary.py', 'bin/filter_keep_otus_by_sample.py',
           'bin/multi_parallel_pick_otus.py', 'bin/otu_to_tax_name.py',
           'bin/prune_otus.py', 'bin/split_sequence_data.py',
           'bin/assign_taxonomy_by_blast_result.py', 'bin/condense_workflow.py',
           'bin/iTol.py', 'bin/multi_qsub.py', 'bin/pick_otus_condense.py',
           'bin/transpose_biom.py', 'bin/barcode_filter.py', 'bin/merge_otu_results.py',
           'bin/otu_condense.py', 'bin/primer_average.py', 'bin/sanger_qiimify.py']

setup(
  name='qiime-tools',
  version='1.1.2',
  description='Useful additions to the QIIME analysis pipeline including tools for data visualization and cluster-computing.',
  author='Shareef M. Dabdoub',
  author_email='dabdoub.2@osu.edu',
  packages=['qiime_tools', 'qiime_tools.test'],
  url='https://github.com/smdabdoub/qiime-tools',
  #install_requires=requires,
  scripts=scripts,
  data_files=[('data', ['data/pbs_job_template.pbs', 'data/slurm_job_template.sbatch'])],
  keywords=['bioinformatics', 'QIIME', 'microbial ecology', '16S', 'microbiology'],
  license='MIT',
  classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
    ],
)
