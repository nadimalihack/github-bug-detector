#!/usr/bin/env python3
"""

Analyzes repositories for SWE-Bench+ sample creation suitability by combining:
- Repository-level metrics (file structure, test coverage, CI/CD, etc.)
- PR-level analysis with detailed rejection tracking

Supports both GitHub and Bitbucket repositories.

Usage:
    # With GitHub token (for private repos or higher rate limits)
    python repo_evaluator.py owner/repo-name --token $GITHUB_TOKEN

    # With Bitbucket repository
    python repo_evaluator.py bitbucket:owner/repo-name --token $BITBUCKET_TOKEN --platform bitbucket

    # Auto-detect platform from URL
    python repo_evaluator.py https://bitbucket.org/owner/repo --token $BITBUCKET_TOKEN

Examples:
    python repo_evaluator.py microsoft/vscode --token $GITHUB_TOKEN
    python repo_evaluator.py bitbucket:owner/repo --token $BITBUCKET_TOKEN --platform bitbucket
"""

import os
import json
import sys
import re
import subprocess
import argparse
import logging
import tempfile
import shutil
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Callable, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

try:
    from .repo_evaluator_helpers import (
    load_language_config,
    get_language_config,
    is_english,
    is_test_file_path,
    is_asset_file_path,
    has_sufficient_code_changes,
    has_rust_embedded_tests,
    normalize_to_utc,
    HEADERS,
    has_valid_issue_word_count,
    count_words,
    MIN_ISSUE_WORDS,
    MAX_ISSUE_WORDS
)
except Exception:
    from repo_evaluator_helpers import (
    load_language_config,
    get_language_config,
    is_english,
    is_test_file_path,
    is_asset_file_path,
    has_sufficient_code_changes,
    has_rust_embedded_tests,
    normalize_to_utc,
    HEADERS,
    has_valid_issue_word_count,
    count_words,
    MIN_ISSUE_WORDS,
    MAX_ISSUE_WORDS
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Default configuration
MIN_PR_CODE_CHANGES = 1
MIN_TEST_FILES = 1
MAX_NON_TEST_FILES = 100
MAX_TEST_FILES = 15
MAX_CHANGED_FILES = 50

DATA_FILE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.csv', '.json', '.xml', '.yaml', '.yml', '.md', '.txt', '.pdf', '.zip', '.tar', '.gz'}


def _is_data_file(filepath: str) -> bool:
    return Path(filepath).suffix.lower() in DATA_FILE_EXTENSIONS

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY_BASE = 1  # Base delay in seconds for exponential backoff


# Retry helper function
def retry_api_call(func: Callable, max_retries: int = MAX_RETRIES, *args, **kwargs):
    """
    Retry an API call with exponential backoff and rate limit handling.

    Args:
        func: Function to retry
        max_retries: Maximum number of retry attempts
        *args, **kwargs: Arguments to pass to func

    Returns:
        Result of func(*args, **kwargs)

    Raises:
        Exception: If all retries fail
    """
    import requests

    last_exception = None
    for attempt in range(max_retries + 1):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code

            # Don't retry on 410 (Gone) errors - they indicate permanent resource removal
            if status_code == 410:
                logger.error(f"{e.response.text}\nHTTP 410 (Gone) error - resource no longer available. Not retrying.")
                raise

            # Handle rate limit errors (429 Too Many Requests or 403 Forbidden with rate limit)
            if status_code == 429 or (status_code == 403 and "rate limit" in str(e).lower()):
                wait_time = None

                # Try to get Retry-After header (seconds to wait)
                retry_after = e.response.headers.get('Retry-After')
                if retry_after:
                    try:
                        wait_time = int(retry_after)
                    except ValueError:
                        pass

                # Try to get X-RateLimit-Reset header (Unix timestamp)
                if wait_time is None:
                    rate_limit_reset = e.response.headers.get('X-RateLimit-Reset')
                    if rate_limit_reset:
                        try:
                            reset_timestamp = int(rate_limit_reset)
                            current_time = int(time.time())
                            wait_time = max(0, reset_timestamp - current_time)
                        except (ValueError, TypeError):
                            pass

                # If we couldn't determine wait time, use exponential backoff
                if wait_time is None:
                    wait_time = RETRY_DELAY_BASE * (2 ** attempt)
                    logger.warning(f"Rate limit exceeded. Using exponential backoff: {wait_time} seconds")
                else:
                    logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds until rate limit resets...")

                if attempt < max_retries:
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"Rate limit exceeded and max retries reached. Last error: {e}")
                    raise

            # Retry on 5xx server errors (transient server-side issues)
            if 500 <= status_code < 600:
                last_exception = e
                if attempt < max_retries:
                    delay = RETRY_DELAY_BASE * (2 ** attempt)
                    logger.warning(f"Server error {status_code} (attempt {attempt + 1}/{max_retries + 1}): {str(e)}")
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                    continue
                else:
                    logger.error(f"Server error {status_code} after {max_retries + 1} attempts. Last error: {e}")
                    raise

            # For other HTTP errors (4xx client errors), don't retry
            raise
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            last_exception = e
            if attempt < max_retries:
                delay = RETRY_DELAY_BASE * (2 ** attempt)
                error_msg = str(e)
                if "Failed to resolve" in error_msg or "nodename nor servname" in error_msg:
                    logger.warning(f"Network/DNS error (attempt {attempt + 1}/{max_retries + 1}): {error_msg}")
                else:
                    logger.warning(f"API request failed (attempt {attempt + 1}/{max_retries + 1}): {error_msg}")
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.error(f"All {max_retries + 1} attempts failed. Last error: {error_msg}")
                raise
        except Exception:
            # For other non-network errors, don't retry
            raise

    if last_exception:
        raise last_exception


# Data classes
@dataclass
class RepoMetrics:
    """Repository-level metrics."""
    repo_name: str
    total_files: int
    test_files: int
    test_file_ratio: float
    source_files: int
    total_loc: int
    source_loc: int
    test_loc: int
    languages: Dict[str, int]
    primary_language: str
    has_ci_cd: bool
    ci_files: List[str]
    test_frameworks: List[str]
    has_test_runner: bool
    total_commits: Optional[int]
    recent_commits_12mo: Optional[int]
    commits_referencing_issues: int
    test_coverage_percentage: Optional[float]
    swebench_readiness_score: float
    recommendation: str
    strengths: List[str]
    weaknesses: List[str]
    commit_spread_days: Optional[float] = None  # Days between first and latest commit
    median_commit_interval_hours: Optional[float] = None  # Median hours between commits (last 90 days)


@dataclass
class PRRejectionStats:
    """PR rejection statistics."""
    accepted_prs: List[dict]
    total_prs: int
    accepted: int
    rejected: int
    acceptance_rate: float
    rejection_breakdown: Dict[str, Dict[str, Any]]
    f2p_results: Optional[List[dict]] = None
    f2p_skipped_reason: Optional[str] = None


@dataclass
class AnalysisReport:
    """Complete analysis report."""
    repo_name: str
    repo_full_name: str
    repo_metrics: RepoMetrics
    pr_analysis: PRRejectionStats
    overall_score: float
    recommendation: str


# Platform Detection
def detect_platform(repo_string: str, explicit_platform: Optional[str] = "auto") -> str:
    """
    Detect platform (github or bitbucket) from repo string or explicit parameter.
    """
    if explicit_platform:
        explicit_platform = explicit_platform.lower()
        if explicit_platform in ['github', 'bitbucket']:
            return explicit_platform
        elif explicit_platform == 'auto':
            pass  # Continue with auto-detection
        else:
            raise ValueError(f"Invalid platform: {explicit_platform}. Must be 'github', 'bitbucket', or 'auto'")

    repo_string = repo_string.strip()

    # Check for explicit prefix
    if repo_string.startswith('bitbucket:'):
        return 'bitbucket'
    if repo_string.startswith('github:'):
        return 'github'

    # Check for URL patterns
    if 'bitbucket' in repo_string.lower():
        return 'bitbucket'
    if 'github.com' in repo_string.lower():
        return 'github'

    # Default to GitHub
    return 'github'


# Platform Abstraction Layer
from abc import ABC, abstractmethod


def _is_bot_username(username: str) -> bool:
    """
    Check if a username belongs to a bot.

    Args:
        username: The username to check

    Returns:
        True if the username appears to be a bot, False otherwise
    """
    if not username:
        return False

    username_lower = username.lower()

    # Check for common bot patterns
    # GitHub bots often end with [bot]
    if username.endswith('[bot]'):
        return True

    # Check for common bot names
    common_bots = [
        'dependabot', 'renovate', 'codecov', 'greenkeeper', 'snyk-bot',
        'pyup-bot', 'whitesource', 'mergify', 'stale', 'github-actions',
        'allcontributors', 'imgbot', 'k8s-ci-robot', 'k8s-bot', 'k8s-mergebot'
    ]

    if username_lower in common_bots:
        return True

    return False


class PlatformClient(ABC):
    """Abstract base class for platform-specific API clients."""

    def __init__(self, owner: str, repo_name: str, token: Optional[str] = None):
        self.owner = owner
        self.repo_name = repo_name
        self.repo_full_name = f"{owner}/{repo_name}"
        self.token = token

    @abstractmethod
    def fetch_prs(self, cursor: Optional[str] = None, page_size: int = 50, start_date: Optional[datetime] = None) -> dict:
        """Fetch pull requests. Returns dict with 'data', 'pageInfo', etc."""
        pass

    @abstractmethod
    def fetch_issue(self, issue_number: int) -> Optional[dict]:
        """Fetch issue details by number."""
        pass

    @abstractmethod
    def get_repo_url(self, include_token: bool = False) -> str:
        """Get repository clone URL."""
        pass

    @abstractmethod
    def extract_issue_number_from_text(self, text: str) -> List[int]:
        """Extract issue numbers from text (PR body, commit message, etc.)."""
        pass

    @abstractmethod
    def fetch_repo_languages(self) -> Optional[Dict[str, int]]:
        """Fetch repository languages with byte counts. Returns dict mapping language names to byte counts."""
        pass


# GitHub Client Implementation
class GitHubClient(PlatformClient):
    """GitHub API client implementation."""

    def __init__(self, owner: str, repo_name: str, token: Optional[str] = None):
        super().__init__(owner, repo_name, token)
        self.base_url = "https://api.github.com"
        self.headers = HEADERS.copy()
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def fetch_prs(self, cursor: Optional[str] = None, page_size: int = 50, start_date: Optional[datetime] = None) -> dict:
        """Fetch PRs using GraphQL API."""

        query = """
            query($owner: String!, $name: String!, $cursor: String, $page_size: Int!) {
            repository(owner: $owner, name: $name) {
              primaryLanguage { name }
              owner { login }
              name
              pullRequests(
                first: $page_size,
                after: $cursor,
                states: MERGED,
                orderBy: {field: CREATED_AT, direction: DESC}
              ) {
                pageInfo {
                  endCursor
                  hasNextPage
                }
                nodes {
                  number
                  title
                  body
                  baseRefOid
                  headRefOid
                  baseRefName
                  headRefName
                  mergedAt
                  createdAt
                  url
                  author {
                    login
                    __typename
                  }
                  files(first: 100) {
                    nodes {
                      path
                      changeType
                      additions
                      deletions
                    }
                  }
                  closingIssuesReferences(first: 10) {
                    nodes {
                      url
                      number
                      title
                      body
                      state
                      __typename
                    }
                  }
                }
              }
            }
          }
        """
        query_string = f"repo:{self.owner}/{self.repo_name} is:pr is:merged"
        if start_date:
            query_string += f" merged:>={start_date}"

        variables = {
            "owner": self.owner,
            "name": self.repo_name,
            "queryString": query_string,
            "cursor": cursor,
            "page_size": page_size
        }

        def _make_request():
            import requests
            response = requests.post(
                f"{self.base_url}/graphql",
                json={"query": query, "variables": variables},
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()

        return retry_api_call(_make_request)

    def fetch_issue(self, issue_number: int) -> Optional[dict]:
        """Fetch issue details by number."""
        import requests
        try:
            def _make_request():
                response = requests.get(
                    f"{self.base_url}/repos/{self.repo_full_name}/issues/{issue_number}",
                    headers=self.headers,
                    timeout=30
                )
                response.raise_for_status()
                return response.json()

            issue_details = retry_api_call(_make_request)

            # Exclude PRs
            if "pull_request" in issue_details:
                return None

            return {
                "number": issue_details.get("number"),
                "title": issue_details.get("title", ""),
                "body": issue_details.get("body", ""),
                "state": issue_details.get("state", "").upper(),
                "__typename": "Issue"
            }
        except Exception:
            return None

    def get_repo_url(self, include_token: bool = False) -> str:
        """Get repository clone URL."""
        if include_token and self.token:
            return f"https://{self.token}@github.com/{self.repo_full_name}.git"
        return f"https://github.com/{self.repo_full_name}.git"

    def extract_issue_number_from_text(self, text: str) -> List[int]:
        """Extract issue numbers from text."""
        if not text:
            return []
        issue_numbers = []
        # GitHub format: #123 or https://github.com/owner/repo/issues/123
        matches = re.findall(r'#(\d+)', text)
        issue_numbers.extend([int(m) for m in matches])
        url_matches = re.findall(r'https://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+/issues/(\d+)', text)
        issue_numbers.extend([int(m) for m in url_matches])
        return list(set(issue_numbers))

    def fetch_repo_languages(self) -> Optional[Dict[str, int]]:
        """Fetch repository languages with byte counts from GitHub API."""
        import requests
        try:
            url = f"{self.base_url}/repos/{self.repo_full_name}/languages"

            def _make_request():
                response = requests.get(url, headers=self.headers, timeout=30)
                response.raise_for_status()
                return response

            response = retry_api_call(_make_request)
            languages = response.json()
            return languages if languages else None
        except Exception as e:
            logger.debug(f"Failed to fetch repository languages from GitHub API: {e}")
            return None


# Bitbucket Client Implementation
class BitbucketClient(PlatformClient):
    """Bitbucket API client implementation."""

    def __init__(self, owner: str, repo_name: str, token: Optional[str] = None):
        super().__init__(owner, repo_name, token)
        self.base_url = "https://api.bitbucket.org/2.0"
        self.headers = {"Accept": "application/json"}
        if self.token:
            # Bitbucket uses Basic Auth with username:token or just token
            import base64
            base64.b64encode(f"{self.token}:{self.token}".encode()).decode()
            self.headers["Authorization"] = f"Bearer {self.token}"

    def fetch_prs(self, cursor: Optional[str] = None, page_size: int = 50, start_date: Optional[datetime] = None) -> dict:
        """Fetch PRs using REST API."""
        import requests

        # If cursor is a full URL (for pagination), use it directly
        if cursor and cursor.startswith("http"):
            request_url = cursor
            params = None
        else:
            request_url = f"{self.base_url}/repositories/{self.owner}/{self.repo_name}/pullrequests"
            params = {
                "state": "MERGED",
                "pagelen": page_size,
                "sort": "-created_on"
            }
            if cursor:
                params["page"] = cursor

            if start_date:
                params["q"] = f"created_on>={start_date.isoformat()}"

        def _make_request():
            response = requests.get(request_url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()

        data = retry_api_call(_make_request)

        # Transform Bitbucket format to GitHub-like format
        pr_nodes = []
        for pr in data.get("values", []):
            # Get PR files
            files_url = pr.get("links", {}).get("diffstat", {}).get("href", "")
            files = []
            if files_url:
                try:
                    def _get_files():
                        files_response = requests.get(files_url, headers=self.headers, timeout=30)
                        files_response.raise_for_status()
                        return files_response.json()

                    files_data = retry_api_call(_get_files)
                    for file_info in files_data.get("values", []):
                        files.append({
                            "path": file_info.get("new", {}).get("path", file_info.get("old", {}).get("path", "")),
                            "changeType": "ADDED" if file_info.get("status") == "added" else
                                        "DELETED" if file_info.get("status") == "deleted" else "MODIFIED",
                            "additions": file_info.get("lines_added", 0),
                            "deletions": file_info.get("lines_removed", 0)
                        })
                except Exception:
                    pass

            # Get linked issues from PR description
            linked_issues = []
            pr_description = pr.get("description", "") or ""
            issue_numbers = self.extract_issue_number_from_text(pr_description)
            for issue_num in issue_numbers:
                issue_data = self.fetch_issue(issue_num)
                if issue_data:
                    linked_issues.append(issue_data)

            # Get author information
            author_info = pr.get("author", {}) or {}
            author_login = author_info.get("display_name") or author_info.get("username") or ""

            pr_node = {
                "number": pr.get("id"),
                "title": pr.get("title", ""),
                "body": pr.get("description", "") or "",
                "baseRefOid": pr.get("destination", {}).get("commit", {}).get("hash", ""),
                "headRefOid": pr.get("source", {}).get("commit", {}).get("hash", ""),
                "mergedAt": pr.get("closed_on", pr.get("updated_on", "")),
                "createdAt": pr.get("created_on", ""),
                "url": pr.get("links", {}).get("html", {}).get("href", ""),
                "author": {
                    "login": author_login,
                    "isBot": _is_bot_username(author_login),
                    "__typename": "User"
                },
                "baseRepository": {"nameWithOwner": f"{self.owner}/{self.repo_name}"},
                "headRepository": {"nameWithOwner": f"{self.owner}/{self.repo_name}"},
                "files": {"nodes": files},
                "closingIssuesReferences": {"nodes": linked_issues}
            }
            pr_nodes.append(pr_node)

        # Create pageInfo
        page_info = {
            "hasNextPage": data.get("next") is not None,
            "endCursor": data.get("next")
        }

        # Try to get primary language from repo API
        primary_language_name = None
        try:
            languages = self.fetch_repo_languages()
            if languages:
                primary_language_name = list(languages.keys())[0]
        except Exception:
            pass

        # Create repository info - match GitHub format with pullRequests
        repo_info = {
            "primaryLanguage": {"name": primary_language_name},
            "owner": {"login": self.owner},
            "name": self.repo_name,
            "pullRequests": {
                "pageInfo": page_info,
                "nodes": pr_nodes
            }
        }

        # Return in GitHub-like format
        return {
            "data": {
                "repository": repo_info
            }
        }

    def fetch_issue(self, issue_number: int) -> Optional[dict]:
        """Fetch issue details by number."""
        import requests
        try:
            url = f"{self.base_url}/repositories/{self.owner}/{self.repo_name}/issues/{issue_number}"

            def _make_request():
                response = requests.get(url, headers=self.headers, timeout=30)
                response.raise_for_status()
                return response.json()

            issue_details = retry_api_call(_make_request)

            return {
                "number": issue_details.get("id"),
                "title": issue_details.get("title", ""),
                "body": issue_details.get("content", {}).get("raw", "") if isinstance(issue_details.get("content"), dict) else str(issue_details.get("content", "")),
                "state": issue_details.get("state", "").upper(),
                "__typename": "Issue"
            }
        except Exception:
            return None

    def get_repo_url(self, include_token: bool = False) -> str:
        """Get repository clone URL."""
        if include_token and self.token:
            return f"https://x-token-auth:{self.token}@bitbucket.org/{self.repo_full_name}.git"
        return f"https://bitbucket.org/{self.repo_full_name}.git"

    def extract_issue_number_from_text(self, text: str) -> List[int]:
        """Extract issue numbers from text."""
        if not text:
            return []
        issue_numbers = []
        # Bitbucket format: #123 or https://bitbucket.org/owner/repo/issues/123
        matches = re.findall(r'#(\d+)', text)
        issue_numbers.extend([int(m) for m in matches])
        url_matches = re.findall(r'https://bitbucket\.org/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+/issues/(\d+)', text)
        issue_numbers.extend([int(m) for m in url_matches])
        return list(set(issue_numbers))

    def fetch_repo_languages(self) -> Optional[Dict[str, int]]:
        """Fetch repository language from Bitbucket API."""
        import requests
        try:
            url = f"{self.base_url}/repositories/{self.owner}/{self.repo_name}"

            def _make_request():
                response = requests.get(url, headers=self.headers, timeout=30)
                response.raise_for_status()
                return response.json()

            repo_data = retry_api_call(_make_request)
            language = repo_data.get('language')

            if language:
                # Return in same format as GitHub (language -> byte count)
                # Since Bitbucket doesn't provide byte counts, use 1 as placeholder
                return {language: 1}
            return None
        except Exception as e:
            logger.debug(f"Failed to fetch repository language from Bitbucket API: {e}")
            return None


# Repository Analyzer
class RepoAnalyzer:
    """Analyze repository structure and metrics."""

    LANGUAGE_EXTENSIONS = {
        'Python': ['.py'],
        'JavaScript': ['.js', '.jsx', '.mjs'],
        'TypeScript': ['.ts', '.tsx'],
        'Java': ['.java'],
        'Scala': ['.scala'],
        'C++': ['.cpp', '.cc', '.cxx', '.hpp', '.h'],
        'C': ['.c', '.h'],
        'Go': ['.go'],
        'Rust': ['.rs'],
        'Ruby': ['.rb'],
        'PHP': ['.php'],
        'C#': ['.cs'],
        'Swift': ['.swift'],
        'Kotlin': ['.kt'],
    }

    TEST_PATTERNS = [
        r'test.*\.py$', r'.*_test\.py$',
        r'.*\.test\.(js|ts|jsx|tsx)$', r'.*\.spec\.(js|ts|jsx|tsx)$',
        r'test/.*', r'tests/.*', r'__tests__/.*',
        r'.*Test\.(java|scala)$', r'.*Spec\.(java|scala)$',
    ]

    CI_FILES = [
        '.github/workflows', '.gitlab-ci.yml', '.travis.yml',
        'Jenkinsfile', '.circleci', 'azure-pipelines.yml', '.drone.yml', 'buildkite.yml',
    ]

    TEST_FRAMEWORKS = {
        'pytest': ['pytest', 'pyproject.toml', 'pytest.ini', 'setup.cfg'],
        'unittest': ['unittest'],
        'jest': ['jest.config', 'package.json'],
        'mocha': ['mocha', '.mocharc', 'package.json'],
        'vitest': ['vitest.config', 'package.json'],
        'junit': ['junit', 'build.gradle', 'pom.xml'],
        'scalatest': ['scalatest', 'build.gradle', 'build.sbt'],
        'rspec': ['rspec', '.rspec', 'spec/'],
        'go test': ['_test.go'],
        'cargo test': ['Cargo.toml'],
    }

    def __init__(self, repo_path: str, owner: Optional[str] = None, repo_name: Optional[str] = None, platform_client: Optional[PlatformClient] = None):
        self.repo_path = Path(repo_path).resolve()
        if not self.repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")
        self.repo_name = self.repo_path.name
        self.is_git_repo = (self.repo_path / '.git').exists()
        self.owner = owner
        self.repo_name_github = repo_name
        self.platform_client = platform_client

    def analyze(self) -> RepoMetrics:
        """Run full repository analysis."""
        logger.info(f"Analyzing repository: {self.repo_name}")

        files = self._get_all_files()
        total_files = len(files)

        # Always count languages for metrics, but try GitHub API first for primary language
        language_counts = self._count_by_language(files)

        # Try to get primary language from platform API first
        primary_language = self._get_primary_language_from_api()

        # If GitHub API didn't return a language, fall back to file counting
        if not primary_language:
            primary_language = max(language_counts.items(), key=lambda x: x[1])[
                0] if language_counts else "Unknown"

            # If no language detected from files, try fallback detection
            if primary_language == "Unknown":
                primary_language = self._detect_language_from_indicators()

        source_files = self._count_source_files(files, language_counts)
        test_files = self._find_test_files(files)
        test_file_ratio = len(test_files) / \
            total_files if total_files > 0 else 0

        loc_counts = self._count_lines_of_code(files)
        ci_files = self._find_ci_files()
        has_ci_cd = len(ci_files) > 0
        test_frameworks = self._detect_test_frameworks()
        has_test_runner = len(test_frameworks) > 0

        git_metrics = self._analyze_git_history() if self.is_git_repo else {}

        # Try to find coverage reports
        test_coverage = self._find_coverage_reports()

        score_data = self._calculate_score(
            test_file_ratio=test_file_ratio,
            has_ci_cd=has_ci_cd,
            has_test_runner=has_test_runner,
            test_frameworks=test_frameworks,
            git_metrics=git_metrics,
            primary_language=primary_language,
            test_coverage=test_coverage,
        )

        return RepoMetrics(
            repo_name=self.repo_name,
            total_files=total_files,
            test_files=len(test_files),
            test_file_ratio=test_file_ratio,
            source_files=source_files,
            total_loc=loc_counts['total_loc'],
            source_loc=loc_counts['source_loc'],
            test_loc=loc_counts['test_loc'],
            languages=language_counts,
            primary_language=primary_language,
            has_ci_cd=has_ci_cd,
            ci_files=ci_files,
            test_frameworks=test_frameworks,
            has_test_runner=has_test_runner,
            total_commits=git_metrics.get('total_commits'),
            recent_commits_12mo=git_metrics.get('recent_commits_12mo'),
            commits_referencing_issues=git_metrics.get(
                'commits_referencing_issues', 0),
            test_coverage_percentage=test_coverage,
            swebench_readiness_score=score_data['score'],
            recommendation=score_data['recommendation'],
            strengths=[],
            weaknesses=[],
            commit_spread_days=git_metrics.get('commit_spread_days'),
            median_commit_interval_hours=git_metrics.get('median_commit_interval_hours'),
        )

    def _get_all_files(self) -> List[Path]:
        """Get all files in repository."""
        files = []
        if self.is_git_repo:
            try:
                result = subprocess.run(
                    ['git', 'ls-files'],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    timeout=30
                )

                if result.returncode == 0:
                    file_paths = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
                    for f in file_paths:
                        file_path = self.repo_path / f
                        if file_path.exists():
                            files.append(file_path)
                    if len(files) > 0:
                        return files
            except Exception:
                pass

        ignore_dirs = {'.git', 'node_modules', '__pycache__',
                       '.venv', 'venv', 'dist', 'build', '.gradle', 'target'}
        for root, dirs, filenames in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for filename in filenames:
                files.append(Path(root) / filename)
        return files

    def _get_primary_language_from_api(self) -> Optional[str]:
        """Get primary language from platform API based on highest byte count."""
        if not self.platform_client:
            return None

        try:
            languages = self.platform_client.fetch_repo_languages()
            if not languages:
                return None

            # Find language with highest byte count
            primary_language = max(languages.items(), key=lambda x: x[1])[0] if languages else None

            # Only return if the language exists in our supported languages
            if primary_language and primary_language in self.LANGUAGE_EXTENSIONS:
                return primary_language
            else:
                # return the next language with the highest byte count
                primary_language = list(languages.keys())[1] if len(languages) > 1 else None
                if primary_language and primary_language in self.LANGUAGE_EXTENSIONS:
                    return primary_language

            return None
        except Exception as e:
            logger.debug(f"Error getting primary language from API: {e}")
            return None

    def _count_by_language(self, files: List[Path]) -> Dict[str, int]:
        """Count files by language."""
        counts = {}
        for file_path in files:
            ext = file_path.suffix.lower()
            for language, extensions in self.LANGUAGE_EXTENSIONS.items():
                if ext in extensions:
                    counts[language] = counts.get(language, 0) + 1
                    break
        return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

    def _detect_language_from_indicators(self) -> str:
        """Detect language from indicator files when no source files are found."""
        # Language indicator files mapping
        indicators = {
            'Python': ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile', 'setup.cfg', 'tox.ini', 'manage.py'],
            'JavaScript': ['package.json', 'package-lock.json', 'yarn.lock', '.nvmrc', 'bower.json'],
            'TypeScript': ['tsconfig.json', 'tsconfig.*.json'],
            'Java': ['pom.xml', 'build.gradle', 'build.gradle.kts', 'gradlew', 'gradlew.bat', '.classpath', '.project'],
            'Scala': ['build.sbt', 'project/build.properties'],
            'Go': ['go.mod', 'go.sum', 'Gopkg.toml', 'Gopkg.lock', 'glide.yaml'],
            'Rust': ['Cargo.toml', 'Cargo.lock'],
            'Ruby': ['Gemfile', 'Gemfile.lock', 'Rakefile', '.ruby-version'],
            'PHP': ['composer.json', 'composer.lock', '.php-version'],
            'C#': ['.csproj', '.sln', 'project.json', 'paket.dependencies'],
            'Swift': ['Package.swift', '.swift-version'],
            'Kotlin': ['build.gradle.kts'],
            'C++': ['CMakeLists.txt', 'Makefile', 'configure', 'configure.ac'],
            'C': ['Makefile', 'configure', 'configure.ac', 'autogen.sh'],
        }

        # Check for indicator files
        for language, indicator_files in indicators.items():
            for indicator in indicator_files:
                # Handle patterns like 'tsconfig.*.json'
                if '*' in indicator:
                    pattern = indicator.replace('*', '.*')
                    for file_path in self.repo_path.rglob(indicator.split('*')[0] + '*'):
                        if file_path.is_file() and re.match(pattern, file_path.name):
                            return language
                else:
                    indicator_path = self.repo_path / indicator
                    if indicator_path.exists() and indicator_path.is_file():
                        return language

        return "Unknown"

    def _count_source_files(self, files: List[Path], language_counts: Dict[str, int]) -> int:
        """Count source files."""
        code_extensions = set()
        for lang in ['Python', 'JavaScript', 'TypeScript', 'Java', 'Scala', 'Go', 'Rust', 'C++', 'C']:
            if lang in language_counts:
                code_extensions.update(self.LANGUAGE_EXTENSIONS[lang])

        source_count = 0
        for file_path in files:
            ext = file_path.suffix.lower()
            if ext in code_extensions:
                rel_path = str(file_path.relative_to(self.repo_path))
                if not any(re.search(pattern, rel_path) for pattern in self.TEST_PATTERNS):
                    if not any(name in rel_path for name in ['config', 'setup', '__init__']):
                        source_count += 1
        return source_count

    def _count_lines_of_code(self, files: List[Path]) -> Dict[str, int]:
        """Count lines of code."""
        code_extensions = set()
        for lang in ['Python', 'JavaScript', 'TypeScript', 'Java', 'Scala', 'Go', 'Rust', 'C++', 'C', 'Ruby', 'PHP', 'C#', 'Swift', 'Kotlin']:
            code_extensions.update(self.LANGUAGE_EXTENSIONS.get(lang, []))

        total_loc = 0
        source_loc = 0
        test_loc = 0

        for file_path in files:
            ext = file_path.suffix.lower()
            if ext in code_extensions:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = [line for line in f if line.strip()]
                        loc = len(lines)

                    total_loc += loc
                    rel_path = str(file_path.relative_to(self.repo_path))
                    is_test = any(re.search(pattern, rel_path)
                                  for pattern in self.TEST_PATTERNS)

                    if is_test:
                        test_loc += loc
                    else:
                        source_loc += loc
                except Exception:
                    pass

        return {'total_loc': total_loc, 'source_loc': source_loc, 'test_loc': test_loc}

    def _find_test_files(self, files: List[Path]) -> List[Path]:
        """Find test files."""
        test_files = []
        for file_path in files:
            rel_path = str(file_path.relative_to(self.repo_path))
            if any(re.search(pattern, rel_path) for pattern in self.TEST_PATTERNS):
                test_files.append(file_path)
        return test_files

    def _find_ci_files(self) -> List[str]:
        """Find CI/CD files."""
        ci_files = []
        for ci_path in self.CI_FILES:
            full_path = self.repo_path / ci_path
            if full_path.exists():
                ci_files.append(ci_path)
        return ci_files

    def _detect_test_frameworks(self) -> List[str]:
        """Detect test frameworks."""
        frameworks = []
        for framework, indicators in self.TEST_FRAMEWORKS.items():
            for indicator in indicators:
                if '/' in indicator or '.' in indicator:
                    if (self.repo_path / indicator).exists():
                        if framework not in frameworks:
                            frameworks.append(framework)
                        break
                else:
                    config_files = ['package.json', 'pyproject.toml', 'requirements.txt',
                                    'build.gradle', 'pom.xml', 'Cargo.toml', 'go.mod']
                    for config_file in config_files:
                        config_path = self.repo_path / config_file
                        if config_path.exists():
                            try:
                                content = config_path.read_text()
                                if indicator in content:
                                    if framework not in frameworks:
                                        frameworks.append(framework)
                                    break
                            except Exception:
                                pass
        return frameworks

    def _find_coverage_reports(self) -> Optional[float]:
        """Find and parse coverage reports if available."""
        # Common coverage report locations
        coverage_paths = [
            self.repo_path / 'coverage.xml',
            self.repo_path / 'coverage' / 'coverage.xml',
            self.repo_path / 'coverage' / 'cobertura.xml',
            self.repo_path / 'htmlcov' / 'coverage.xml',
            self.repo_path / '.coverage.xml',
            self.repo_path / 'lcov.info',
            self.repo_path / 'coverage' / 'lcov.info',
            self.repo_path / 'coverage-final.json',
            self.repo_path / 'coverage' / 'coverage-final.json',
            self.repo_path / '.nyc_output' / 'coverage-final.json',
        ]

        for cov_path in coverage_paths:
            if not cov_path.exists():
                continue

            try:
                # Try parsing coverage.xml (Cobertura format)
                if cov_path.suffix == '.xml':
                    coverage = self._parse_coverage_xml(cov_path)
                    if coverage is not None:
                        logger.info(
                            f"Found coverage report: {cov_path} ({coverage:.1f}% coverage)")
                        return coverage

                # Try parsing lcov.info
                elif cov_path.name == 'lcov.info':
                    coverage = self._parse_lcov_info(cov_path)
                    if coverage is not None:
                        logger.info(
                            f"Found coverage report: {cov_path} ({coverage:.1f}% coverage)")
                        return coverage

                # Try parsing coverage-final.json (Istanbul/NYC)
                elif cov_path.name == 'coverage-final.json':
                    coverage = self._parse_coverage_json(cov_path)
                    if coverage is not None:
                        logger.info(
                            f"Found coverage report: {cov_path} ({coverage:.1f}% coverage)")
                        return coverage
            except Exception as e:
                logger.debug(
                    f"Failed to parse coverage report {cov_path}: {e}")
                continue

        return None

    def _parse_coverage_xml(self, xml_path: Path) -> Optional[float]:
        """Parse Cobertura XML coverage report."""
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Cobertura format: <coverage line-rate="0.85" branch-rate="0.70">
            line_rate = root.get('line-rate')
            if line_rate:
                return float(line_rate) * 100

            # Alternative: calculate from packages
            total_lines = 0
            covered_lines = 0
            for package in root.findall('.//package'):
                for class_elem in package.findall('.//class'):
                    for line in class_elem.findall('.//line'):
                        total_lines += 1
                        if line.get('hits') and int(line.get('hits', 0)) > 0:
                            covered_lines += 1

            if total_lines > 0:
                return (covered_lines / total_lines) * 100
        except Exception as e:
            logger.debug(f"Error parsing XML coverage: {e}")
        return None

    def _parse_lcov_info(self, lcov_path: Path) -> Optional[float]:
        """Parse LCOV info coverage report."""
        try:
            total_lines = 0
            covered_lines = 0

            with open(lcov_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    # LCOV format: DA:<line_number>,<execution_count>
                    if line.startswith('DA:'):
                        parts = line[3:].split(',')
                        if len(parts) == 2:
                            total_lines += 1
                            try:
                                if int(parts[1]) > 0:
                                    covered_lines += 1
                            except ValueError:
                                pass
                    # Use summary at end_of_record if available (more accurate)
                    elif line.startswith('LF:'):
                        # LF: total lines found
                        try:
                            lf_value = int(line.split(':')[1])
                            # Use summary if we haven't counted many lines yet
                            if total_lines < 100:  # Prefer summary for large files
                                total_lines = lf_value
                        except (ValueError, IndexError):
                            pass
                    elif line.startswith('LH:'):
                        # LH: lines hit
                        try:
                            lh_value = int(line.split(':')[1])
                            # Use summary if we haven't counted many lines yet
                            if covered_lines < 100:  # Prefer summary for large files
                                covered_lines = lh_value
                        except (ValueError, IndexError):
                            pass

            if total_lines > 0:
                return (covered_lines / total_lines) * 100
        except Exception as e:
            logger.debug(f"Error parsing LCOV coverage: {e}")
        return None

    def _parse_coverage_json(self, json_path: Path) -> Optional[float]:
        """Parse Istanbul/NYC coverage-final.json report."""
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)

            total_statements = 0
            covered_statements = 0

            # NYC format: { "path/to/file.js": { "s": { "1": 1, "2": 0, ... } } }
            for file_path, file_data in data.items():
                # Skip test files and node_modules
                if 'test' in file_path.lower() or 'node_modules' in file_path:
                    continue

                statements = file_data.get('s', {})
                for stmt_id, count in statements.items():
                    total_statements += 1
                    if count and count > 0:
                        covered_statements += 1

            if total_statements > 0:
                return (covered_statements / total_statements) * 100
        except Exception as e:
            logger.debug(f"Error parsing JSON coverage: {e}")
        return None

    def _calculate_score(
        self,
        test_file_ratio: float,
        has_ci_cd: bool,
        has_test_runner: bool,
        test_frameworks: List[str],
        git_metrics: Dict[str, Any],
        primary_language: str,
        test_coverage: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Calculate SWE-bench readiness score."""
        score = 0.0
        strengths = []
        weaknesses = []

        # Test coverage (40 points max)
        # Use actual coverage percentage if available, otherwise fall back to file ratio
        if test_coverage is not None:
            # Use actual coverage percentage (0-100 scale)
            # 100% coverage = 40 points
            test_score = min(test_coverage * 0.4, 40)
            score += test_score
            if test_coverage >= 80:
                strengths.append(
                    f"Excellent test coverage ({test_coverage:.1f}%)")
            elif test_coverage >= 60:
                strengths.append(f"Good test coverage ({test_coverage:.1f}%)")
            elif test_coverage >= 40:
                strengths.append(
                    f"Moderate test coverage ({test_coverage:.1f}%)")
            else:
                weaknesses.append(f"Low test coverage ({test_coverage:.1f}%)")
        else:
            # Fallback to file ratio
            test_score = min(test_file_ratio * 400, 40)
            score += test_score
            if test_file_ratio >= 0.10:
                strengths.append(
                    f"Good test file ratio ({test_file_ratio*100:.1f}%)")
            elif test_file_ratio >= 0.05:
                strengths.append(
                    f"Moderate test file ratio ({test_file_ratio*100:.1f}%)")
            else:
                weaknesses.append(
                    f"Low test file ratio ({test_file_ratio*100:.1f}%)")

        # CI/CD (15 points)
        if has_ci_cd:
            score += 15
            strengths.append("CI/CD pipeline configured")
        else:
            weaknesses.append("No CI/CD pipeline detected")

        # Test runner (15 points)
        if has_test_runner:
            score += 15
            strengths.append(f"Test frameworks: {', '.join(test_frameworks)}")
        else:
            weaknesses.append("No test framework detected")

        # Git activity (15 points)
        if git_metrics.get('recent_commits_12mo', 0) > 10:
            score += 15
            strengths.append(
                f"Active development ({git_metrics['recent_commits_12mo']} commits in 6mo)")
        elif git_metrics.get('recent_commits_12mo', 0) > 0:
            score += 7
            strengths.append(
                f"Some recent activity ({git_metrics['recent_commits_12mo']} commits in 6mo)")
        else:
            weaknesses.append("No recent commits (last 6 months)")

        # Issue tracking (15 points)
        issue_refs = git_metrics.get('commits_referencing_issues', 0)
        if issue_refs > 20:
            score += 15
            strengths.append(
                f"Good issue tracking ({issue_refs} commits reference issues)")
        elif issue_refs > 5:
            score += 10
            strengths.append(
                f"Some issue tracking ({issue_refs} commits reference issues)")
        elif issue_refs > 0:
            score += 5
        else:
            weaknesses.append("Few/no commits reference issues")

        # Recommendation
        if score >= 70:
            recommendation = "🌟 EXCELLENT - Highly suitable for SWE-Bench+ samples"
        elif score >= 50:
            recommendation = "✅ GOOD - Suitable for SWE-Bench+ samples with some limitations"
        elif score >= 30:
            recommendation = "⚠️  FAIR - May be suitable but has significant gaps"
        else:
            recommendation = "❌ POOR - Not recommended for SWE-Bench+ samples"

        return {
            'score': round(score, 1),
            'recommendation': recommendation,
            'strengths': strengths,
            'weaknesses': weaknesses,
        }

    def _analyze_git_history(self) -> Dict[str, Any]:
        """Analyze git history."""
        metrics = {}
        try:
            result = subprocess.run(
                ['git', 'rev-list', '--count', 'HEAD'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30
            )
            if result.returncode == 0:
                metrics['total_commits'] = int(result.stdout.strip())

            result = subprocess.run(
                ['git', 'rev-list', '--count', '--since=12.months.ago', 'HEAD'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30
            )
            if result.returncode == 0:
                metrics['recent_commits_12mo'] = int(result.stdout.strip())

            result = subprocess.run(
                ['git', 'log', '--all', '--oneline', '--grep=#[0-9]'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30
            )
            if result.returncode == 0:
                metrics['commits_referencing_issues'] = len(
                    result.stdout.strip().split('\n')) if result.stdout.strip() else 0

            # Calculate commit spread (days between first and latest commit)
            # Get ALL commit timestamps to find min (first) and max (latest)
            all_ts_result = subprocess.run(
                ['git', 'log', '--format=%ct'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=60
            )
            if all_ts_result.returncode == 0 and all_ts_result.stdout.strip():
                all_timestamps = [int(ts) for ts in all_ts_result.stdout.strip().split('\n') if ts]
                if len(all_timestamps) >= 2:
                    first_timestamp = min(all_timestamps)
                    latest_timestamp = max(all_timestamps)
                    spread_seconds = latest_timestamp - first_timestamp
                    metrics['commit_spread_days'] = round(spread_seconds / 86400, 1)  # 86400 seconds in a day

            # Calculate median commit interval in the last 90 days
            result = subprocess.run(
                ['git', 'log', '--since=90 days ago', '--format=%ct'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30
            )
            if result.returncode == 0 and result.stdout.strip():
                timestamps = [int(ts) for ts in result.stdout.strip().split('\n') if ts]
                if len(timestamps) >= 2:
                    # Sort timestamps in ascending order (oldest first)
                    timestamps.sort()
                    # Calculate intervals between consecutive commits
                    intervals_hours = []
                    for i in range(1, len(timestamps)):
                        interval_seconds = timestamps[i] - timestamps[i - 1]
                        intervals_hours.append(interval_seconds / 3600)  # Convert to hours
                    # Calculate median
                    intervals_hours.sort()
                    n = len(intervals_hours)
                    if n % 2 == 0:
                        median = (intervals_hours[n // 2 - 1] + intervals_hours[n // 2]) / 2
                    else:
                        median = intervals_hours[n // 2]
                    metrics['median_commit_interval_hours'] = round(median, 2)

        except Exception as e:
            logger.warning(f"Could not analyze git history: {e}")

        return metrics


# PR Analyzer
class PRAnalyzer:
    """Analyze PRs with rejection tracking."""

    def __init__(self, platform_client: PlatformClient, language_config: dict,
                 repo_path: str,
                 min_test_files: int = MIN_TEST_FILES, max_non_test_files: int = MAX_NON_TEST_FILES,
                 min_code_changes: int = MIN_PR_CODE_CHANGES, start_date: Optional[datetime] = None,
                 ):
        self.platform_client = platform_client
        self.owner = platform_client.owner
        self.repo_name = platform_client.repo_name
        self.repo_full_name = platform_client.repo_full_name
        self.repo_path = Path(repo_path)
        self.language_config = language_config
        self.min_test_files = min_test_files
        self.max_non_test_files = max_non_test_files
        self.min_code_changes = min_code_changes
        self.start_date = start_date

    def _commit_exists(self, sha: str) -> bool:
        """Check if a commit exists in the local repo."""
        check = subprocess.run(
            ['git', 'cat-file', '-t', sha],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=10
        )
        return check.returncode == 0

    def _fetch_pr_ref(self, pr_number: int) -> bool:
        """Fetch a PR's head ref from origin."""
        try:
            result = subprocess.run(
                ['git', 'fetch', 'origin', f'pull/{pr_number}/head:pr-{pr_number}'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=60
            )
            return result.returncode == 0
        except Exception as e:
            logger.debug(f"Failed to fetch PR ref: {e}")
            return False

    def _get_patch_from_git(self, base_sha: str, head_sha: str, pr_number: Optional[int] = None) -> Optional[str]:
        """Get patch/diff between two commits, with API fallback."""
        patch = None

        # Try local git first
        try:
            # Check if commits exist, try to fetch PR ref if head is missing
            if not self._commit_exists(head_sha) and pr_number:
                logger.debug(f"Head commit {head_sha[:8]} not found, fetching PR #{pr_number} ref...")
                self._fetch_pr_ref(pr_number)

            # Try git diff if both commits exist
            if self._commit_exists(base_sha) and self._commit_exists(head_sha):
                result = subprocess.run(
                    ['git', 'diff', f'{base_sha}..{head_sha}'],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    timeout=60
                )
                if result.returncode == 0 and result.stdout:
                    return result.stdout
                else:
                    logger.debug(f"Git diff failed: {result.stderr}")
            else:
                logger.debug(f"Commits not available locally (base: {self._commit_exists(base_sha)}, head: {self._commit_exists(head_sha)})")

        except subprocess.TimeoutExpired:
            logger.debug(f"Git diff timed out for {base_sha}..{head_sha}")
        except Exception as e:
            logger.debug(f"Git diff error: {e}")

        # Fallback to API
        logger.debug(f"Falling back to API for patch {base_sha[:8]}..{head_sha[:8]}")
        try:
            from repo_evaluator_helpers import get_full_patch_content
            patch = get_full_patch_content(
                self.repo_full_name,
                base_sha,
                head_sha,
                token=self.platform_client.token
            )
            if patch:
                logger.debug(f"Successfully retrieved patch from API")
            return patch
        except Exception as e:
            logger.warning(f"API patch retrieval failed: {e}")
            return None

    def analyze_prs(self, max_prs: Optional[int] = None) -> PRRejectionStats:
        """Analyze PRs and track rejections."""
        logger.info(f"Analyzing PRs for {self.repo_full_name}...")

        cursor = None
        total_prs = 0
        accepted = 0
        rejected = 0
        rejection_reasons = {}
        accepted_prs = []

        while True:
            try:
                res = self.platform_client.fetch_prs(cursor, page_size=50, start_date=self.start_date)

                if res.get('errors'):
                    error_msg = res['errors'][0]['message']
                    # Check for rate limit errors
                    if "rate limit" in error_msg.lower() or "403" in error_msg:
                        logger.error(
                            f"API rate limit exceeded. Please provide a token using --token")
                    logger.error(f"API error: {error_msg}")
                    break

                repo_data = res.get('data', {}).get('repository', {})
                res.get('data', {}).get('search', {})
                pr_data = repo_data.get('pullRequests', {})
                language_name = repo_data.get(
                    'primaryLanguage', {}).get('name', None)
                pr_nodes = pr_data.get('nodes', [])
                page_info = pr_data.get('pageInfo', {})

                if not pr_nodes:
                    break

                for pr_data in pr_nodes:
                    if max_prs and total_prs >= max_prs:
                        break

                    logger.info(f"Processing PR #{pr_data['number']}...")

                    # Parse dates - handle both GitHub (Z suffix) and Bitbucket (no Z) formats
                    created_at_str = pr_data['createdAt']
                    if created_at_str.endswith('Z'):
                        created_at_str = created_at_str.replace('Z', '+00:00')
                    elif '+' not in created_at_str and created_at_str.count(':') == 2:
                        # Bitbucket format without timezone - assume UTC
                        created_at_str = created_at_str + '+00:00'
                    pr_created_at = normalize_to_utc(datetime.fromisoformat(created_at_str))

                    merged_at_str = pr_data['mergedAt']
                    if merged_at_str.endswith('Z'):
                        merged_at_str = merged_at_str.replace('Z', '+00:00')
                    elif '+' not in merged_at_str and merged_at_str.count(':') == 2:
                        # Bitbucket format without timezone - assume UTC
                        merged_at_str = merged_at_str + '+00:00'
                    pr_merged_at = normalize_to_utc(datetime.fromisoformat(merged_at_str))
                    pr_number = pr_data['number']

                    total_prs += 1

                    # Apply filters
                    failed_filter = None
                    filter_reason = None

                    # Bot filter - skip PRs from bots
                    author_info = pr_data.get('author', {})
                    # Check __typename to see if author is a Bot
                    is_bot = author_info.get('__typename') == 'Bot' if author_info else False
                    author_login = author_info.get('login', '') if author_info else ''

                    # Also check username pattern as fallback
                    if not is_bot and author_login:
                        is_bot = _is_bot_username(author_login)

                    if is_bot:
                        failed_filter = "bot_pr"
                        filter_reason = f"PR is from bot account: {author_login}"

                    # Date filters
                    if not failed_filter and self.start_date and pr_merged_at < self.start_date:
                        failed_filter = "merge_date"
                        filter_reason = f"PR merged {pr_merged_at.date()} before start date {self.start_date.date()}"
                    elif pr_created_at is None:
                        failed_filter = "creation_date"
                        filter_reason = "PR has no createdAt date"

                    # Content filter
                    if not failed_filter:
                        pr_body = pr_data.get('body', '') or ''
                        if not (is_english(pr_data.get('title', '')) and is_english(pr_body)):
                            failed_filter = "content_not_in_english"
                            filter_reason = "Content may not be in English"

                    # Closing issues validation
                    if not failed_filter:
                        closing_issues = pr_data.get('closingIssuesReferences', {}).get('nodes', [])

                        # If no closing issues from API, try regex extraction from PR body
                        if not closing_issues:
                            issue_numbers = self.platform_client.extract_issue_number_from_text(pr_body)
                            if issue_numbers:
                                logger.info(f"PR #{pr_number}: Using regex fallback for issues {issue_numbers} via API.")
                                for issue_num in issue_numbers:
                                    try:
                                        issue_data_from_api = self.platform_client.fetch_issue(issue_num)
                                        if issue_data_from_api:
                                            closing_issues.append(issue_data_from_api)
                                    except Exception as e:
                                        logger.warning(f"Failed to fetch fallback issue #{issue_num} via API: {e}")

                        # If we have closing issues, validate them
                        if closing_issues:
                            found_valid_issue = False
                            for issue_data in closing_issues:
                                issue_number = issue_data.get('number')
                                issue_typename = issue_data.get('__typename', 'Issue')

                                # Check if issue is not a PR
                                if issue_typename == 'PullRequest':
                                    continue  # Skip this issue, try next one

                                # Check if issue is closed
                                issue_state = issue_data.get('state', '').lower()
                                if issue_state != 'closed':
                                    continue  # Skip this issue, try next one

                                # Check word count
                                issue_body = issue_data.get('body', '') or ''
                                if not has_valid_issue_word_count(issue_body):
                                    continue  # Skip this issue, try next one

                                # If we get here, this issue passed all validations
                                found_valid_issue = True
                                break  # Found a valid issue, no need to check others

                            # If no issue passed validation, reject the PR
                            if not found_valid_issue:
                                # Use the first issue's failure reason (or a generic one)
                                first_issue = closing_issues[0]
                                issue_number = first_issue.get('number')
                                issue_typename = first_issue.get('__typename', 'Issue')

                                if issue_typename == 'PullRequest':
                                    failed_filter = "issue_is_a_pr"
                                    filter_reason = f"Linked issue #{issue_number} is a Pull Request"
                                else:
                                    issue_state = first_issue.get('state', '').lower()
                                    if issue_state != 'closed':
                                        failed_filter = "issue_is_not_closed"
                                        filter_reason = f"Linked issue #{issue_number} is not closed (state: {issue_state})"
                                    else:
                                        issue_body = first_issue.get('body', '') or ''
                                        word_count = count_words(issue_body)
                                        failed_filter = "issue_word_count"
                                        filter_reason = f"Issue #{issue_number} word count ({word_count}) is outside {MIN_ISSUE_WORDS}-{MAX_ISSUE_WORDS} range"
                        # If no closing issues found at all, continue with PR analysis (don't reject)

                    # File filters
                    if not failed_filter:
                        pr_files_nodes = pr_data.get(
                            'files', {}).get('nodes', [])
                        test_files = [f for f in pr_files_nodes if is_test_file_path(
                            f['path'], self.language_config) and not is_asset_file_path(f['path'], self.language_config)]
                        non_test_files = [f for f in pr_files_nodes if not is_test_file_path(
                            f['path'], self.language_config) and not is_asset_file_path(f['path'], self.language_config)]

                        if len(test_files) < self.min_test_files:
                            failed_filter = "fewer_than_min_test_files"
                            filter_reason = f"PR has fewer than {self.min_test_files} test files"
                        elif len(non_test_files) > self.max_non_test_files:
                            failed_filter = "more_than_max_non_test_files"
                            filter_reason = f"PR has more than {self.max_non_test_files} non-test files"
                        elif len(non_test_files + test_files) <= 5:
                            failed_filter = "difficulty_not_hard"
                            filter_reason = "PR has less than 5 files (difficulty not hard enough)"
                        elif len(test_files) > MAX_TEST_FILES:
                            failed_filter = "too_many_test_files"
                            filter_reason = f"PR has more than {MAX_TEST_FILES} test files"
                        else:
                            code_files = [f for f in pr_files_nodes if not _is_data_file(f['path'])]
                            if len(code_files) > MAX_CHANGED_FILES:
                                failed_filter = "too_many_changed_files"
                                filter_reason = f"PR has more than {MAX_CHANGED_FILES} changed code files"

                    # Code changes filter (requires patch)
                    if not failed_filter:
                        try:
                            full_patch = self._get_patch_from_git(
                                pr_data['baseRefOid'],
                                pr_data['headRefOid'],
                                pr_number=pr_number
                            )
                            if not full_patch:
                                failed_filter = "full_patch_retrieval"
                                filter_reason = "Could not retrieve full patch"
                            else:
                                # Rust embedded tests check
                                if language_name == "Rust" and has_rust_embedded_tests(pr_files_nodes, full_patch, self.language_config):
                                    failed_filter = "rust_embedded_tests"
                                    filter_reason = "Rust files contain embedded tests"
                                else:
                                    # Check code changes
                                    has_sufficient, source_changes = has_sufficient_code_changes(
                                        full_patch,
                                        self.language_config,
                                        self.min_code_changes
                                    )
                                    if not has_sufficient:
                                        failed_filter = "code_changes_not_sufficient"
                                        filter_reason = f"Code changes {source_changes} below {self.min_code_changes}"
                        except Exception as e:
                            logger.warning(
                                f"Error processing PR #{pr_number}: {e}")
                            failed_filter = "pr_processing_error"
                            filter_reason = f"Exception during processing: {str(e)}"

                    # Track results
                    if failed_filter:
                        rejected += 1
                        rejection_reasons[failed_filter] = rejection_reasons.get(
                            failed_filter, 0) + 1
                        logger.info(
                            f"PR #{pr_number} rejected: {failed_filter} - {filter_reason}")
                    else:
                        accepted += 1
                        accepted_prs.append(pr_data)
                        logger.info(f"PR #{pr_number} accepted")

                if max_prs and total_prs >= max_prs:
                    break

                if not page_info.get('hasNextPage'):
                    break
                cursor = page_info.get('endCursor')

            except Exception as e:
                error_str = str(e)
                # Check for rate limit errors
                if "rate limit" in error_str.lower() or "403" in error_str:
                    logger.error(
                        f"API rate limit exceeded. Please provide a token using --token")
                    logger.error(f"Error: {e}")
                elif "Failed to resolve" in error_str or "nodename nor servname" in error_str:
                    logger.error(
                        f"Network/DNS error fetching PRs from {self.repo_full_name}: {e}")
                    logger.error("This could be a temporary network issue. Please check your internet connection and try again.")
                else:
                    logger.error(
                        f"Error fetching PRs from {self.repo_full_name} for cursor {cursor}: {e}")
                break

        # Build rejection breakdown
        rejection_breakdown = {}
        for filter_name, count in rejection_reasons.items():
            rejection_breakdown[filter_name] = {
                'count': count,
                'percentage': round((count / rejected * 100) if rejected > 0 else 0, 1)
            }

        acceptance_rate = (accepted / total_prs) if total_prs > 0 else 0.0

        return PRRejectionStats(
            total_prs=total_prs,
            accepted=accepted,
            rejected=rejected,
            acceptance_rate=round(acceptance_rate, 3),
            rejection_breakdown=rejection_breakdown,
            accepted_prs=accepted_prs
        )


class RepoEvaluator:
    def __init__(self, repo_path: str, owner: str, repo_name: str,
                 platform_client: PlatformClient,
                 min_test_files: int = MIN_TEST_FILES,
                 max_non_test_files: int = MAX_NON_TEST_FILES,
                 min_code_changes: int = MIN_PR_CODE_CHANGES,
                 start_date: Optional[datetime] = None,
                 max_prs: Optional[int] = None,
                 skip_f2p: bool = False,
                 f2p_timeout: int = 600):
        self.repo_path = repo_path
        self.owner = owner
        self.repo_name = repo_name
        self.repo_full_name = f"{owner}/{repo_name}"
        self.platform_client = platform_client

        self.min_test_files = min_test_files
        self.max_non_test_files = max_non_test_files
        self.min_code_changes = min_code_changes
        self.start_date = start_date
        self.max_prs = max_prs
        self.skip_f2p = skip_f2p
        self.f2p_timeout = f2p_timeout

        self.language_config = load_language_config()

    def evaluate(self) -> AnalysisReport:
        if not self.platform_client:
            raise ValueError("Platform client is required")
        if not self.owner:
            raise ValueError("Owner is required")
        if not self.repo_name:
            raise ValueError("Repository name is required")

        logger.info(f"Evaluating repository: {self.repo_full_name}")

        repo_analyzer = RepoAnalyzer(
            repo_path=self.repo_path,
            owner=self.owner,
            repo_name=self.repo_name,
            platform_client=self.platform_client
        )
        repo_metrics = repo_analyzer.analyze()

        primary_language = repo_metrics.primary_language
        if primary_language in ["Vue", "React"]:
            primary_language = "TypeScript"

        language_config = get_language_config(primary_language)
        if not language_config:
            logger.warning(
                f"Language '{primary_language}' not found, using generic fallback")
            language_config = get_language_config(
                "Unknown")  # Generic fallback

        pr_analyzer = PRAnalyzer(
            platform_client=self.platform_client,
            language_config=language_config,
            repo_path=self.repo_path,
            min_test_files=self.min_test_files,
            max_non_test_files=self.max_non_test_files,
            min_code_changes=self.min_code_changes,
            start_date=self.start_date,
        )

        try:
            pr_analysis = pr_analyzer.analyze_prs(max_prs=self.max_prs)
            if pr_analysis.total_prs == 0:
                logger.warning("No PRs were analyzed. This could be due to:")
                logger.warning(
                    "Rate limit exceeded (provide --token)") if not self.platform_client.token else None
                logger.warning("No merged PRs found in the repository")
                logger.warning("API access issues")
        except Exception as e:
            logger.error(f"Error analyzing PRs: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            pr_analysis = PRRejectionStats(
                total_prs=0,
                accepted=0,
                rejected=0,
                acceptance_rate=0.0,
                rejection_breakdown={},
                accepted_prs=[]
            )

        if not self.skip_f2p and pr_analysis.accepted_prs:
            pr_analysis = self._run_f2p_analysis(pr_analysis, primary_language)

        # Calculate overall score (weighted: 60% repo, 40% PR acceptance rate)
        repo_score = repo_metrics.swebench_readiness_score
        pr_score = pr_analysis.acceptance_rate * \
            100 if pr_analysis.total_prs > 0 else 0
        overall_score = (repo_score * 0.6) + (pr_score * 0.4)

        # Overall recommendation
        if overall_score >= 70:
            recommendation = "🌟 GREAT"
        elif overall_score >= 50:
            recommendation = "✅ GOOD"
        elif overall_score >= 30:
            recommendation = "⚠️ FAIR"
        else:
            recommendation = "❌ POOR"

        return AnalysisReport(
            repo_name=self.repo_name,
            repo_full_name=self.repo_full_name,
            repo_metrics=repo_metrics,
            pr_analysis=pr_analysis,
            overall_score=overall_score,
            recommendation=recommendation
        )

    def _run_f2p_analysis(self, pr_analysis: PRRejectionStats, primary_language: str) -> PRRejectionStats:
        from test_runners import F2PP2PAnalyzer, preflight_check, get_runner

        check = preflight_check(self.repo_path, primary_language)
        if not check["can_run"]:
            blockers = check['blockers']
            reason = blockers[0]['message'] if blockers else "Unknown blocker"
            logger.warning(f"F2P analysis skipped: {blockers}")
            pr_analysis.f2p_skipped_reason = reason
            return pr_analysis

        logger.info(f"Running F2P/P2P analysis on {len(pr_analysis.accepted_prs)} accepted PRs...")
        logger.info(f"Detected: {check['detected']}")

        runner = get_runner(Path(self.repo_path), primary_language)
        if not runner:
            logger.warning("F2P analysis skipped: No suitable test runner found")
            pr_analysis.f2p_skipped_reason = "No suitable test runner found"
            return pr_analysis

        logger.info(f"Using runner: {runner.name} ({runner.language})")

        f2p_validated_prs = []
        f2p_results = []
        f2p_rejection_reasons = {}

        for pr in pr_analysis.accepted_prs:
            pr_number = pr.get('number')
            logger.info(f"F2P analysis for PR #{pr_number}...")

            analyzer = F2PP2PAnalyzer(
                repo_path=Path(self.repo_path),
                runner=runner,
                test_timeout=self.f2p_timeout,
                language_hint=primary_language,
            )
            pr_files = [f['path'] for f in pr.get('files', {}).get('nodes', [])]
            result = analyzer.analyze(
                pr_number=pr_number,
                pr_title=pr.get('title', ''),
                base_sha=pr.get('baseRefOid', ''),
                head_sha=pr.get('headRefOid', ''),
                pr_files=pr_files,
            )

            f2p_results.append(result.to_dict())

            if result.success and result.has_valid_f2p and result.has_valid_p2p:
                logger.info(f"PR #{pr_number}: ✅ VALID (F2P: {len(result.f2p_tests)}, P2P: {len(result.p2p_tests)})")
                pr['f2p_result'] = result.to_dict()
                f2p_validated_prs.append(pr)
            else:
                reason = result.rejection_reason or result.error_code or 'f2p_invalid'
                if reason == 'empty_p2p':
                    message = 'No P2P tests found'
                elif reason == 'empty_f2p':
                    message = 'No F2P tests found'
                else:
                    message = result.error or 'Invalid F2P/P2P'
                logger.info(f"PR #{pr_number}: ❌ REJECTED - {reason}: {message}")
                f2p_rejection_reasons[reason] = f2p_rejection_reasons.get(reason, 0) + 1

        rejection_breakdown = pr_analysis.rejection_breakdown.copy()
        f2p_rejected_count = sum(f2p_rejection_reasons.values())
        if f2p_rejected_count > 0:
            total_rejected = pr_analysis.rejected + f2p_rejected_count
            for reason, count in f2p_rejection_reasons.items():
                rejection_breakdown[reason] = {
                    'count': count,
                    'percentage': round((count / total_rejected * 100) if total_rejected > 0 else 0, 1)
                }

        new_accepted = len(f2p_validated_prs)
        new_rejected = pr_analysis.rejected + f2p_rejected_count
        new_acceptance_rate = new_accepted / pr_analysis.total_prs if pr_analysis.total_prs > 0 else 0.0

        return PRRejectionStats(
            accepted_prs=f2p_validated_prs,
            total_prs=pr_analysis.total_prs,
            accepted=new_accepted,
            rejected=new_rejected,
            acceptance_rate=round(new_acceptance_rate, 3),
            rejection_breakdown=rejection_breakdown,
            f2p_results=f2p_results
        )


# Output functions
def print_report(report: AnalysisReport):
    """Print human-readable report to console."""
    print(f"\n{'='*60}")
    print(f"REPOSITORY EVALUATION REPORT")
    print(f"{'='*60}")
    print(f"Repository: {report.repo_full_name}")
    print(f"Language: {report.repo_metrics.primary_language}")

    print(f"Overall Score: {report.overall_score}/100")
    print(f"Recommendation: {report.recommendation}\n")
    print()

    print("--- Repository Metrics ---")
    print(f"Total files: {report.repo_metrics.total_files}")
    print(f"Source files: {report.repo_metrics.source_files}")
    print(f"Test files: {report.repo_metrics.test_files}")
    print(
        f"Test coverage ratio: {report.repo_metrics.test_file_ratio*100:.1f}%")
    if report.repo_metrics.test_coverage_percentage is not None:
        print(
            f"Test coverage (from reports): {report.repo_metrics.test_coverage_percentage:.1f}%")
    print(f"Total LoC: {report.repo_metrics.total_loc:,}")
    print(f"Source LoC: {report.repo_metrics.source_loc:,}")
    print(f"Test LoC: {report.repo_metrics.test_loc:,}")
    print(f"CI/CD: {'✅' if report.repo_metrics.has_ci_cd else '❌'}")
    print(
        f"Test frameworks: {', '.join(report.repo_metrics.test_frameworks) if report.repo_metrics.test_frameworks else 'None'}")
    if report.repo_metrics.total_commits:
        print(f"Total commits: {report.repo_metrics.total_commits:,}")
        if report.repo_metrics.recent_commits_12mo:
            print(
                f"Recent commits (6mo): {report.repo_metrics.recent_commits_12mo:,}")
    if report.repo_metrics.commit_spread_days is not None:
        print(f"Commit spread: {report.repo_metrics.commit_spread_days:,.1f} days")
    if report.repo_metrics.median_commit_interval_hours is not None:
        print(f"Median commit interval (90d): {report.repo_metrics.median_commit_interval_hours:,.2f} hours")

    print(f"\n--- PR Analysis ---")
    print(f"Total PRs Analyzed: {report.pr_analysis.total_prs}")
    print(f"Accepted PRs: {len(report.pr_analysis.accepted_prs)}")
    for pr in report.pr_analysis.accepted_prs:
        f2p_info = ""
        if 'f2p_result' in pr:
            f2p = pr['f2p_result']
            f2p_info = f" [F2P: {f2p.get('f2p_count', 0)}, P2P: {f2p.get('p2p_count', 0)}]"
        print(f"  - {pr['title']} (#{pr['number']}){f2p_info}")
    print(
        f"Accepted: {report.pr_analysis.accepted} ({report.pr_analysis.acceptance_rate*100:.1f}%)")
    print(
        f"Rejected: {report.pr_analysis.rejected} ({(1-report.pr_analysis.acceptance_rate)*100:.1f}%)")

    if report.pr_analysis.rejection_breakdown:
        print(f"\nRejection Breakdown:")
        sorted_rejections = sorted(
            report.pr_analysis.rejection_breakdown.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )
        for filter_name, stats in sorted_rejections:
            print(
                f" {filter_name}: {stats['count']} ({stats['percentage']}%)")

    if report.pr_analysis.f2p_results:
        print(f"\n--- F2P Analysis Results ---")
        valid_f2p_count = sum(1 for r in report.pr_analysis.f2p_results if r.get('verdict') == 'VALID')
        total_f2p_tests = sum(r.get('f2p_count', 0) for r in report.pr_analysis.f2p_results)
        total_p2p_tests = sum(r.get('p2p_count', 0) for r in report.pr_analysis.f2p_results)
        total_analyzed = len(report.pr_analysis.f2p_results)
        valid_pct = (valid_f2p_count / total_analyzed * 100) if total_analyzed > 0 else 0
        print(f"PRs with valid F2P: {valid_f2p_count} ({valid_pct:.1f}%)")
        print(f"Total F2P tests found: {total_f2p_tests}")
        print(f"Total P2P tests found: {total_p2p_tests}")
    elif report.pr_analysis.f2p_skipped_reason:
        print(f"\n--- F2P Analysis ---")
        print(f"⚠️  Skipped: {report.pr_analysis.f2p_skipped_reason}")

def to_json(report: AnalysisReport) -> dict:
    """Convert report to JSON-serializable dict."""
    accepted_prs_clean = []
    for pr in report.pr_analysis.accepted_prs:
        pr_data = {
            'number': pr.get('number'),
            'title': pr.get('title'),
            'url': pr.get('url'),
            'baseRefOid': pr.get('baseRefOid'),
            'headRefOid': pr.get('headRefOid'),
        }
        if 'f2p_result' in pr:
            pr_data['f2p_result'] = pr['f2p_result']
        accepted_prs_clean.append(pr_data)

    result = {
        'repo_name': report.repo_name,
        'repo_full_name': report.repo_full_name,
        'overall_score': report.overall_score,
        'recommendation': report.recommendation,
        'repo_metrics': asdict(report.repo_metrics),
        'pr_analysis': {
            'total_prs': report.pr_analysis.total_prs,
            'accepted': report.pr_analysis.accepted,
            'rejected': report.pr_analysis.rejected,
            'acceptance_rate': report.pr_analysis.acceptance_rate,
            'rejection_breakdown': report.pr_analysis.rejection_breakdown,
            'accepted_prs': accepted_prs_clean,
        }
    }

    if report.pr_analysis.f2p_results:
        result['pr_analysis']['f2p_results'] = report.pr_analysis.f2p_results
    elif report.pr_analysis.f2p_skipped_reason:
        result['pr_analysis']['f2p_skipped_reason'] = report.pr_analysis.f2p_skipped_reason

    return result


def clone_repo(repo_full_name: str, temp_dir: Path, token: str, platform: str = 'github', shallow: bool = False) -> Path:
    """Clone repository to a temporary directory."""
    import shutil

    if platform == 'bitbucket':
        repo_url = f"https://x-token-auth:{token}@bitbucket.org/{repo_full_name}.git"
    else:  # github
        # Fine-grained PATs (github_pat_*) and classic PATs both work with x-access-token
        if token:
            repo_url = f"https://x-access-token:{token}@github.com/{repo_full_name}.git"
        else:
            repo_url = f"https://github.com/{repo_full_name}.git"

    clone_path = temp_dir / repo_full_name.replace('/', '_')

    cmd = ['git', 'clone']
    if shallow:
        cmd += ['--depth', '1']   # faster for RAG indexing
    cmd += [repo_url, str(clone_path)]

    # Try with token first if provided
    try:
        logger.info(f"Cloning {repo_full_name} (shallow={shallow}) to {clone_path}...")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=120,          # 120 s max — prevents indefinite hang
        )
        if result.returncode == 0:
            logger.info("Successfully cloned repository")
            return clone_path
    except Exception as e:
        logger.warning(f"Initial clone attempt failed with exception: {e}")
        # Initialize result with a dummy object in case subprocess.run raised an exception
        class DummyResult:
            returncode = -1
            stderr = str(e)
        result = DummyResult()

    # Fallback: if token was provided, retry WITHOUT the token in case it's a public repo and the token was invalid/expired
    if token:
        logger.info(f"Retrying clone of {repo_full_name} without authentication token...")
        public_repo_url = f"https://github.com/{repo_full_name}.git" if platform != 'bitbucket' else f"https://bitbucket.org/{repo_full_name}.git"
        fallback_cmd = ['git', 'clone']
        if shallow:
            fallback_cmd += ['--depth', '1']
        fallback_cmd += [public_repo_url, str(clone_path)]
        
        # Clean up any partial clone directory first
        if clone_path.exists():
            shutil.rmtree(clone_path, ignore_errors=True)
            
        try:
            result = subprocess.run(
                fallback_cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=120,
            )
            if result.returncode == 0:
                logger.info("Successfully cloned repository using unauthenticated fallback")
                return clone_path
        except Exception as e:
            logger.warning(f"Fallback clone attempt failed with exception: {e}")

    # If all attempts failed, handle error
    stderr = getattr(result, 'stderr', '').strip()
    # Surface a friendly error for auth failures
    if '403' in stderr or 'Write access' in stderr or 'Authentication' in stderr:
        raise RuntimeError(
            f"GitHub authentication failed for '{repo_full_name}'. "
            f"Check that your GITHUB_TOKEN has 'Contents: Read' permission. "
            f"Detail: {stderr[:300]}"
        )
    raise RuntimeError(f"Failed to clone repository: {stderr[:500]}")


def parse_repo_name(repo_string: str) -> Tuple[str, str]:
    """Parse owner/repo-name format, handling platform prefixes."""
    repo_string = repo_string.strip()

    # Remove platform prefix if present
    if repo_string.startswith('bitbucket:'):
        repo_string = repo_string[10:]  # Remove 'bitbucket:'
    elif repo_string.startswith('github:'):
        repo_string = repo_string[7:]  # Remove 'github:'

    # Extract from URL if present
    if 'bitbucket' in repo_string or 'github.com' in repo_string:
        # Extract owner/repo from URL
        match = re.search(r'/([^/]+)/([^/]+?)(?:\.git)?/?$', repo_string)
        if match:
            return match.group(1), match.group(2)

    if '/' not in repo_string:
        raise ValueError(
            f"Invalid repo format: {repo_string}. Expected 'owner/repo-name'")

    parts = repo_string.split('/')
    if len(parts) != 2:
        raise ValueError(
            f"Invalid repo format: {repo_string}. Expected 'owner/repo-name'")

    return parts[0], parts[1]


def main():
    parser = argparse.ArgumentParser(
        description='Evaluate repositories for SWE-bench sample creation suitability'
    )
    parser.add_argument(
        'repo',
        help='Repository in format owner/repo-name (e.g., microsoft/vscode)'
    )
    parser.add_argument(
        '--repo-path',
        help='Path to local repository directory (if not provided, will auto-clone)',
        default=None
    )
    parser.add_argument(
        '--github-token',
        help='GitHub token for API access (deprecated, use --token)',
        default=None
    )
    parser.add_argument(
        '--token',
        help='API token for platform access (GitHub or Bitbucket)',
        default=None
    )
    parser.add_argument(
        '--platform',
        choices=['auto', 'github', 'bitbucket'],
        default='auto',
        help='Platform to use (default: auto-detect from repo string)'
    )
    parser.add_argument(
        '--min-test-files',
        type=int,
        default=MIN_TEST_FILES,
        help=f'Minimum test files per PR (default: {MIN_TEST_FILES})'
    )
    parser.add_argument(
        '--max-non-test-files',
        type=int,
        default=MAX_NON_TEST_FILES,
        help=f'Maximum non-test files per PR (default: {MAX_NON_TEST_FILES})'
    )
    parser.add_argument(
        '--min-code-changes',
        type=int,
        default=MIN_PR_CODE_CHANGES,
        help=f'Minimum code changes per PR (default: {MIN_PR_CODE_CHANGES})'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser.add_argument(
        '--max-prs',
        type=int,
        default=None,
        help='Maximum number of PRs to evaluate (default: None)'
    )
    parser.add_argument(
        '--start-date',
        type=str,
        default=None,
        help='Start date for evaluating PRs (YYYY-MM-DD)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output file (default: None)'
    )
    parser.add_argument(
        '--skip-f2p',
        action='store_true',
        help='Skip F2P/P2P test verification'
    )
    parser.add_argument(
        '--f2p-timeout',
        type=int,
        default=600,
        help='Timeout for F2P test execution per PR in seconds (default: 600)'
    )

    args = parser.parse_args()

    if args.start_date:
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    else:
        start_date = None

    # Detect platform
    platform = detect_platform(args.repo, args.platform)
    logger.info(f"Detected platform: {platform}")

    # Get token (prefer --token, fallback to --github-token for backward compatibility)
    token = args.token or args.github_token
    if not token:
        logger.warning("No token provided. API rate limits may apply.")

    # Parse repo name
    try:
        owner, repo_name = parse_repo_name(args.repo)
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)

    # Create platform client
    if platform == 'bitbucket':
        platform_client = BitbucketClient(owner, repo_name, token)
    else:
        platform_client = GitHubClient(owner, repo_name, token)

    repo_path = args.repo_path
    temp_dir = None
    should_cleanup = True

    if not repo_path:
        # Auto-clone to temp directory
        temp_dir = Path(tempfile.mkdtemp(prefix='repo_evaluator_'))
        try:
            # if not token:
            #     raise ValueError("Token is required for cloning repositories")
            repo_path = str(clone_repo(
                f"{owner}/{repo_name}", temp_dir, token, platform))
        except Exception as e:
            logger.error(f"Failed to clone repository: {e}")
            if temp_dir and temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)
            sys.exit(1)
    else:
        repo_path = str(Path(repo_path).resolve())
        if not Path(repo_path).exists():
            logger.error(f"Repository path does not exist: {repo_path}")
            sys.exit(1)

    # Run evaluation
    try:
        evaluator = RepoEvaluator(
            repo_path=repo_path,
            owner=owner,
            repo_name=repo_name,
            platform_client=platform_client,
            min_test_files=args.min_test_files,
            max_non_test_files=args.max_non_test_files,
            min_code_changes=args.min_code_changes,
            start_date=start_date,
            max_prs=args.max_prs,
            skip_f2p=args.skip_f2p,
            f2p_timeout=args.f2p_timeout
        )

        report = evaluator.evaluate()

        # Output
        if args.json:
            output = json.dumps(to_json(report), indent=2)
            if args.output:
                Path(args.output).write_text(output)
                print(f"Results saved to {args.output}")
            else:
                print(output)
                output_dir = Path(os.getcwd() + '/output')
                os.makedirs(output_dir, exist_ok=True)
                filepath = os.path.join(output_dir, Path(f"{args.repo.replace('/', '__')}.json"))

                with open(filepath, 'w') as f:
                    f.write(output)
        else:
            print_report(report)
            output = json.dumps(to_json(report), indent=2)
            output_dir = Path(os.getcwd() + '/output')
            os.makedirs(output_dir, exist_ok=True)
            filepath = os.path.join(output_dir, Path(f"{args.repo.replace('/', '__')}.json"))

            with open(filepath, 'w') as f:
                f.write(output)

    except Exception as e:
        logger.error(f"Error evaluating repository: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        if should_cleanup and temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == '__main__':
    main()
