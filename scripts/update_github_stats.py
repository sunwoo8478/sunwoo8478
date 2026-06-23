#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import os
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "github-stats-card.svg"
USERNAME = os.getenv("GITHUB_STATS_USERNAME", "sunwoo8478")
TOKEN = os.getenv("PROFILE_STATS_TOKEN") or os.getenv("GITHUB_TOKEN")

LANG_COLORS = {
    "HTML": "#e34c26",
    "JavaScript": "#f1e05a",
    "Java": "#b07219",
    "PHP": "#4F5D95",
    "CSS": "#563d7c",
    "SCSS": "#c6538c",
    "Python": "#3572A5",
    "Kotlin": "#A97BFF",
    "TypeScript": "#3178c6",
    "Shell": "#89e051",
}


def escape(value: object) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def graphql(query: str, variables: dict) -> dict:
    if not TOKEN:
        raise RuntimeError("GITHUB_TOKEN or PROFILE_STATS_TOKEN is required")

    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "sunwoo8478-profile-stats",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode())
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    return payload["data"]


def collect_stats() -> dict:
    today = dt.datetime.now(dt.timezone.utc)
    since = today - dt.timedelta(days=365)

    query = """
    query ProfileStats($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
          }
          totalCommitContributions
          totalIssueContributions
          totalPullRequestContributions
          totalRepositoryContributions
        }
        repositories(first: 100, ownerAffiliations: OWNER, isFork: false, orderBy: {field: UPDATED_AT, direction: DESC}) {
          nodes {
            stargazerCount
            languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
              edges {
                size
                node {
                  name
                  color
                }
              }
            }
          }
        }
      }
    }
    """
    data = graphql(
        query,
        {
            "login": USERNAME,
            "from": since.isoformat(),
            "to": today.isoformat(),
        },
    )
    user = data["user"]
    contributions = user["contributionsCollection"]

    stars = 0
    language_sizes: dict[str, int] = {}
    language_colors: dict[str, str] = {}

    for repo in user["repositories"]["nodes"]:
        stars += repo.get("stargazerCount") or 0
        for edge in repo.get("languages", {}).get("edges", []):
            name = edge["node"]["name"]
            language_sizes[name] = language_sizes.get(name, 0) + int(edge["size"] or 0)
            language_colors[name] = edge["node"].get("color") or LANG_COLORS.get(name, "#8b949e")

    total_lang = sum(language_sizes.values()) or 1
    languages = [
        {
            "name": name,
            "percent": round(size / total_lang * 100, 2),
            "color": language_colors.get(name) or LANG_COLORS.get(name, "#8b949e"),
        }
        for name, size in sorted(language_sizes.items(), key=lambda item: item[1], reverse=True)[:8]
    ]

    return {
        "stars": stars,
        "total_contributions": contributions["contributionCalendar"]["totalContributions"],
        "commit_contributions": contributions["totalCommitContributions"],
        "pull_requests": contributions["totalPullRequestContributions"],
        "issues": contributions["totalIssueContributions"],
        "repository_contributions": contributions["totalRepositoryContributions"],
        "languages": languages,
    }


def language_bar(languages: list[dict], x: int = 64, y: int = 430, total_width: int = 632) -> str:
    parts = [f'<rect x="{x}" y="{y}" width="{total_width}" height="16" rx="8" fill="#21262d"/>']
    cursor = x
    for index, language in enumerate(languages):
        width = max(4, round(total_width * language["percent"] / 100))
        rx = ' rx="8"' if index == 0 or index == len(languages) - 1 else ""
        parts.append(
            f'<rect x="{cursor}" y="{y}" width="{width}" height="16"{rx} fill="{language["color"]}"/>'
        )
        cursor += width
    return "\n      ".join(parts)


def language_legend(languages: list[dict]) -> str:
    rows = []
    for index, language in enumerate(languages[:8]):
        col = index % 2
        row = index // 2
        x = 64 + (340 * col)
        y = 480 + (36 * row)
        rows.append(
            f'<circle cx="{x + 10}" cy="{y + 8}" r="9" fill="{language["color"]}"/>\n'
            f'      <text x="{x + 30}" y="{y + 15}" fill="#c9d1d9">{escape(language["name"])} {language["percent"]:.2f}%</text>'
        )
    return "\n\n      ".join(rows)


def render(stats: dict) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="760" height="620" viewBox="0 0 760 620" role="img" aria-labelledby="title desc" preserveAspectRatio="xMidYMid meet">
  <title id="title">이선우 GitHub 통계</title>
  <desc id="desc">GitHub 활동과 사용 언어를 자동 갱신하는 다크 통계 카드</desc>

  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0d1117"/>
      <stop offset="1" stop-color="#0b1220"/>
    </linearGradient>
    <filter id="softShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#000000" flood-opacity="0.35"/>
    </filter>
  </defs>

  <rect width="760" height="620" rx="22" fill="url(#bg)"/>
  <rect x="20" y="20" width="720" height="580" rx="18" fill="none" stroke="#30363d"/>

  <g font-family="Pretendard, Noto Sans KR, Apple SD Gothic Neo, Segoe UI, sans-serif">
    <text x="64" y="76" fill="#58a6ff" font-size="30" font-weight="800">이선우의 GitHub 통계</text>
    <text x="64" y="108" fill="#8b949e" font-size="14">GitHub Actions 자동 갱신 · 공식 contribution graph 기준</text>

    <g transform="translate(64 142)">
      <rect width="632" height="220" rx="18" fill="#0b1220" stroke="#21262d"/>

      <g transform="translate(30 30)" font-size="22" font-weight="760">
        <text x="42" y="24" fill="#c9d1d9">받은 스타 수</text>
        <text x="476" y="24" fill="#c9d1d9" text-anchor="end">{escape(stats["stars"])}</text>

        <text x="42" y="64" fill="#c9d1d9">전체 기여 수</text>
        <text x="476" y="64" fill="#c9d1d9" text-anchor="end">{escape(stats["total_contributions"])}</text>

        <text x="42" y="104" fill="#c9d1d9">커밋 기여</text>
        <text x="476" y="104" fill="#c9d1d9" text-anchor="end">{escape(stats["commit_contributions"])}</text>

        <text x="42" y="144" fill="#c9d1d9">PR 횟수</text>
        <text x="476" y="144" fill="#c9d1d9" text-anchor="end">{escape(stats["pull_requests"])}</text>

        <text x="42" y="184" fill="#c9d1d9">이슈 개수</text>
        <text x="476" y="184" fill="#c9d1d9" text-anchor="end">{escape(stats["issues"])}</text>
      </g>

      <g transform="translate(30 30)" fill="none" stroke="#1f6feb" stroke-width="2.7" stroke-linecap="round" stroke-linejoin="round">
        <path d="M13 2.5l3.2 6.4 7.1 1-5.1 5 1.2 7-6.4-3.4-6.3 3.4 1.2-7-5.1-5 7.1-1z"/>
        <path transform="translate(0 40)" d="M12 2a10 10 0 1 0 10 10"/>
        <path transform="translate(0 40)" d="M12 6v7l5 3"/>
        <path transform="translate(0 80)" d="M8 4h8M12 4v18M6 10l6-6 6 6M6 18l6 6 6-6"/>
        <circle transform="translate(0 120)" cx="12" cy="12" r="10"/>
        <path transform="translate(0 120)" d="M12 7v6"/>
        <circle transform="translate(0 120)" cx="12" cy="17" r="1"/>
        <path transform="translate(0 160)" d="M5 4h14a2 2 0 0 1 2 2v13H3V6a2 2 0 0 1 2-2z"/>
        <path transform="translate(0 160)" d="M8 23h8"/>
      </g>

      <g transform="translate(535 54)" filter="url(#softShadow)">
        <circle cx="42" cy="42" r="42" fill="#0f2747"/>
        <circle cx="42" cy="42" r="34" fill="#c9d1d9"/>
        <circle cx="42" cy="42" r="29" fill="#0d1117"/>
        <path fill="#c9d1d9" transform="translate(12 10) scale(0.58)" d="M52 4c-27 0-49 22-49 49 0 21 13 38 31 45 2 0 3-1 3-2V86c-12 3-15-5-15-5-2-5-5-7-5-7-4-3 0-3 0-3 5 0 8 5 8 5 4 8 12 6 15 4 0-3 2-6 3-7-10-1-20-5-20-23 0-5 2-9 5-13-1-1-2-6 0-12 0 0 4-1 13 5 4-1 8-2 12-2s8 1 12 2c9-6 13-5 13-5 2 6 1 11 0 12 3 4 5 8 5 13 0 18-10 22-20 23 2 2 3 5 3 10v15c0 1 1 2 3 2 18-7 31-24 31-45C101 26 79 4 52 4z"/>
      </g>
    </g>

    <text x="64" y="398" fill="#58a6ff" font-size="30" font-weight="800">Most Used Languages</text>

    <g>
      {language_bar(stats["languages"])}
    </g>

    <g font-size="19" font-weight="560">
      {language_legend(stats["languages"])}
    </g>
  </g>
</svg>
"""


def main() -> None:
    stats = collect_stats()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(stats), encoding="utf-8")
    print(f"updated {OUT}")


if __name__ == "__main__":
    main()
