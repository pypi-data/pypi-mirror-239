import dataclasses
from typing import Callable, Optional, Tuple
import PIL.Image
import torch
import irisml.core


class Task(irisml.core.TaskBase):
    """Creates a transform function for VQA task.

    The input to the transform function is ((question, image), targets), where question is a string,
    image is a PIL image, and targets is a string.

    If tokenizer is provided, the output of the transform function is ((question, image_tensor), targets),
    where question is a tuple of tensors, image_tensor is a tensor, and targets is a tuple of tensors.

    If tokenizer is not provided, the output of the transform function is ((question, image_tensor), targets),
    where question is a tuple of tensors or a string, image_tensor is a tensor, and targets is a string.
    """
    VERSION = '1.1.0'

    @dataclasses.dataclass
    class Inputs:
        image_transform: Callable[[PIL.Image.Image], torch.Tensor]
        text_transform: Optional[Callable[[str], str]] = None
        target_text_transform: Optional[Callable[[str], str]] = None
        tokenizer: Optional[Callable[[str], Tuple[torch.Tensor, torch.Tensor]]] = None  # The output is (input_ids, attention_mask)

    @dataclasses.dataclass
    class Config:
        skip_target_tokenization: bool = False

    @dataclasses.dataclass
    class Outputs:
        transform: Callable[[Tuple[str, PIL.Image.Image], str], Tuple[Tuple[str, torch.Tensor], str]]
        collate_function: Callable  # [(((input_ids, attention_mask), image_tensor), (input_ids, attention_mask))] => (((input_ids, attention_mask), image_tensor), (input_ids, attention_mask))

    def execute(self, inputs):
        transform = VqaImageTransform(inputs.image_transform, inputs.text_transform, inputs.target_text_transform, inputs.tokenizer, self.config.skip_target_tokenization)
        return self.Outputs(transform=transform, collate_function=_collate_function)

    def dry_run(self, inputs):
        return self.execute(inputs)


def _collate_function(batch):
    questions = [b[0][0] for b in batch]
    images = [b[0][1] for b in batch]
    targets = [b[1] for b in batch]

    questions = (torch.stack([q[0] for q in questions], 0), torch.stack([q[1] for q in questions], 0))
    images = torch.stack(images, 0)
    if not isinstance(targets[0], str):
        targets = (torch.stack([t[0] for t in targets], 0), torch.stack([t[1] for t in targets], 0))

    return (questions, images), targets


class VqaImageTransform:
    def __init__(self, image_transform, text_transform, target_text_transform, tokenizer, skip_target_tokenization):
        self._image_transform = image_transform
        self._text_transform = text_transform
        self._target_text_transform = target_text_transform
        self._tokenizer = tokenizer
        self._skip_target_tokenization = skip_target_tokenization

    def __call__(self, inputs, targets):
        question, image = inputs
        assert isinstance(question, str)
        assert isinstance(image, PIL.Image.Image)
        assert isinstance(targets, str)

        image_tensor = self._image_transform(image)

        if self._text_transform:
            question = self._text_transform(question)

        if self._target_text_transform:
            targets = self._target_text_transform(targets)

        if self._tokenizer:
            question = self._tokenizer(question)
            if not self._skip_target_tokenization:
                targets = self._tokenizer(targets)

        return (question, image_tensor), targets
