import re
from typing import List, Union

import numpy as np
import spacy
from spacy.tokens import Doc
from tqdm import tqdm

from stefutil.prettier import get_logger, ca, pl


__all__ = ['doc2tokens', 'TextPreprocessor']


_logger = get_logger(__name__)


# _pattern_space = re.compile(r'\s+')  # match one or more whitespace
_pattern_term = re.compile(r'\w+|[^\s\w]+')  # match one or more alphanumeric or non-whitespace-non-alphanumeric


def doc2tokens(sentence: str) -> List[str]:
    """
    Split sentence into tokens, split on any punctuation or whitespace
        e.g. `SOCCER-JAPAN` => [`SOCCER`, `-`, `JAPAN`]
    """
    return _pattern_term.findall(sentence)


class TextPreprocessor:
    """
    Pre-process documents in to lists of tokens

    By default, the document is broken into words, only non-stop words with alphabets are kept, and words are lemmatized & lowercased
    """
    # tags to remove from the text
    tags_ignore = [
        'ADV',  # adverbs, e.g. extremely, loudly, hard
        'PRON',  # pronouns, e.g. I, you, he
        'CCONJ',  # coordinating conjunctions, e.g. and, or, but
        'PUNCT',  # punctuation
        'PART',  # particle, e.g. about, off, up
        'DET',  # determiner, e.g. a, the, these
        'ADP',  # adposition, e.g. in, to, during
        'SPACE',  # space
        'NUM',  # numeral
        'SYM'  # symbol
    ]
    # from spacy import glossary
    # tag_name = 'ADV'
    # mic(glossary.explain(tag_name))
    # definitions linked in the source code https://github.com/explosion/spaCy/blob/master/spacy/glossary.py
    # http://universaldependencies.org/u/pos/

    nlp = None

    def __init__(self, tokenize_scheme: str = 'word', drop_tags: bool = False, verbose: bool = False):
        ca.check_mismatch(display_name='Tokenization Scheme', val=tokenize_scheme, accepted_values=['word', '2-gram', 'chunk'])
        self.tokenize_scheme = tokenize_scheme

        if TextPreprocessor.nlp is None:
            TextPreprocessor.nlp = self.nlp = spacy.load('en_core_web_sm')
        else:
            self.nlp = TextPreprocessor.nlp
        # self.nlp.add_pipe("merge_entities")
        # self.nlp.add_pipe("merge_noun_chunks")
        self.drop_tags = drop_tags
        self.verbose = verbose

    def keep_token(self, tok) -> bool:
        ret = not tok.is_stop and tok.is_alpha
        if self.drop_tags:
            ret = ret and tok.pos_ not in TextPreprocessor.tags_ignore
        return ret

    def __call__(self, texts: List[str]) -> List[List[str]]:
        assert isinstance(texts, list) and len(texts) > 0
        avg_tok_len = round(np.mean([len(doc2tokens(sent)) for sent in texts]), 2)
        ret = []
        it = tqdm(self.nlp.pipe(texts), desc='Preprocessing documents', unit=pl.i('doc'), total=len(texts))
        for doc in it:
            toks = self.process_single(doc)
            it.set_postfix(tok_len=pl.i(len(toks)))
            ret.append(toks)
        avg_tok_len_ = round(np.mean([len(toks) for toks in ret]), 2)
        if self.verbose:
            _logger.info(f'Preprocessing finished w/ average token length {pl.i(avg_tok_len)} => {pl.i(avg_tok_len_)}')
        return ret

    def process_single(self, text: Union[str, Doc]) -> List[str]:
        doc = self.nlp(text) if isinstance(text, str) else text

        # doc on attributes of a token at https://spacy.io/api/token
        # ignore certain tags & stop words, keep tokens w/ english letters, lemmatize & lowercase
        if self.tokenize_scheme == 'chunk':
            toks = [chunk.text for chunk in doc.noun_chunks]
        else:  # `word`, `2-gram`
            toks = [tok.lemma_.lower() for tok in doc if self.keep_token(tok)]
            if self.tokenize_scheme == '2-gram':
                toks = [' '.join(toks[i:i + 2]) for i in range(len(toks) - 1)]
        return toks


if __name__ == '__main__':
    from stefutil.prettier import mic

    def check_process():
        tp = TextPreprocessor()

        docs = ['hello world', 'japan-soccer.']
        lst_toks = tp(docs)
        mic(lst_toks)

        mic(tp.process_single('hello world'))
    check_process()
