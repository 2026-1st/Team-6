# Feature_Engineering.ipynb 코드 설명 및 결과 해석

이 문서는 `feature_engineering/Feature_Engineering.ipynb`에서 수행하는 2단계 피처 엔지니어링 과정을 정리한 문서입니다.

목표는 1단계에서 만든 도시별 샘플 리뷰 CSV에 모델 학습에 사용할 수 있는 파생변수를 추가하고, 최종 결과를 `data/processed/`에 저장하는 것입니다.

## 1. 노트북의 입력과 출력

### 입력 데이터

노트북은 다음 파일을 입력으로 사용합니다.

```text
data/interim/yelp_subset_philly_15k.csv
data/interim/yelp_subset_tucson_15k.csv
data/interim/yelp_subset_new_orleans_15k.csv
data/interim/business_location.csv
```

도시별 리뷰 CSV에는 기본적으로 다음 컬럼이 들어 있습니다.

```text
review_id, user_id, business_id, stars, useful, funny, cool, text, date, is_positive
```

`business_location.csv`에는 위치 기반 피처를 만들기 위한 컬럼이 들어 있습니다.

```text
business_id, city, state, latitude, longitude
```

### 출력 데이터

피처 엔지니어링이 끝난 결과는 다음 파일로 저장됩니다.

```text
data/processed/yelp_subset_philly_15k_features.csv
data/processed/yelp_subset_tucson_15k_features.csv
data/processed/yelp_subset_new_orleans_15k_features.csv
```

Colab에서 실행할 경우 실제 저장 경로는 다음과 같습니다.

```text
/content/drive/MyDrive/ml_project/Team-6/data/processed
```

## 2. 환경 설정 셀

노트북 첫 코드 셀에서는 Google Drive를 mount하고 프로젝트 경로를 설정합니다.

```python
from google.colab import drive
drive.mount('/content/drive')

PROJECT_ROOT = Path('/content/drive/MyDrive/ml_project/Team-6')
```

입력 데이터는 `data/interim`에서 찾고, 출력 데이터는 `data/processed`에 저장합니다.

```python
INPUT_DIR = find_input_dir(PROJECT_ROOT)
OUTPUT_DIR = PROJECT_ROOT / 'data' / 'processed'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

`find_input_dir()` 함수는 우선 다음 경로에서 샘플 CSV를 찾습니다.

```text
data/interim
sampling
eda_sampling
```

현재 정리된 구조에서는 `data/interim`을 사용하는 것이 정상입니다.

## 3. 입력 파일 확인 셀

`check_input_files()` 함수는 도시별 샘플 CSV가 모두 존재하는지 확인합니다.

확인 대상:

```text
yelp_subset_philly_15k.csv
yelp_subset_tucson_15k.csv
yelp_subset_new_orleans_15k.csv
```

파일이 없으면 `FileNotFoundError`를 발생시켜 어느 파일이 누락되었는지 알려줍니다.

## 4. 텍스트 기반 피처 생성

`add_text_features(df)` 함수는 리뷰 본문인 `text` 컬럼을 기반으로 파생변수를 생성합니다.

생성되는 컬럼:

| 컬럼 | 의미 |
|---|---|
| `text_length` | 리뷰 텍스트의 전체 글자 수 |
| `word_count` | 리뷰 단어 수 |
| `sentence_count` | 문장 수 추정값 |
| `avg_word_length` | 평균 단어 길이 |
| `uppercase_ratio` | 전체 글자 중 대문자 비중 |
| `exclamation_count` | 느낌표 개수 |
| `question_count` | 물음표 개수 |
| `engagement_sum` | `useful`, `funny`, `cool` 합계 |

예를 들어 `uppercase_ratio`는 리뷰에서 대문자가 차지하는 비중입니다. 감정이 강한 리뷰일수록 대문자, 느낌표, 물음표 사용량이 달라질 수 있으므로 감성 분류 모델에 도움이 될 수 있습니다.

## 5. 날짜 기반 피처 생성

`add_date_features(df)` 함수는 `date` 컬럼을 날짜 타입으로 변환한 뒤 시간 관련 파생변수를 만듭니다.

생성되는 컬럼:

| 컬럼 | 의미 |
|---|---|
| `review_year` | 리뷰 작성 연도 |
| `review_month` | 리뷰 작성 월 |
| `review_dayofweek` | 리뷰 작성 요일 |
| `is_weekend` | 주말 여부 |

`is_weekend`는 토요일 또는 일요일에 작성된 리뷰이면 `1`, 아니면 `0`입니다.

## 6. 유저 기준 피처 생성

`add_user_features(df)` 함수는 `user_id` 기준으로 유저의 리뷰 작성 패턴을 요약합니다.

생성되는 컬럼:

| 컬럼 | 의미 |
|---|---|
| `user_review_count` | 현재 샘플 안에서 해당 유저가 작성한 리뷰 수 |
| `user_avg_stars` | 현재 샘플 안에서 해당 유저가 준 평균 별점 |
| `user_star_deviation` | 현재 리뷰 별점과 해당 유저 평균 별점의 차이 |

예시:

```text
stars = 5
user_avg_stars = 3.666667
user_star_deviation = 1.333333
```

이 경우 해당 유저는 평균적으로 3.67점을 주는 편인데, 현재 리뷰에서는 5점을 줬으므로 평소보다 높게 평가한 리뷰로 볼 수 있습니다.

주의할 점은 이 값들이 전체 Yelp 데이터 기준이 아니라, 현재 15k 샘플 안에서 계산된 값이라는 점입니다.

## 7. 식당 기준 피처 생성

`add_business_features(df)` 함수는 `business_id` 기준으로 식당별 리뷰 패턴을 요약합니다.

생성되는 컬럼:

| 컬럼 | 의미 |
|---|---|
| `business_review_count` | 현재 샘플 안에서 해당 식당에 달린 리뷰 수 |
| `business_avg_stars` | 현재 샘플 안에서 해당 식당의 평균 별점 |
| `business_star_deviation` | 현재 리뷰 별점과 해당 식당 평균 별점의 차이 |

예시:

```text
stars = 5
business_avg_stars = 4.538462
business_star_deviation = 0.461538
```

이 경우 현재 리뷰는 해당 식당의 평균 평점보다 약간 높은 평가입니다.

## 8. 위치 정보 병합

`load_business_locations(business_ids)` 함수는 `business_location.csv`에서 필요한 식당의 위도와 경도를 불러옵니다.

노트북은 우선 다음 파일을 찾습니다.

```text
data/interim/business_location.csv
```

해당 파일이 있으면 원본 `business.json`을 읽지 않고, 바로 위치 정보만 병합합니다.

생성 또는 병합되는 컬럼:

| 컬럼 | 의미 |
|---|---|
| `latitude` | 식당 위도 |
| `longitude` | 식당 경도 |

이 단계가 정상적으로 수행되면 결과 데이터프레임에 `latitude`, `longitude`가 채워집니다.

## 9. K-Means 상권 클러스터링

`add_kmeans_cluster(df)` 함수는 위도와 경도를 이용해 식당을 위치 기반 클러스터로 묶습니다.

생성되는 컬럼:

| 컬럼 | 의미 |
|---|---|
| `business_cluster` | K-Means 기반 상권 클러스터 번호 |

기본 클러스터 수는 다음 값입니다.

```python
KMEANS_CLUSTERS = 5
```

`business_cluster` 값은 순위가 아닙니다. 예를 들어 `0`, `1`, `2`, `3`, `4`는 단순히 서로 다른 위치 그룹을 의미합니다.

위도와 경도 결측치가 없으면 K-Means가 정상적으로 수행됩니다. 위치 정보가 없으면 클러스터링은 건너뜁니다.

## 10. 도시별 피처 생성 및 저장

도시별 피처 생성은 다음 루프에서 진행됩니다.

```python
feature_datasets = {}

for config in CITY_CONFIGS:
    city = config['city']
    input_path = INPUT_DIR / config['input_file']
    output_path = OUTPUT_DIR / config['output_file']

    df = pd.read_csv(input_path)
    feature_df = add_all_features(df, location_df)
    feature_df.to_csv(output_path, index=False)
    feature_datasets[city] = feature_df
```

이 셀은 다음 작업을 도시별로 반복합니다.

1. 샘플 CSV 로드
2. 텍스트 피처 생성
3. 날짜 피처 생성
4. 유저 기준 피처 생성
5. 식당 기준 피처 생성
6. 위치 정보 병합
7. K-Means 클러스터 생성
8. `data/processed`에 CSV 저장

## 11. 최종 저장 셀

노트북 끝부분에는 최종 저장 확인용 셀이 추가되어 있습니다.

이 셀은 `feature_datasets`에 있는 도시별 결과를 다시 한번 `data/processed/`에 저장하고, 저장 결과를 표로 보여줍니다.

출력되는 확인 항목:

| 컬럼 | 의미 |
|---|---|
| `city` | 도시명 |
| `path` | 저장된 CSV 경로 |
| `rows` | 저장된 행 수 |
| `columns` | 저장된 컬럼 수 |
| `file_size_mb` | 저장된 파일 크기 |

이 셀을 실행하면 최종 CSV 파일이 실제로 저장되었는지 확인할 수 있습니다.

## 12. 실행 결과 해석

실행 결과 예시에서 Philadelphia 데이터는 다음과 같이 출력되었습니다.

```text
5 rows × 31 columns
```

이는 기존 샘플 CSV의 기본 컬럼에 피처 엔지니어링 컬럼들이 추가되어 총 31개 컬럼이 되었다는 의미입니다.

결과 예시에서 확인된 주요 컬럼은 다음과 같습니다.

```text
is_weekend
user_review_count
user_avg_stars
user_star_deviation
business_review_count
business_avg_stars
business_star_deviation
latitude
longitude
business_cluster
```

예시 행 해석:

```text
stars = 5
user_avg_stars = 3.666667
user_star_deviation = 1.333333
```

이 유저는 평균적으로 약 3.67점을 주는 편인데, 해당 리뷰에서는 5점을 주었으므로 유저 기준으로는 긍정적으로 치우친 리뷰입니다.

```text
business_avg_stars = 4.538462
business_star_deviation = 0.461538
```

이 리뷰는 해당 식당의 평균 별점보다 약간 높은 평가입니다.

```text
latitude = 40.052064
longitude = -75.127394
business_cluster = 4
```

해당 식당의 위치 정보가 정상적으로 병합되었고, K-Means 결과 4번 상권 클러스터에 배정되었다는 뜻입니다.

## 13. 현재 결과의 의미

현재 결과는 2단계 피처 엔지니어링이 정상적으로 진행되었음을 보여줍니다.

특히 다음 항목이 정상적으로 생성된 것이 중요합니다.

- 텍스트 기반 피처
- 날짜 기반 피처
- 유저 기준 피처
- 식당 기준 피처
- 위치 정보
- K-Means 상권 클러스터

따라서 이 결과 CSV는 3단계 RoBERTa 임베딩 또는 4단계 모델링의 입력 데이터로 사용할 수 있습니다.

## 14. 다음 단계

다음 단계에서는 `text` 컬럼을 RoBERTa 모델에 통과시켜 텍스트 임베딩을 생성합니다.

3단계 결과는 다음 폴더에 저장하는 것을 권장합니다.

```text
data/embeddings/
```

모델링 단계에서는 다음 데이터를 결합해 사용할 수 있습니다.

```text
data/processed/*_features.csv
data/embeddings/*
```
