# 데이터 폴더 안내

이 폴더는 프로젝트에서 사용하는 데이터와 단계별 산출물을 보관하는 공간입니다.

## 폴더 구조

- `raw/`: 원본 데이터 보관 폴더입니다. Yelp 원본 JSON처럼 큰 파일은 GitHub에 올리지 않습니다.
- `interim/`: 중간 산출물 보관 폴더입니다. 샘플링이 끝난 CSV와 공통으로 쓰는 작은 lookup 파일을 둡니다.
- `processed/`: 피처 엔지니어링이 끝난 최종 정형 데이터 보관 폴더입니다.
- `embeddings/`: RoBERTa 임베딩, PCA 결과 등 텍스트 벡터 산출물을 보관하는 폴더입니다.

## 현재 공유 데이터

`interim/`에는 다음 파일을 둡니다.

```text
yelp_subset_philly_15k.csv
yelp_subset_tucson_15k.csv
yelp_subset_new_orleans_15k.csv
business_location.csv
```

`processed/`에는 2단계 피처 엔지니어링 결과가 저장됩니다.

```text
yelp_subset_philly_15k_features.csv
yelp_subset_tucson_15k_features.csv
yelp_subset_new_orleans_15k_features.csv
```

## 데이터 흐름

```text
raw
원본 Yelp JSON

↓ 샘플링

interim
도시별 샘플 CSV, business_location.csv

↓ 피처 엔지니어링

processed
파생변수가 추가된 features CSV

↓ RoBERTa 임베딩

embeddings
텍스트 임베딩 벡터, PCA 결과
```
