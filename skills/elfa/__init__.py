"""Elfa skills."""

from typing import NotRequired, TypedDict

from abstracts.skill import SkillStoreABC
from skills.base import SkillConfig, SkillState
from skills.elfa.base import ElfaBaseTool
from skills.elfa.mention import ElfaGetMentions, ElfaGetTopMentions, ElfaSearchMentions
from skills.elfa.stats import ElfaGetSmartStats
from skills.elfa.tokens import ElfaGetTrendingTokens

# Cache skills at the system level, because they are stateless
_cache: dict[str, ElfaBaseTool] = {}


class SkillStates(TypedDict):
    get_mentions: SkillState
    get_top_mentions: SkillState
    search_mentions: SkillState
    get_trending_tokens: SkillState
    get_smart_stats: SkillState


class Config(SkillConfig):
    """Configuration for Elfa skills."""

    states: SkillStates
    api_key: NotRequired[str]


async def get_skills(
    config: "Config",
    is_private: bool,
    store: SkillStoreABC,
    **_,
) -> list[ElfaBaseTool]:
    """Get all Elfa skills.

    Args:
        config: The configuration for Elfa skills.
        is_private: Whether to include private skills.
        store: The skill store for persisting data.

    Returns:
        A list of Elfa skills.
    """
    available_skills = []

    # Include skills based on their state
    for skill_name, state in config["states"].items():
        if state == "disabled":
            continue
        elif state == "public" or (state == "private" and is_private):
            available_skills.append(skill_name)

    # Get each skill using the cached getter
    return [get_elfa_skill(name, store) for name in available_skills]


def get_elfa_skill(
    name: str,
    store: SkillStoreABC,
) -> ElfaBaseTool:
    """Get an Elfa skill by name.

    Args:
        name: The name of the skill to get
        api_key: The Elfa API key
        store: The skill store for persisting data

    Returns:
        The requested Elfa skill

    Raises:
        ValueError: If the requested skill name is unknown
    """

    if name == "get_mentions":
        if name not in _cache:
            _cache[name] = ElfaGetMentions(
                skill_store=store,
            )
        return _cache[name]

    elif name == "get_top_mentions":
        if name not in _cache:
            _cache[name] = ElfaGetTopMentions(
                skill_store=store,
            )
        return _cache[name]

    elif name == "search_mentions":
        if name not in _cache:
            _cache[name] = ElfaSearchMentions(
                skill_store=store,
            )
        return _cache[name]

    elif name == "get_trending_tokens":
        if name not in _cache:
            _cache[name] = ElfaGetTrendingTokens(
                skill_store=store,
            )
        return _cache[name]

    elif name == "get_smart_stats":
        if name not in _cache:
            _cache[name] = ElfaGetSmartStats(
                skill_store=store,
            )
        return _cache[name]

    else:
        raise ValueError(f"Unknown Elfa skill: {name}")
