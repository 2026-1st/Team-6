# 2단계 피처 엔지니어링 작업 순서

## 목표

1단계에서 만든 도시별 샘플 CSV에 모델 성능 향상을 위한 파생변수를 추가한다. 원본 샘플 CSV는 덮어쓰지 않고, 피처가 추가된 파일은 `*_features.csv` 형태로 별도 저장한다.

## 입력 데이터

- `yelp_subset_philly_15k.csv`
- `yelp_subset_tucson_15k.csv`
- `yelp_subset_new_orleans_15k.csv`

기본 컬럼 예시:

```text
review_id, user_id, business_id, stars, useful, funny, cool, text, date, is_positive
```

K-Means 상권 클러스터링을 하려면 원본 `business.json`에서 아래 컬럼을 추가로 가져와야 한다.

```text
business_id, latitude, longitude
```

## 전체 진행 순서

### 1. 샘플 CSV 로드 및 기본 점검

먼저 도시별 샘플 CSV를 불러온 뒤 데이터 크기, 컬럼, 결측치, 타겟 분포를 확인한다.

확인 항목:

```python
df.shape
df.columns
df.isnull().sum()
df['is_positive'].value_counts()
```

이 단계에서 `text`, `date`, `user_id`, `business_id`, `stars` 컬럼이 있는지 확인한다.

### 2. 텍스트 기반 파생변수 생성

샘플 CSV만으로 만들 수 있는 변수부터 생성한다. 이 단계는 빠르고 안정적이므로 가장 먼저 진행한다.

추천 변수:

```text
text_length
word_count
sentence_count
avg_word_length
uppercase_ratio
exclamation_count
question_count
engagement_sum
```

예시 코드:

```python
df['text'] = df['text'].fillna('').astype(str)

df['text_length'] = df['text'].str.len()
df['word_count'] = df['text'].str.split().str.len()
df['sentence_count'] = df['text'].str.count(r'[.!?]+').clip(lower=1)
df['avg_word_length'] = df['text_length'] / df['word_count'].clip(lower=1)
df['uppercase_ratio'] = df['text'].apply(
    lambda text: sum(1 for char in text if char.isupper()) / max(len(text), 1)
)
df['exclamation_count'] = df['text'].str.count('!')
df['question_count'] = df['text'].str.count(r'\?')
df['engagement_sum'] = df[['useful', 'funny', 'cool']].sum(axis=1)
```

### 3. 날짜 기반 파생변수 생성

`date` 컬럼을 날짜 타입으로 변환한 뒤 리뷰 작성 시점 관련 변수를 만든다.

추천 변수:

```text
review_year
review_month
review_dayofweek
is_weekend
```

예시 코드:

```python
df['date'] = pd.to_datetime(df['date'])

df['review_year'] = df['date'].dt.year
df['review_month'] = df['date'].dt.month
df['review_dayofweek'] = df['date'].dt.dayofweek
df['is_weekend'] = df['review_dayofweek'].isin([5, 6]).astype(int)
```

### 4. 유저 기준 파생변수 생성

`user_id` 기준으로 유저의 리뷰 수와 평균 평점을 계산한 뒤, 현재 리뷰 평점이 해당 유저 평균과 얼마나 다른지 계산한다.

추천 변수:

```text
user_review_count
user_avg_stars
user_star_deviation
```

예시 코드:

```python
user_stats = df.groupby('user_id')['stars'].agg(
    user_review_count='count',
    user_avg_stars='mean'
).reset_index()

df = df.merge(user_stats, on='user_id', how='left')
df['user_star_deviation'] = df['stars'] - df['user_avg_stars']
```

주의: 이 값은 전체 Yelp 데이터 기준 유저 성향이 아니라, 현재 샘플 안에서 계산한 값이다.

### 5. 식당 기준 파생변수 생성

`business_id` 기준으로 식당별 리뷰 수와 평균 평점을 계산한다.

추천 변수:

```text
business_review_count
business_avg_stars
business_star_deviation
```

예시 코드:

```python
business_stats = df.groupby('business_id')['stars'].agg(
    business_review_count='count',
    business_avg_stars='mean'
).reset_index()

df = df.merge(business_stats, on='business_id', how='left')
df['business_star_deviation'] = df['stars'] - df['business_avg_stars']
```

### 6. 위치 정보 병합

K-Means 상권 클러스터링을 위해 원본 `business.json`에서 `latitude`, `longitude`를 가져와 샘플 데이터에 붙인다.

예시 코드:

```python
biz_location = biz_df[['business_id', 'latitude', 'longitude']]
df = df.merge(biz_location, on='business_id', how='left')
```

병합 후 확인:

```python
df[['latitude', 'longitude']].isnull().sum()
```

### 7. K-Means 상권 클러스터링

위도와 경도를 표준화한 뒤 K-Means로 식당 위치 기반 클러스터를 만든다.

추천 변수:

```text
business_cluster
```

예시 코드:

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

coords = df[['latitude', 'longitude']].dropna()

scaler = StandardScaler()
coords_scaled = scaler.fit_transform(coords)

kmeans = KMeans(n_clusters=5, random_state=42, n_init='auto')
df.loc[coords.index, 'business_cluster'] = kmeans.fit_predict(coords_scaled)
```

주의:

- `latitude`, `longitude` 결측치가 있는 행은 클러스터링에서 제외한다.
- `n_clusters=5`는 시작점으로 사용하고, 필요하면 도시별 데이터 분포를 보고 조정한다.

### 8. 최종 점검

피처 생성 후 결측치, 데이터 타입, 컬럼 수를 확인한다.

확인 항목:

```python
df.shape
df.columns
df.isnull().sum().sort_values(ascending=False).head(20)
df.dtypes
```

타겟 컬럼 `is_positive`가 변경되지 않았는지 확인한다.

```python
df['is_positive'].value_counts()
```

### 9. 피처 추가 파일 저장

원본 샘플 CSV는 유지하고, 피처가 추가된 파일은 별도 이름으로 저장한다.

저장 파일명 예시:

```text
yelp_subset_philly_15k_features.csv
yelp_subset_tucson_15k_features.csv
yelp_subset_new_orleans_15k_features.csv
```

예시 코드:

```python
df.to_csv('yelp_subset_philly_15k_features.csv', index=False)
```

## 권장 작업 우선순위

1. 텍스트 기반 변수
2. 날짜 기반 변수
3. 유저 기준 변수
4. 식당 기준 변수
5. 위치 정보 병합
6. K-Means 상권 클러스터링
7. 최종 점검 및 저장

## 최종 산출물

- 피처 엔지니어링 노트북 또는 Python 스크립트
- 도시별 피처 추가 CSV 파일
- 생성한 파생변수 목록
- 결측치 및 데이터 크기 점검 결과

## 다음 단계 연결

2단계 산출물은 3단계 RoBERTa 텍스트 임베딩의 입력 데이터로 사용된다. RoBERTa 임베딩은 `text` 컬럼을 기반으로 만들고, 2단계에서 생성한 수치형 피처들과 나중에 결합한다.
