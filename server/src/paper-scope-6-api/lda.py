import os
import tempfile

from functools import lru_cache

import requests

from gensim.corpora.mmcorpus import MmCorpus
from gensim.models.ldamodel import LdaModel
from gensim.similarities import SparseMatrixSimilarity
from pydantic import BaseSettings


model = {}


class ModelSettings(BaseSettings):
    models_uri: str
    corpus: str
    lda: str
    index: str

    class Config:
        env_file = '.env.local'

    def __hash__(self):
        return hash(tuple(item for item in self.dict().items()))


@lru_cache
def get_model_settings():
    return ModelSettings()


@lru_cache
def get_tempdir():
    return tempfile.TemporaryDirectory()


def get_corpus():
    model_settings = get_model_settings()
    tempdir = get_tempdir()

    models_uri = model_settings.models_uri
    mm_fname = model_settings.corpus
    mm_tmpdir = tempdir
    mm_urls = [f'{models_uri}/{mm_fname}{suffix}' for suffix in ('', '.index')]
    for url in mm_urls:
        fname = url.rsplit('/', 1)[1]
        print(f'Downloading {url}...')
        res = requests.get(url)
        with open(os.path.join(mm_tmpdir.name, fname), 'wb') as fh:
            fh.write(res.content)

    return MmCorpus(os.path.join(mm_tmpdir.name, mm_fname))


@lru_cache
def get_lda():
    model_settings = get_model_settings()
    tempdir = get_tempdir()

    models_uri = model_settings.models_uri
    lda_fname = model_settings.lda
    lda_tmpdir = tempdir
    lda_urls = [
        f'{models_uri}/{lda_fname}{suffix}'
        for suffix in ('', '.expElogbeta.npy', '.id2word', '.state')
    ]
    for url in lda_urls:
        fname = url.rsplit('/', 1)[1]
        print(f'Downloading {url}...')
        res = requests.get(url)
        with open(os.path.join(lda_tmpdir.name, fname), 'wb') as fh:
            fh.write(res.content)

    return LdaModel.load(os.path.join(lda_tmpdir.name, lda_fname))


@lru_cache
def get_index():
    model_settings = get_model_settings()
    tempdir = get_tempdir()

    models_uri = model_settings.models_uri
    sim_fname = model_settings.index
    sim_tmpdir = tempdir
    sim_urls = [f'{models_uri}/{sim_fname}{suffix}' for suffix in ('', '.0')]
    for url in sim_urls:
        fname = url.rsplit('/', 1)[1]
        res = requests.get(url)
        print(f'Downloading {url}...')
        with open(os.path.join(sim_tmpdir.name, fname), 'wb') as fh:
            fh.write(res.content)

    index_path = os.path.join(sim_tmpdir.name, sim_fname)
    index = SparseMatrixSimilarity.load(index_path)
    for shard in index.shards:
        shard.dirname = sim_tmpdir.name
    return index


def load_model():
    model['corpus'] = get_corpus()
    model['lda'] = get_lda()
    model['index'] = get_index()
