from __future__ import annotations

import abc
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Type,
    Union,
)

import numpy as np
import torch


if TYPE_CHECKING:
    import streaming
    from transformers import PreTrainedTokenizer, PreTrainedTokenizerFast

    Tokenizer = Union[PreTrainedTokenizer, PreTrainedTokenizerFast]


Sample = Dict[str, Any]
StateDict = Dict[str, Any]
TokenArray = Union[List[int], np.ndarray, torch.Tensor]
FilterMapFn = Callable[[Sample], Optional[Sample]]
MapFn = Callable[[Sample], Sample]
FilterFn = Callable[[Sample], bool]
CollateFn = Callable[[List[Sample]], Sample]
ParallelExecutorType = Literal["process", "thread"]
FileFormat = Literal["auto", "jsonl", "cbor"]


class CheckpointableIterator(abc.ABC):
    def __iter__(self) -> CheckpointableIterator:
        return self

    @abc.abstractmethod
    def __next__(self) -> Sample:
        raise NotImplementedError()

    @abc.abstractmethod
    def state_dict(self) -> StateDict:
        raise NotImplementedError

    @abc.abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    def __enter__(self) -> CheckpointableIterator:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()


class CheckpointableDataset(torch.utils.data.IterableDataset, abc.ABC):
    def __iter__(self) -> CheckpointableIterator:
        return self.iter(state_dict=None)

    @abc.abstractmethod
    def iter(self, state_dict: Optional[StateDict] = None) -> CheckpointableIterator:
        raise NotImplementedError()

    @staticmethod
    def from_sequence(
        sequence: Sequence[Sample],
        repeat: bool = False,
        shuffle: bool = False,
        shuffle_seed: int = 42,
    ) -> CheckpointableDataset:
        from .sources import SequenceDataset

        return SequenceDataset(
            sequence=sequence, repeat=repeat, shuffle=shuffle, shuffle_seed=shuffle_seed
        )

    @staticmethod
    def from_iterable(
        iterable: Iterable[Sample],
        repeat: bool = False,
    ) -> CheckpointableDataset:
        """
        Create a CheckpointableDataset from an iterable.

        This static method creates a new CheckpointableDataset instance from an iterable.
        Each item in the iterable should be a `Sample` instance.

        The iterable should be a 're-iterable' and 'deterministic', i.e., it should return a new
        iterator each time `iter` is invoked and generate the same sequence of samples every time.
        This allows the successful resumption.
        """

        from .sources import IterableDataset

        return IterableDataset(iterable, repeat=repeat)

    @staticmethod
    def from_mosaicml(
        mosaicml_dataset: streaming.StreamingDataset,
        repeat: bool = False,
    ) -> CheckpointableDataset:
        from .sources import MosaicmlDataset

        return MosaicmlDataset(mosaicml_dataset, repeat=repeat)

    @staticmethod
    def from_files(
        urls: Union[str, Sequence[str]],
        repeat: bool = False,
        shuffle_shards: bool = False,
        format: FileFormat = "auto",
        n_active_shards: int = 10,
        n_standby_shards: int = 2,
        timeout: float = 60.0,
        n_prefetch_samples: int = 10,
        seed: int = 42,
    ) -> CheckpointableDataset:
        from .sources import FilesDataset

        return FilesDataset(
            urls=urls,
            repeat=repeat,
            shuffle_shards=shuffle_shards,
            format=format,
            n_active_shards=n_active_shards,
            n_standby_shards=n_standby_shards,
            timeout=timeout,
            n_prefetch_samples=n_prefetch_samples,
            seed=seed,
        )

    def filter_map(self, fn: FilterMapFn) -> CheckpointableDataset:
        from .transforms import FilterMapDataset

        return FilterMapDataset(self, fn)

    def map(self, fn: Callable[[Sample], Sample]) -> CheckpointableDataset:
        from .transforms import FilterMapDataset

        return FilterMapDataset(self, fn)

    def filter(self, fn: Callable[[Sample], bool]) -> CheckpointableDataset:
        from .transforms import FilterMapDataset

        def _fn(sample: Sample) -> Optional[Sample]:
            return sample if fn(sample) else None

        return FilterMapDataset(self, _fn)

    def parallel_filter_map(
        self,
        fn: FilterMapFn,
        max_workers: Optional[int] = None,
        prefetch_factor: int = 10,
        ordered: bool = True,
        executor_type: ParallelExecutorType = "process",
    ) -> CheckpointableDataset:
        from .transforms import ParallelFilterMapDataset

        return ParallelFilterMapDataset(
            self,
            fn,
            max_workers=max_workers,
            prefetch_factor=prefetch_factor,
            ordered=ordered,
            executor_type=executor_type,
        )

    def parallel_map(
        self,
        fn: Callable[[Sample], Sample],
        max_workers: Optional[int] = None,
        prefetch_factor: int = 10,
        ordered: bool = True,
        executor_type: ParallelExecutorType = "process",
    ) -> CheckpointableDataset:
        from .transforms.basic.filter_map import adapt_map_fn

        return self.parallel_filter_map(
            adapt_map_fn(fn),
            max_workers=max_workers,
            prefetch_factor=prefetch_factor,
            ordered=ordered,
            executor_type=executor_type,
        )

    def parallel_filter(
        self,
        fn: FilterFn,
        max_workers: Optional[int] = None,
        prefetch_factor: int = 10,
        ordered: bool = True,
        executor_type: ParallelExecutorType = "process",
    ) -> CheckpointableDataset:
        from .transforms.basic.filter_map import adapt_filter_fn

        return self.parallel_filter_map(
            adapt_filter_fn(fn),
            max_workers=max_workers,
            prefetch_factor=prefetch_factor,
            ordered=ordered,
            executor_type=executor_type,
        )

    def enumerate(self, count_column: str = "step") -> CheckpointableDataset:
        from .transforms import CountDataset

        return CountDataset(self, count_column=count_column)

    def take(
        self,
        max_count: int,
    ) -> CheckpointableDataset:
        from .transforms import CountDataset

        return CountDataset(self, max_count=max_count)

    def shuffle(
        self,
        buffer_size: int,
        seed: int = 42,
    ) -> CheckpointableDataset:
        from .transforms import ShuffleDataset

        return ShuffleDataset(self, buffer_size=buffer_size, seed=seed)

    def batch(
        self,
        batch_size: int,
        collate_fn: CollateFn = torch.utils.data.default_collate,
        drop_last: bool = False,
    ) -> CheckpointableDataset:
        from .transforms import BatchDataset

        return BatchDataset(
            self, batch_size=batch_size, collate_fn=collate_fn, drop_last=drop_last
        )

    def stride(
        self,
        interval: int,
        offset: int,
    ) -> CheckpointableDataset:
        from .transforms import StrideDataset

        return StrideDataset(self, interval=interval, offset=offset)

    def tokenize(
        self,
        tokenizer: Tokenizer,
        tokenizer_kwargs: Optional[Dict[str, Any]] = None,
        target_column: str = "text",
        parallel: bool = True,
        max_workers: Optional[int] = 1,
        prefetch_factor: int = 10,
        ordered: bool = True,
        executor_type: ParallelExecutorType = "thread",
    ) -> CheckpointableDataset:
        from .transforms import tokenize

        return tokenize(
            source=self,
            tokenizer=tokenizer,
            tokenizer_kwargs=tokenizer_kwargs,
            target_column=target_column,
            parallel=parallel,
            max_workers=max_workers,
            prefetch_factor=prefetch_factor,
            ordered=ordered,
            executor_type=executor_type,
        )

    def add_bos_eos(
        self,
        bos_token_id: Optional[int],
        eos_token_id: Optional[int],
        target_column: str = "input_ids",
    ) -> CheckpointableDataset:
        from .transforms import add_bos_eos

        return add_bos_eos(
            self, bos_token_id=bos_token_id, eos_token_id=eos_token_id, target_column=target_column
        )

    def ensure_bos_eos(
        self, tokenizer: Tokenizer, target_column: str = "input_ids"
    ) -> CheckpointableDataset:
        from .transforms import ensure_bos_eos

        return ensure_bos_eos(self, tokenizer=tokenizer, target_column=target_column)

    def pad(
        self,
        pad_values: Mapping[str, int],
        chunk_length: int,
    ) -> CheckpointableDataset:
        from .transforms import pad

        return pad(self, pad_values=pad_values, chunk_length=chunk_length)

    def chunk(
        self,
        chunk_length: int,
        target_columns: Sequence[str] = ("input_ids",),
        drop_remainder: bool = True,
    ) -> CheckpointableDataset:
        from .transforms import ChunkDataset

        return ChunkDataset(
            self,
            chunk_length=chunk_length,
            target_columns=target_columns,
            drop_remainder=drop_remainder,
        )

    def concat_chunk(
        self,
        chunk_length: int,
        target_columns: Sequence[str] = ("input_ids",),
    ) -> CheckpointableDataset:
        from .transforms import ConcatChunkDataset

        return ConcatChunkDataset(
            self,
            chunk_length=chunk_length,
            target_columns=target_columns,
        )

    def pack_chunk(
        self,
        chunk_length: int,
        target_columns: Sequence[str],
        discard_long_samples: bool = False,
    ) -> CheckpointableDataset:
        from .transforms import PackChunkDataset

        return PackChunkDataset(
            self,
            chunk_length=chunk_length,
            target_columns=target_columns,
            discard_long_samples=discard_long_samples,
        )

    def cache(
        self,
    ) -> CheckpointableDataset:
        from .caching import CacheDataset

        return CacheDataset(self)

    # `__add__` is implemented in PyTorch's `IterableDataset`,
    # so we need to override it here for prevent unexpected behavior
    def __add__(self, other: CheckpointableDataset) -> CheckpointableDataset:  # type: ignore
        from .combinations import concat_datasets

        return concat_datasets([self, other])
