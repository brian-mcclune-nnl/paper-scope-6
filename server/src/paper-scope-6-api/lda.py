import asyncio
import os
import tempfile

from functools import lru_cache
from typing import List

import aiofiles
import aiohttp
import numpy as np
import sklearn.manifold as sm

from gensim.corpora.mmcorpus import MmCorpus
from gensim.models.ldamodel import LdaModel
from gensim.similarities import SparseMatrixSimilarity
from pydantic import BaseSettings


model = {}
tasks = {}


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


async def get_corpus():
    model_settings = get_model_settings()
    tempdir = get_tempdir()

    models_uri = model_settings.models_uri
    mm_fname = model_settings.corpus
    mm_tmpdir = tempdir
    mm_urls = [f'{models_uri}/{mm_fname}{suffix}' for suffix in ('', '.index')]
    async with aiohttp.ClientSession() as session:
        for url in mm_urls:
            fname = url.rsplit('/', 1)[1]
            print(f'Downloading {url}...')
            async with session.get(url) as res:
                fpath = os.path.join(mm_tmpdir.name, fname)
                async with aiofiles.open(fpath, 'wb') as fh:
                    await fh.write(await res.read())

    return os.path.join(mm_tmpdir.name, mm_fname)


async def get_lda():
    model_settings = get_model_settings()
    tempdir = get_tempdir()

    models_uri = model_settings.models_uri
    lda_fname = model_settings.lda
    lda_tmpdir = tempdir
    lda_urls = [
        f'{models_uri}/{lda_fname}{suffix}'
        for suffix in ('', '.expElogbeta.npy', '.id2word', '.state')
    ]
    async with aiohttp.ClientSession() as session:
        for url in lda_urls:
            fname = url.rsplit('/', 1)[1]
            print(f'Downloading {url}...')
            async with session.get(url) as res:
                fpath = os.path.join(lda_tmpdir.name, fname)
                async with aiofiles.open(fpath, 'wb') as fh:
                    await fh.write(await res.read())

    return os.path.join(lda_tmpdir.name, lda_fname)


async def get_index():
    model_settings = get_model_settings()
    tempdir = get_tempdir()

    models_uri = model_settings.models_uri
    sim_fname = model_settings.index
    sim_tmpdir = tempdir
    sim_urls = [f'{models_uri}/{sim_fname}{suffix}' for suffix in ('', '.0')]
    async with aiohttp.ClientSession() as session:
        for url in sim_urls:
            fname = url.rsplit('/', 1)[1]
            print(f'Downloading {url}...')
            async with session.get(url) as res:
                fpath = os.path.join(sim_tmpdir.name, fname)
                async with aiofiles.open(fpath, 'wb') as fh:
                    await fh.write(await res.read())

    return os.path.join(sim_tmpdir.name, sim_fname)


async def schedule_model_downloads():
    tasks['corpus'] = asyncio.create_task(get_corpus())
    tasks['lda'] = asyncio.create_task(get_lda())
    tasks['index'] = asyncio.create_task(get_index())


async def load_corpus():
    if 'corpus' not in model:
        model['corpus'] = MmCorpus(await tasks['corpus'])
    return model['corpus']


async def load_lda():
    if 'lda' not in model:
        model['lda'] = LdaModel.load(await tasks['lda'])
    return model['lda']


async def load_index():
    if 'index' not in model:
        index_file = await tasks['index']
        model['index'] = SparseMatrixSimilarity.load(index_file)
        for shard in model['index'].shards:
            shard.dirname = os.path.dirname(index_file)
    return model['index']


def get_tsne_datasets(indices: List[int]):

    lda = model['lda']
    corpus = model['corpus']

    # Get topic weights for referenced article indices
    weights = []
    for idx in indices:
        weights.append([weight for _, weight in lda[corpus[idx]]])
    weights = np.nan_to_num(weights)

    # Record dominant topics for each article
    topics = np.argmax(weights, axis=1)

    # Do tSNE Dimension Reduction
    tsne = sm.TSNE(init='pca')
    embedding = tsne.fit_transform(weights)

    # Break values up into datasets by topic, format amenable to Chart.js
    unique_topics = np.unique(topics)

    datasets = []
    for topic in unique_topics:
        datasets.append([
            {'x': x, 'y': y} for x, y in embedding[topics == topic]
        ])

    return datasets
