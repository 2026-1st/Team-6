from __future__ import annotations

import csv
import html
import re
from collections import Counter, defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INTERIM_DIR = PROJECT_ROOT / "data" / "interim"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
EMBEDDING_DIR = PROJECT_ROOT / "data" / "embeddings"
FIGURE_DIR = PROJECT_ROOT / "output" / "figures"
TABLE_DIR = PROJECT_ROOT / "output" / "tables"

for directory in [FIGURE_DIR, TABLE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


CITY_CONFIGS = [
    ("Philadelphia", "philly", INTERIM_DIR / "yelp_subset_philly_15k.csv"),
    ("Tucson", "tucson", INTERIM_DIR / "yelp_subset_tucson_15k.csv"),
    ("New Orleans", "new_orleans", INTERIM_DIR / "yelp_subset_new_orleans_15k.csv"),
]

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from",
    "had", "has", "have", "he", "her", "his", "i", "in", "is", "it", "its",
    "me", "my", "of", "on", "or", "our", "she", "so", "that", "the", "their",
    "there", "they", "this", "to", "was", "we", "were", "with", "you", "your",
    "food", "place", "restaurant", "good", "great", "time", "one", "really",
    "even", "came", "went", "got", "make", "will", "go", "ordered", "us",
    "back", "much", "well",
}


def read_rows(path: Path):
    with path.open(encoding="utf-8", newline="") as file:
        yield from csv.DictReader(file)


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def svg_bar_chart(title: str, rows: list[tuple[str, float]], path: Path, x_label: str = "") -> None:
    width = 820
    row_height = 44
    top = 70
    left = 190
    right = 40
    height = top + row_height * len(rows) + 50
    chart_width = width - left - right
    max_value = max((value for _, value in rows), default=1)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="32" y="38" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#222">{html.escape(title)}</text>',
    ]
    for idx, (label, value) in enumerate(rows):
        y = top + idx * row_height
        bar_width = int(chart_width * (value / max_value)) if max_value else 0
        parts.append(f'<text x="32" y="{y + 24}" font-family="Arial, sans-serif" font-size="14" fill="#333">{html.escape(label)}</text>')
        parts.append(f'<rect x="{left}" y="{y}" width="{bar_width}" height="26" rx="3" fill="#4f7cac"/>')
        parts.append(f'<text x="{left + bar_width + 8}" y="{y + 19}" font-family="Arial, sans-serif" font-size="13" fill="#222">{value:,.0f}</text>')
    if x_label:
        parts.append(f'<text x="{left}" y="{height - 18}" font-family="Arial, sans-serif" font-size="12" fill="#666">{html.escape(x_label)}</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def summarize_eda(city_name: str, city_slug: str, input_path: Path) -> None:
    grouped = defaultdict(lambda: {"review_count": 0, "stars_sum": 0.0, "text_len_sum": 0})
    word_counts = {0: Counter(), 1: Counter()}

    for row in read_rows(input_path):
        label = int(float(row["is_positive"]))
        stars = float(row["stars"])
        text = row.get("text", "")
        grouped[label]["review_count"] += 1
        grouped[label]["stars_sum"] += stars
        grouped[label]["text_len_sum"] += len(text)

        words = re.findall(r"[A-Za-z]{3,}", text.lower())
        word_counts[label].update(word for word in words if word not in STOPWORDS and city_slug.replace("_", "") not in word)

    summary_rows = []
    for label in [0, 1]:
        stats = grouped[label]
        count = stats["review_count"]
        summary_rows.append(
            {
                "city": city_name,
                "is_positive": label,
                "review_count": count,
                "avg_stars": round(stats["stars_sum"] / count, 4) if count else 0,
                "avg_text_length": round(stats["text_len_sum"] / count, 2) if count else 0,
            }
        )

    write_csv(
        TABLE_DIR / f"eda_{city_slug}_summary.csv",
        summary_rows,
        ["city", "is_positive", "review_count", "avg_stars", "avg_text_length"],
    )

    svg_bar_chart(
        f"{city_name} 만족도 분포",
        [("불만족 리뷰", grouped[0]["review_count"]), ("만족 리뷰", grouped[1]["review_count"])],
        FIGURE_DIR / f"eda_{city_slug}_target_distribution.svg",
        "리뷰 수",
    )

    top_words = []
    for label in [0, 1]:
        label_text = "불만족" if label == 0 else "만족"
        for word, count in word_counts[label].most_common(8):
            top_words.append((f"{label_text}: {word}", count))
    svg_bar_chart(
        f"{city_name} 주요 리뷰 단어",
        top_words,
        FIGURE_DIR / f"eda_{city_slug}_top_words.svg",
        "단어 빈도",
    )


def csv_shape(path: Path) -> tuple[int, int]:
    with path.open(encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = sum(1 for _ in reader)
    return rows, len(header)


def write_data_inventory() -> None:
    files = [
        ("중간 데이터", path) for _, _, path in CITY_CONFIGS
    ] + [
        ("처리 데이터", PROCESSED_DIR / "yelp_subset_philly_15k_features.csv"),
        ("처리 데이터", PROCESSED_DIR / "yelp_subset_tucson_15k_features.csv"),
        ("처리 데이터", PROCESSED_DIR / "yelp_subset_new_orleans_15k_features.csv"),
        ("임베딩 데이터", EMBEDDING_DIR / "philly_pca_32.csv"),
        ("임베딩 데이터", EMBEDDING_DIR / "tucson_pca_32.csv"),
        ("임베딩 데이터", EMBEDDING_DIR / "new_orleans_pca_32.csv"),
    ]
    rows = []
    for stage, path in files:
        row_count, column_count = csv_shape(path)
        rows.append(
            {
                "단계": stage,
                "파일": str(path.relative_to(PROJECT_ROOT)),
                "행 수": row_count,
                "컬럼 수": column_count,
            }
        )
    write_csv(TABLE_DIR / "data_inventory.csv", rows, ["단계", "파일", "행 수", "컬럼 수"])


def main() -> None:
    for city_name, city_slug, input_path in CITY_CONFIGS:
        summarize_eda(city_name, city_slug, input_path)
    write_data_inventory()
    print(f"표 산출물 생성 완료: {TABLE_DIR}")
    print(f"그래프 산출물 생성 완료: {FIGURE_DIR}")


if __name__ == "__main__":
    main()
