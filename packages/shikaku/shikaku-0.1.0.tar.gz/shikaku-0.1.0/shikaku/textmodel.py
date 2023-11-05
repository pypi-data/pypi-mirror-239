"""Markov chain model."""

import re
from functools import cache
from typing import Any, Optional

import markovify
import matplotlib.axes
import matplotlib.pyplot as plt
import MeCab
import networkx as nx
import numpy as np
from japanize_matplotlib.japanize_matplotlib import FONT_NAME
from markovify.chain import BEGIN, END


class TextModel:
    """Text generation model by Markov chain."""

    def __init__(self, state_size: int = 2) -> None:
        """
        Construct a text generation model.

        Parameters
        ----------
        state_size : int, default 2
            Markov chain state size.

        """
        self._state_size = state_size
        self._model: Optional[markovify.Text] = None
        self._compiled_model: Optional[markovify.Text] = None

    def fit(self, text: str) -> None:
        """
        Train the model.

        Parameters
        ----------
        text : str
            Text for training.

        """
        # Normalize sentence endings.
        text = re.sub("[！？。]", r"\g<0>.", text)
        # Split the text into words.
        tagger = MeCab.Tagger("-Owakati")
        text = tagger.parse(text)

        # Build a model.
        model = markovify.Text(text.split("."), state_size=self._state_size)

        self._model = model
        self._compiled_model = None

    def generate(
        self,
        *,
        beginning: Optional[str] = None,
        strict: Optional[bool] = None,
        tries: Optional[int] = None,
        min_words: Optional[int] = None,
        max_words: Optional[int] = None,
    ) -> Optional[str]:
        """
        Generate a sentence.

        Parameters
        ----------
        beginning : str, optional
            Beginning word.
        strict : bool, optional
            Whether to strictly use the beginning word or not.
        tries : int, optional
            Number of tries to generate a valid sentence.
        min_words : int, optional
            Minimum number of words.
        max_words : int, optional
            Maximum number of words.

        Returns
        -------
        str or None
            Generated sentence.

        """
        if self._model is None:
            raise ValueError("model is not yet trained")

        if self._compiled_model is None:
            self._compiled_model = self._model.compile()
            # Monkey patch to generate Japanese sentences.
            self._compiled_model.word_join = lambda words: "".join(words)

        args: dict[str, Any] = {}
        if beginning is not None:
            args["beginning"] = beginning
        if strict is not None:
            args["strict"] = strict
        if tries is not None:
            args["tries"] = tries
        if min_words is not None:
            args["min_words"] = min_words
        if max_words is not None:
            args["max_words"] = max_words

        m = self._compiled_model
        if beginning is None:
            s = m.make_sentence(**args)
        else:
            s = m.make_sentence_with_start(**args)
        return s  # type: ignore[no-any-return]

    def plot(
        self,
        *,
        width: Optional[float] = None,
        height: Optional[float] = None,
        dpi: Optional[int] = None,
        iterations: Optional[int] = None,
    ) -> matplotlib.axes.Axes:
        """
        Plot the model.

        Parameters
        ----------
        width: float, optional
            Width of the figure.
        height: float, optional
            Height of the figure.
        dpi: int, optional
            Resolution of the figure.
        iterations : int, optional
            Maximum number of iterations to fix the layout.

        Returns
        -------
        matplotlib.axes.Axes :
            Matplotlib axes containing the plot.

        """
        if self._model is None:
            raise ValueError("model is not yet trained")

        if width is None:
            width = 7.5
        if height is None:
            height = width
        if iterations is None:
            iterations = 200

        g = nx.DiGraph()
        m = self._model.chain.model
        n = self._model.state_size
        beginning_state = (BEGIN,) * n
        endding_state = (END,)
        visited = set()

        @cache
        def get_state_name(state: tuple[str, ...]) -> str:
            if all(x == BEGIN for x in state):
                return "BEGIN"
            if END in state:
                return "END"
            s = list(state)
            while s[0] == BEGIN:
                del s[0]
            return ",".join(s)

        def traverse(state: tuple[str, ...]) -> None:
            if state in visited:
                return
            visited.add(state)

            g.add_node(get_state_name(state))

            if state not in m:
                return

            total_weight = sum(m[state].values())

            for next_word, weight in m[state].items():
                if next_word == END:
                    next_state = endding_state
                else:
                    next_state = state[1:] + (next_word,)  # type: ignore[assignment]
                traverse(next_state)
                g.add_edge(
                    get_state_name(state),
                    get_state_name(next_state),
                    probability=weight / total_weight,
                )

        traverse(beginning_state)

        pos = nx.spectral_layout(g)
        pos = nx.spring_layout(
            g,
            pos=pos,
            iterations=iterations,
        )

        if pos["BEGIN"][0] > pos["END"][0]:
            pos = {a: np.array((-x, y)) for a, (x, y) in pos.items()}
        if pos["BEGIN"][1] < pos["END"][1]:
            pos = {a: np.array((x, -y)) for a, (x, y) in pos.items()}

        _, ax = plt.subplots(figsize=(width, height), dpi=dpi)
        nx.draw_networkx(g, pos=pos, ax=ax, font_family=FONT_NAME)
        nx.draw_networkx_edge_labels(
            g,
            pos=pos,
            edge_labels={
                (u, v): f'{d["probability"]:.02f}' for u, v, d in g.edges(data=True)
            },
        )
        return ax
