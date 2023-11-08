# source.py

import os
import multiprocessing
from typing import Iterable
from pathlib import Path
from functools import partial

import numpy as np
from PIL import Image

from pyvideo import Video

from ascii_art.image import (
    image_to_ascii_art_html, html_to_image, pillow_to_numpy,
    load_image, load_html, save_html, save_image
)

__all__ = [
    "video_to_ascii_art_htmls",
    "video_ascii_art",
    "htmls_to_video",
    "htmls_to_images",
    "save_htmls",
    "save_images",
    "load_images",
    "load_htmls"
]

FPS = 60

def save_htmls(htmls: Iterable[str], path: str | Path) -> list[str]:
    """
    Saves the HTML data to the saving path.

    :param htmls: The HTML strings.
    :param path: The saving path.

    :return: The file paths.
    """

    location = os.path.split(path)[0]

    if location:
        os.makedirs(location, exist_ok=True)
    # end if

    pool = multiprocessing.Pool()

    paths = [str(Path(path) / Path(f"{i}.html")) for i in range(len(list(htmls)))]

    pool.map(save_html, [(html, file) for html, file in zip(htmls, paths)])

    return paths
# end save_html

def load_htmls(path: str | Path) -> list[str]:
    """
    Loads the HTML data from the path.

    :param path: The saving path.

    :return: The HTML string.
    """

    pool = multiprocessing.Pool()

    return pool.map(
        load_html,
        [path for path in os.listdir(path) if path.endswith(".html")]
    )
# end load_html

def save_images(
        images: Iterable[Image.Image | np.ndarray],
        path: str | Path,
        extension: str = "png"
) -> list[str]:
    """
    Saves the source data to the saving path.

    :param images: The source objects.
    :param path: The saving path.
    :param extension: The type of file extension.

    :return: The file paths.
    """

    location = os.path.split(path)[0]

    if location:
        os.makedirs(location, exist_ok=True)
    # end if

    pool = multiprocessing.Pool()

    paths = [str(Path(path) / Path(f"{i}.{extension}")) for i in range(len(list(images)))]

    pool.map(save_image, [(html, file) for html, file in zip(images, paths)])

    return paths
# end save_image

def load_images(
        path: str | Path, extensions: Iterable[str] = None
) -> list[Image.Image | np.ndarray]:
    """
    Loads the source data from the path.

    :param path: The saving path.
    :param extensions: The file extensions to load.

    :return: The source object.
    """

    pool = multiprocessing.Pool()

    return pool.map(
        load_image,
        [
            path for path in os.listdir(path)
            if (
                (extensions is None) or
                any(extension == path[-len(extension):] for extension in extensions)
            )
        ]
    )
# end load_image

def video_to_ascii_art_htmls(
        video: Video, lines: int = None, color: bool = None
) -> list[str]:
    """
    Generates an HTML string of ASCII art from a source pillow source object.

    :param video: The source object or file path.
    :param lines: The amount of lines in the html string.
    :param color: The value to color the html.

    :return: The HTML string.
    """

    pool = multiprocessing.Pool()

    return pool.map(
        partial(image_to_ascii_art_html, lines=lines, color=color),
        video.frames
    )
# end video_to_ascii_art_htmls

def htmls_to_images(
        htmls: Iterable[str],
        size: tuple[int, int] = None,
        quality: int = None,
        brightness_factor: float = None,
        color_factor: float = None
) -> list[Image.Image]:
    """
    Generates an image from the html.

    :param htmls: The HTML string.
    :param size: The size to crop the source to.
    :param quality: The quality of the source.
    :param brightness_factor: The brightness factor to scale the source.
    :param color_factor: The color factor to scale the source.

    :return: The generated source object.
    """

    pool = multiprocessing.Pool()

    return pool.map(
        partial(
            html_to_image,
            size=size, quality=quality,
            brightness_factor=brightness_factor,
            color_factor=color_factor
        ),
        list(htmls)
    )
# end htmls_to_images

def htmls_to_video(
        htmls: Iterable[str],
        fps: float,
        size: tuple[int, int] = None,
        quality: int = None,
        brightness_factor: float = None,
        color_factor: float = None,
        video: Video = None
) -> Video:
    """
    Generates a video from the html.

    :param htmls: The HTML string.
    :param fps: The fps for the source.
    :param size: The size to crop the source to.
    :param quality: The quality of the source.
    :param brightness_factor: The brightness factor to scale the source.
    :param color_factor: The color factor to scale the source.
    :param video: The video to add the frames into

    :return: The generated source object.
    """

    if fps is None:
        fps = FPS
    # end if

    frames = htmls_to_images(
        htmls=htmls,
        size=size, quality=quality,
        brightness_factor=brightness_factor,
        color_factor=color_factor
    )

    video = video or Video(fps=fps)

    if frames:
        video.frames = [pillow_to_numpy(frame) for frame in frames]
        video.width = frames[0].width,
        video.height = frames[0].height
    # end if

    return video
# end htmls_to_video

def video_ascii_art(
        source: str | Path | Video = None,
        htmls: str | Path | Iterable[str] = None,
        lines: int = None,
        color: bool = None,
        quality: int = None,
        fps: float = None,
        brightness_factor: float = None,
        color_factor: float = None,
        html_destination: str | Path = None,
        destination: str | Path = None
) -> None:
    """
    Generate an ASCII ark source from a source video or HTML file.

    :param source: The source video object or file path.
    :param htmls: The html file path or data.
    :param lines: The amount of lines in the html string.
    :param color: The value to color the html.
    :param fps: The fps for the video.
    :param quality: The quality of the source.
    :param brightness_factor: The brightness factor to scale the source.
    :param color_factor: The color factor to scale the source.
    :param html_destination: The path to save the html data in.
    :param destination: The path to save the generated video data in.
    """

    if (source, htmls) == (None, None):
        raise ValueError("At least one of html or source must be defined.")
    # end if

    if htmls is None:
        if isinstance(source, (str, Path)):
            if Path(str(source)).is_file():
                source = Video.load(source)

                if fps is None:
                    fps = source.fps
                # end if

            else:
                if fps is None:
                    fps = FPS
                # end if

                images = load_images(source)

                source = Video(
                    frames=[pillow_to_numpy(image) for image in images],
                    fps=fps
                )
            # end if
        # end if

        htmls = video_to_ascii_art_htmls(
            video=source, lines=lines, color=color
        )
    # end if

    if fps is None:
        fps = FPS
    # end if

    if isinstance(htmls, Path) or (isinstance(htmls, (str, Path)) and Path(htmls).exists()):
        htmls = load_htmls(htmls)
    # end if

    art_video = htmls_to_video(
        htmls=htmls,
        quality=quality,
        brightness_factor=brightness_factor,
        color_factor=color_factor,
        size=(source.width, source.height),
        fps=fps,
        video=source.copy()
    )

    if html_destination is not None:
        save_htmls(htmls=htmls, path=html_destination)
    # end if

    if destination is not None:
        art_video.save(destination)
    # end if
# end ascii_art