"""Module for various processes that are used in the controllers."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from tqdm import tqdm

if TYPE_CHECKING:
    from typing_extensions import Unpack

    from .models import ConversationSet
    from .utils import GraphKwargs, WordCloudKwargs


def generate_week_barplots(
    conv_set: ConversationSet,
    dir_path: Path | str,
    *,
    progress_bar: bool = False,
    **kwargs: Unpack[GraphKwargs],
) -> None:
    """Create the weekwise graphs and save them to the folder."""
    dir_path = Path(dir_path)

    months_group = conv_set.group_by_month()
    years_group = conv_set.group_by_year()

    for month in tqdm(
        months_group.keys(),
        "Creating monthly weekwise graphs 📈 ",
        disable=not progress_bar,
    ):
        title = month.strftime("%B '%y")
        months_group[month].week_barplot(title, **kwargs).savefig(  # pyright: ignore [reportUnknownMemberType]
            dir_path / f"{month.strftime('%Y %B')}.png",
        )

    for year in tqdm(
        years_group.keys(),
        "Creating yearly weekwise graphs 📈 ",
        disable=not progress_bar,
    ):
        title = year.strftime("%Y")
        years_group[year].week_barplot(title, **kwargs).savefig(  # pyright: ignore [reportUnknownMemberType]
            dir_path / f"{year.strftime('%Y')}.png",
        )


def generate_wordclouds(
    conv_set: ConversationSet,
    dir_path: Path | str,
    *,
    progress_bar: bool = False,
    **kwargs: Unpack[WordCloudKwargs],
) -> None:
    """Create the wordclouds and save them to the folder."""
    dir_path = Path(dir_path)

    weeks_group = conv_set.group_by_week()
    months_group = conv_set.group_by_month()
    years_group = conv_set.group_by_year()

    for week in tqdm(
        weeks_group.keys(),
        "Creating weekly wordclouds 🔡☁️ ",
        disable=not progress_bar,
    ):
        weeks_group[week].wordcloud(**kwargs).save(
            dir_path / f"{week.strftime('%Y week %W')}.png",
            optimize=True,
        )

    for month in tqdm(
        months_group.keys(),
        "Creating monthly wordclouds 🔡☁️ ",
        disable=not progress_bar,
    ):
        months_group[month].wordcloud(**kwargs).save(
            dir_path / f"{month.strftime('%Y %B')}.png",
            optimize=True,
        )

    for year in tqdm(
        years_group.keys(),
        "Creating yearly wordclouds 🔡☁️ ",
        disable=not progress_bar,
    ):
        years_group[year].wordcloud(**kwargs).save(
            dir_path / f"{year.strftime('%Y')}.png",
            optimize=True,
        )
