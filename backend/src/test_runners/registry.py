"""
Test runner registry and auto-detection.
"""

import logging
from pathlib import Path
from typing import List, Optional, Type

from .base import TestRunner

# Import all runners
from .python import PytestRunner, UnittestRunner
from .javascript import JestRunner, VitestRunner, MochaRunner, NodeTestRunner
from .go import GoTestRunner
from .rust import CargoRunner
from .jvm import MavenRunner, GradleRunner, SbtRunner
from .ruby import RSpecRunner, MinitestRunner
from .c_cpp import CMakeRunner, MakeRunner, GoogleTestRunner
from .dotnet import DotNetRunner

logger = logging.getLogger(__name__)


# All available runners, in priority order within each language
ALL_RUNNERS: List[Type[TestRunner]] = [
    # Python (pytest preferred over unittest)
    PytestRunner,
    UnittestRunner,

    # JavaScript/TypeScript (order: vitest, jest, mocha, node:test)
    VitestRunner,
    JestRunner,
    MochaRunner,
    NodeTestRunner,

    # Go
    GoTestRunner,

    # Rust
    CargoRunner,

    # JVM (gradle preferred over maven)
    GradleRunner,
    MavenRunner,
    SbtRunner,

    # Ruby (rspec preferred over minitest)
    RSpecRunner,
    MinitestRunner,

    # C/C++ (cmake preferred)
    GoogleTestRunner,
    CMakeRunner,
    MakeRunner,

    # .NET
    DotNetRunner,
]


# Map language names to preferred runners
LANGUAGE_RUNNERS = {
    "Python": [PytestRunner, UnittestRunner],
    "JavaScript": [VitestRunner, JestRunner, MochaRunner, NodeTestRunner],
    "TypeScript": [VitestRunner, JestRunner, MochaRunner, NodeTestRunner],
    "Go": [GoTestRunner],
    "Rust": [CargoRunner],
    "Java": [GradleRunner, MavenRunner],
    "Scala": [SbtRunner, GradleRunner],
    "Kotlin": [GradleRunner, MavenRunner],
    "Ruby": [RSpecRunner, MinitestRunner],
    "C++": [GoogleTestRunner, CMakeRunner, MakeRunner],
    "C": [CMakeRunner, MakeRunner],
    "C#": [DotNetRunner],
}


def get_runner(repo_path: Path, language_hint: Optional[str] = None) -> Optional[TestRunner]:
    """
    Auto-detect and return the best test runner for a repository.

    Args:
        repo_path: Path to the repository
        language_hint: Optional language hint to narrow down runner selection

    Returns:
        TestRunner instance or None if no suitable runner found
    """
    repo_path = Path(repo_path)

    if not repo_path.exists():
        logger.error(f"Repository path does not exist: {repo_path}")
        return None

    # If we have a language hint, check those runners first
    candidates = []
    if language_hint and language_hint in LANGUAGE_RUNNERS:
        candidates = LANGUAGE_RUNNERS[language_hint]

    # Then check all runners
    candidates = candidates + [r for r in ALL_RUNNERS if r not in candidates]

    best_runner: Optional[TestRunner] = None
    best_score = 0

    for runner_class in candidates:
        try:
            runner = runner_class()
            score = runner.detect(repo_path)

            logger.debug(f"{runner.name}: score={score}")

            if score > best_score:
                best_score = score
                best_runner = runner
        except Exception as e:
            logger.debug(f"Error detecting {runner_class.name}: {e}")
            continue

    if best_runner and best_score >= 30:  # Minimum confidence threshold
        logger.info(f"Selected runner: {best_runner.name} (score: {best_score})")
        return best_runner

    logger.warning(f"No suitable test runner found for {repo_path}")
    return None


def get_all_detected_runners(repo_path: Path) -> List[tuple]:
    """
    Get all runners that can potentially handle this repo, with their scores.

    Returns:
        List of (runner, score) tuples, sorted by score descending
    """
    repo_path = Path(repo_path)
    results = []

    for runner_class in ALL_RUNNERS:
        try:
            runner = runner_class()
            score = runner.detect(repo_path)
            if score > 0:
                results.append((runner, score))
        except Exception:
            continue

    return sorted(results, key=lambda x: x[1], reverse=True)


def get_runner_by_name(name: str) -> Optional[TestRunner]:
    """
    Get a specific runner by name.

    Args:
        name: Runner name (e.g., "pytest", "jest", "cargo test")

    Returns:
        TestRunner instance or None
    """
    name_lower = name.lower()

    for runner_class in ALL_RUNNERS:
        runner = runner_class()
        if runner.name.lower() == name_lower:
            return runner

    return None


def list_available_runners() -> List[dict]:
    """
    List all available runners with their metadata.

    Returns:
        List of dicts with runner info
    """
    runners = []
    for runner_class in ALL_RUNNERS:
        runner = runner_class()
        runners.append({
            "name": runner.name,
            "language": runner.language,
            "class": runner_class.__name__,
        })
    return runners
