# 데이터 폴더 안내

이 폴더는 프로젝트에서 사용하는 데이터와 단계별 산출물을 보관하는 공간입니다.

## 폴더 구조

- `raw/`: 원본 데이터 보관 폴더입니다. Yelp 원본 JSON처럼 큰 파일은 GitHub에 올리지 않습니다.
- `interim/`: 중간 산출물 보관 폴더입니다. 샘플링이 끝난 CSV와 공통으로 쓰는 작은 조회용 파일을 둡니다.
- `processed/`: 피처 엔지니어링이 끝난 최종 정형 데이터 보관 폴더입니다.
- `embeddings/`: RoBERTa 임베딩 `.npy`와 PCA CSV 등 텍스트 벡터 산출물을 보관하는 폴더입니다.

## 현재 공유 데이터

현재 CSV 파일별 행/컬럼 수는 `DATA_CATALOG.md`에서 확인할 수 있습니다.

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

`embeddings/`에는 모델링 입력으로 쓰는 PCA CSV를 둡니다.

```text
philly_pca_32.csv
tucson_pca_32.csv
new_orleans_pca_32.csv
```

원본 RoBERTa `.npy` 임베딩은 파일이 크기 때문에 로컬/Drive에는 보관하되 GitHub 커밋 대상에서는 제외합니다.

## 데이터 흐름

```text
raw
원본 Yelp JSON

↓ 샘플링

interim
도시별 샘플 CSV, business_location.csv

↓ 피처 엔지니어링

processed
파생변수가 추가된 피처 CSV

↓ RoBERTa 임베딩

embeddings
텍스트 임베딩 벡터, PCA 결과
```
