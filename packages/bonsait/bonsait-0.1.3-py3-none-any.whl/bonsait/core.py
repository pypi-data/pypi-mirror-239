import logging
from typing import Iterable, List, Optional

import torch

from bonsait.class_repo import BaseClass, EmbeddingCache
from bonsait.configs import BONSAI_ACTIVITY_API, DEFAULT_MODEL
from bonsait.model_repo import Encoder
from bonsait.utils.similarity_func import calc_cosine_similarity


class BonsaiTransformer:
    def __init__(
        self,
        source_class: str | None = None,
        target_class: BaseClass | None = None,
        model: Optional[Encoder] = None,
        device: str = "cpu",
    ) -> None:
        self._source_class = source_class
        self._target_class = target_class
        if target_class is None:
            self._target_class = BaseClass.from_bonsai(class_name="activity")
            print(
                f"get BONSAI activity classification as the default target classification from {BONSAI_ACTIVITY_API}"
            )

        if model is None:
            logging.info(
                f"No model is provided, the default model {DEFAULT_MODEL} is used"
            )
            model = Encoder.from_sentence_transformer(model_name=DEFAULT_MODEL)
        self._model = model
        self._device = device

    @property
    def target_class(self) -> Optional[List[str]]:
        return self._target_class

    @target_class.setter
    def target_class(self, value: Iterable[str]):
        if not isinstance(value, Iterable):
            raise ValueError("target_class must be a list of strings.")
        if not all(isinstance(item, str) for item in value):
            raise ValueError("Each item in target_class must be a string.")
        if not value:
            raise ValueError("target_class list cannot be empty.")
        self._target_class = value

    @property
    def source_class(self) -> Optional[str]:
        return self._source_class

    @source_class.setter
    def source_class(self, value: str):
        self._source_class = value

    def encode_source_class(self):
        array_source = self._model.encode(self._source_class).unsqueeze(0)
        return array_source

    def encode_target_class(self):
        if not self._target_class:
            raise ValueError("target_class is not set")

        encoded_class = EmbeddingCache().load_embedding(
            class_value=self._target_class.values
        )
        if encoded_class:
            print("Using cached classifications")
            return encoded_class
        else:
            print(f"Start encoding {self._target_class.name}")
            encoded_classes = [
                self._model.encode(classification)
                for classification in self._target_class.values
            ]
            EmbeddingCache().save_embedding(
                encoding=encoded_class, class_value=self._target_class.values
            )
            return encoded_classes

    def transform(
        self,
        similarity_func: callable = None,
    ):
        """
        Computes the correspondence classification from target_class
        that is most similar to the source_class based on cosine similarity.
        """

        source_vector = self.encode_source_class()
        target_vectors = self.encode_target_class()

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
