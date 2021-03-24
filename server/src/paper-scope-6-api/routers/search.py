"""Router module to define `/search` routes.

"""

import json

from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..database.crud import get_article_by_id, get_articles_by_indices
from ..database.schemas import Article
from ..lda import model as lda_model


router = APIRouter(prefix='/search', tags=['search'])


@router.get('/', response_model=List[Article])
async def search(
    q: Optional[int] = None,
    best: Optional[int] = 50,
    db: Session = Depends(get_db),
):
    if not q:
        return []

    # Use ID to lookup index in corpus
    print(f'Querying for id: {q}')
    article = get_article_by_id(db, q)

    # Use index to look up similarity of associated, modeled document
    print(f'Getting similarities for index: {article.index}')
    corpus = lda_model['corpus']
    lda = lda_model['lda']
    sim_index = lda_model['index']

    sim_index.num_best = best
    results = sim_index[lda[corpus[article.index]]]

    # Use results to look up full article metadata
    print(f'Getting metadata for {len(results)} most similar results')
    indices = [result[0].item() for result in results]
    similarities = [result[1].item() for result in results]
    articles = get_articles_by_indices(db, indices)

    # Package response as relevant fields + similarity per result
    response = []
    for similarity, article in zip(similarities, articles):
        article_dict = {
            key: val for key, val in vars(article).items()
            if not key.startswith('_')
        }
        article_dict['groups'] = json.loads(article_dict['groups'])
        article_dict['similarity'] = similarity
        response.append(article_dict)

    return response
