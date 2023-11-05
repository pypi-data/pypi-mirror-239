import logging
from typing import Iterable, List, Optional

import requests
import torch
from sentence_transformers import SentenceTransformer
from transformers import BertModel, BertTokenizer

from bonsait.configs import BONSAI_ACTIVITY_API, BONSAI_API_KEY, DEFAULT_MODEL
from bonsait.utils.similarity_func import calc_cosine_similarity


def get_bonsai_activity_classification(
    url: str = BONSAI_ACTIVITY_API, key: str = BONSAI_API_KEY
) -> Iterable[str]:
    """Get BONSAI's activity classification using its API

    Parameters
    ----------
    url : str, optional
        url for bonsai activity classification, by default BONSAI_ACTIVITY_API

    Returns
    -------
    Iterable[str]
        a list of activity classifications
    """

    try:
        headers = {"Authorization": f"Token {BONSAI_API_KEY}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        activities_data = response.json()

        activity_names = [activity["description"] for activity in activities_data]
        print(f"successfully fetched activity classifications from {url}")
        return activity_names
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error Connecting: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout Error: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error: {req_err}")  # Ambiguous error
    except Exception as err:
        print(f"An error occurred: {err}")  # Other errors

    return []


class Encoder:
    def __init__(self, encoder=None, tokenizer=None, device: str = "cpu") -> None:
        self.encoder = encoder
        self.tokenizer = tokenizer
        self.device = device
        if encoder:
            self.encoder = self.encoder.to(self.device)

    @classmethod
    def from_sentence_transformer(cls, model_name: str, device: str = "cpu"):
        encoder = SentenceTransformer(model_name)
        return cls(encoder, device=device)

    @classmethod
    def from_hugging_face(cls, model_name: str, device: str = "cpu"):
        tokenizer = BertTokenizer.from_pretrained(model_name)
        encoder = BertModel.from_pretrained(model_name)
        return cls(encoder, tokenizer, device)

    def encode(self, sentences, return_tensors="pt"):
        if self.tokenizer:  # Assuming this means we're using Hugging Face BERT
            tokens = self.tokenizer(
                sentences, padding=True, truncation=True, return_tensors=return_tensors
            )
            tokens = {key: value.to(self.device) for key, value in tokens.items()}

            with torch.no_grad():
                outputs = self.encoder(**tokens)
            embeddings = outputs.last_hidden_state[
                :, 0, :
            ]  # Use the [CLS] token embeddings
            return embeddings

        else:  # Assuming this is for SentenceTransformer
            return self.encoder.encode(sentences, convert_to_tensor=True).to(
                self.device
            )


class ClassTransformer:
    def __init__(
        self,
        source_class: str | None = None,
        target_class: list[str] | None = None,
        model: Optional[Encoder] = None,
        device: str = "cpu",
    ) -> None:
        self._source_class = source_class
        self._target_class = target_class
        if target_class is None:
            print(
                f"get BONSAI activity classification as the default target clasification from {BONSAI_ACTIVITY_API}"
            )
            self._target_class = get_bonsai_activity_classification()

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

        encoded_classes = [
            self._model.encode(classification) for classification in self._target_class
        ]
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

        return self._target_class[idx_most_similar]
