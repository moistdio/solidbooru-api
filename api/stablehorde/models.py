from typing import Optional, Sequence

import msgspec


from typing import Sequence
import msgspec

class ModelGenerationInputStable(msgspec.Struct):
    sampler_name: str | None = None
    height: int | None = None
    width: int | None = None
    post_processing: Sequence[str] | None = None
    hires_fix: bool | None = None
    karras: bool | None = None
    cfg_scale: float | None = None
    denoising_strength: float | None = None
    facefixer_strength: float | None = None
    steps: int | None = None
    clip_skip: int | None = None
    seed: str | None = None
    control_type: str | None = None
    n: int | None = None
    hires_fix_denoising_strength: float | None = None
    seed_variation: int | None = None
    tiling: bool | None = None
    image_is_control: bool | None = None
    return_control_map: bool | None = None
    loras: Sequence[str] | None = None
    tis: Sequence[str] | None = None
    special: str | None = None
    extra_texts: Sequence[str] | None = None
    workflow: str | None = None
    transparent: bool | None = None

    def to_dict(self):
        return {f: getattr(self, f) for f in self.__struct_fields__ if getattr(self, f) is not None}
    
class ModelGenerationInputImageStable(msgspec.Struct):
    sampler_name: str | None = None
    height: int | None = None
    width: int | None = None
    post_processing: Sequence[str] | None = None
    hires_fix: Optional[bool] = None
    karras: Optional[bool] = None
    cfg_scale: float | None = None
    denoising_strength: Optional[float] = None
    facefixer_strength: Optional[float] = None
    steps: int | None = None
    clip_skip: int | None = None
    seed: Optional[str] = ""
    control_type: Optional[str] = None
    n: int | None = None

    def to_dict(self):
        return {f: getattr(self, f) for f in self.__struct_fields__}


class GenerationInput(msgspec.Struct):
    prompt: str
    params: ModelGenerationInputStable | None = None
    nsfw: bool | None = None
    trusted_workers: bool | None = None
    censor_nsfw: bool | None = None
    workers: Sequence[str] | None = None
    models: Sequence[str] | None = None
    source_image: str | None = None
    source_processing: str | None = None
    source_mask: str | None = None
    workers: str | None = None
    r2: bool | None = None

    def to_dict(self):
        return {
            f: getattr(
                self, f
                ) for f in self.__struct_fields__ if getattr(
                self, f
                ) is not None
            }


class RequestAsync(msgspec.Struct):
    id: Optional[str] = None
    message: Optional[str] = None
    kudos: Optional[float] = 0
    warnings: Optional[list[dict]] = None

    def to_dict(self):
        return {f: getattr(self, f) for f in self.__struct_fields__}


class RequestStatusCheck(msgspec.Struct):
    finished: int
    processing: int
    restarted: int
    waiting: int
    done: bool
    faulted: bool
    wait_time: int
    queue_position: int
    kudos: float
    is_possible: bool

    def to_dict(self):
        return {f: getattr(self, f) for f in self.__struct_fields__}


class GenerationStable(msgspec.Struct):
    worker_id: str
    worker_name: str
    model: str
    img: str
    seed: str

    def to_dict(self):
        return {f: getattr(self, f) for f in self.__struct_fields__}


class RequestStatusStable(msgspec.Struct):
    finished: int
    processing: int
    restarted: int
    waiting: int
    done: bool
    faulted: bool
    wait_time: int
    queue_position: int
    kudos: float
    is_possible: bool
    generations: list[GenerationStable]

    def to_dict(self):
        return {f: getattr(self, f) for f in self.__struct_fields__}

class ModelPayloadLorasStable(msgspec.Struct):
    name: str
    model: float = 1
    clip: float = 1
    inject_trigger: Optional[str] = None
    is_version: bool = False

    def to_dict(self):
        return {f: getattr(self, f) for f in self.__struct_fields__ if getattr(self, f) is not None}