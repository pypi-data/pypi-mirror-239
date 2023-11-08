import logging
from typing import Iterable, Optional, Union

import torch

from bonsait.cache import BaseClass, EmbeddingCache
from bonsait.configs import BONSAI_ACTIVITY_API, DEFAULT_MODEL
from bonsait.models import Encoder
from bonsait.utils.similarity_func import calc_cosine_similarity


class BonsaiTransformer:
    def __init__(
        self,
        model: Optional[Encoder] = None,
        device: str = "cpu",
    ) -> None:
        if model is None:
            logging.info(
                f"No model is provided, the default model {DEFAULT_MODEL} is used"
            )
            model = Encoder.from_sentence_transformer(model_name=DEFAULT_MODEL)
        self._model = model
        self._device = device

        self._source_class = None
        self._target_class = None

    def _validate_class(self, class_value: Iterable) -> None:
        if not isinstance(class_value, Iterable):
            raise ValueError("class_value must be a list of strings.")
        if not all(isinstance(item, str) for item in class_value):
            raise ValueError("Each item in class_value must be a string.")
        if not class_value:
            raise ValueError("class_value list cannot be empty.")

    def set_target_class(self, target_class: BaseClass = None):
        if target_class is None:
            target_class = BaseClass.from_bonsai(class_name="activity")
            print(
                f"get BONSAI activity classification as the default target classification from {BONSAI_ACTIVITY_API}"
            )
        self._validate_class(target_class.values)
        self._target_class = target_class

    def set_source_class(self, source_class: Union[str, list]):
        # TODO: add support for multiple source classes
        self._source_class = source_class

    def encode_source_class(self, source_class: str) -> torch.Tensor:
        self.set_source_class(source_class)
        array_source = self._model.encode(self._source_class).unsqueeze(0)
        return array_source

    def encode_target_class(
        self, target_class: BaseClass = None, cache: EmbeddingCache = EmbeddingCache()
    ):
        self.set_target_class(target_class)
        if not self._target_class:
            raise ValueError("target_class is not set")
        class_embedding_cached = cache.load_embedding(
            class_value=self._target_class.values
        )
        if class_embedding_cached is not None:
            print("Using cached classifications")
            return class_embedding_cached
        else:
            print(f"Start encoding {self._target_class.name}")
            # TODO: add parallelism here
            class_embedding = [
                self._model.encode(classification)
                for classification in self._target_class.values
            ]
            cache.save_embedding(
                encoding=class_embedding, class_value=self._target_class.values
            )
            return class_embedding

    def transform(
        self,
        source_class: Optional[str] = None,
        target_class: Optional[BaseClass] = None,
        similarity_func: Optional[callable] = None,
    ):
        """
        Computes the correspondence classification from target_class
        that is most similar to the source_class based on cosine similarity.
        """

        source_vector = self.encode_source_class(source_class)
        target_vectors = self.encode_target_class(target_class)

        # Stack all target vectors to create the target matrix
        target_matrix = torch.stack(target_vectors).to(self._device)
        if similarity_func is None:
            logging.info(
                f"No similarity func provided, using the default cosine similarity: {calc_cosine_similarity.__name__}"
            )
            similarity_func = calc_cosine_similarity
        similarity_scores = similarity_func(source_vector, target_matrix)
        idx_most_similar = torch.argmax(similarity_scores, dim=1).item()

        return self._target_class.values[idx_most_similar]
