# 데이터 카탈로그

현재 공유 중인 CSV 파일의 위치, 행 수, 컬럼 수를 정리한 문서입니다.

| 단계 | 파일 | 행 수 | 컬럼 수 | 설명 |
| --- | --- | ---: | ---: | --- |
| 중간 데이터 | `yelp_subset_philly_15k.csv` | 15,000 | 10 | Philadelphia 리뷰 샘플 |
| 중간 데이터 | `yelp_subset_tucson_15k.csv` | 15,000 | 10 | Tucson 리뷰 샘플 |
| 중간 데이터 | `yelp_subset_new_orleans_15k.csv` | 15,000 | 10 | New Orleans 리뷰 샘플 |
| 중간 데이터 | `business_location.csv` | 조회 테이블 | 5 | `business_id`, 도시/주, 위도/경도 |
| 처리 데이터 | `yelp_subset_philly_15k_features.csv` | 15,000 | 31 | Philadelphia 피처 엔지니어링 결과 |
| 처리 데이터 | `yelp_subset_tucson_15k_features.csv` | 15,000 | 31 | Tucson 피처 엔지니어링 결과 |
| 처리 데이터 | `yelp_subset_new_orleans_15k_features.csv` | 15,000 | 31 | New Orleans 피처 엔지니어링 결과 |
| 임베딩 데이터 | `philly_pca_32.csv` | 15,000 | 32 | RoBERTa 임베딩을 PCA로 32차원 축소한 결과 |
| 임베딩 데이터 | `tucson_pca_32.csv` | 15,000 | 32 | RoBERTa 임베딩을 PCA로 32차원 축소한 결과 |
| 임베딩 데이터 | `new_orleans_pca_32.csv` | 15,000 | 32 | RoBERTa 임베딩을 PCA로 32차원 축소한 결과 |

CSV 행 수를 확인할 때는 단순 줄 수 계산보다 CSV 파서를 사용하는 것이 안전합니다. 리뷰 텍스트 안에 줄바꿈 문자가 포함될 수 있기 때문입니다.

이 파일들을 생성하거나 사용하는 노트북은 `notebooks/` 아래에 파이프라인 순서대로 정리되어 있습니다.
