# Team-6 머신러닝 프로젝트

Yelp 레스토랑 리뷰 데이터를 활용해 도시별 리뷰 감성을 예측하고, 불만족 리뷰의 주요 요인을 분석하는 머신러닝 프로젝트입니다.

## 프로젝트 구조

```text
Team-6/
  data/
    raw/          # 원본 Yelp JSON 보관 위치. 대용량 원본 파일은 GitHub에 올리지 않습니다.
    interim/      # 도시별 샘플 CSV, business_location.csv 등 중간 데이터.
    processed/    # 피처 엔지니어링이 끝난 최종 정형 CSV.
    embeddings/   # RoBERTa 임베딩 및 PCA 결과. 대용량 .npy 파일은 GitHub에서 제외합니다.

  notebooks/
    00_full_pipeline/         # 전체 과정을 한 파일로 합친 검토용 노트북.
    01_eda_sampling/          # 1단계: EDA 및 도시별 샘플링.
    02_feature_engineering/   # 2단계: 위치 정보 추출 및 피처 엔지니어링.
    03_text_embedding/        # 3단계: RoBERTa 임베딩 추출 및 PCA 차원 축소.
    04_modeling_analysis/     # 4단계: 모델링, 평가, SHAP 및 오류 분석.

  output/
    figures/      # EDA 및 분석 그래프.
    maps/         # 리뷰 빈도 기반 인터랙티브 지도.
    tables/       # 요약표, 데이터 인벤토리 등 CSV 산출물.
    reports/      # 최종 보고서 또는 발표용 자료 보관 위치.

  docs/           # 작업 계획과 과정 기록.
  scripts/        # 산출물 재생성 등 보조 스크립트.
```

## 분석 파이프라인

1. **EDA 및 샘플링**
   - Yelp 원본 JSON에서 Philadelphia, Tucson, New Orleans의 레스토랑 리뷰를 추출합니다.
   - 3점 중립 리뷰를 제거하고, 긍정/부정 라벨을 생성합니다.
   - 도시별 샘플 CSV를 `data/interim/`에 저장합니다.

2. **피처 엔지니어링**
   - 리뷰 텍스트 길이, 단어 수, 문장 수, 느낌표/물음표 수 등 텍스트 기반 피처를 생성합니다.
   - 날짜, 사용자, 비즈니스 통계 기반 파생변수를 추가합니다.
   - 위치 정보가 있으면 위도/경도와 상권 클러스터 피처를 추가합니다.
   - 최종 피처 CSV를 `data/processed/`에 저장합니다.

3. **RoBERTa 임베딩 및 PCA**
   - 리뷰 텍스트를 `distilroberta-base` 임베딩으로 변환합니다.
   - 768차원 임베딩을 PCA로 32차원까지 축소합니다.
   - PCA 결과 CSV는 `data/embeddings/`에 저장합니다.

4. **모델링 및 분석**
   - 로지스틱 회귀, CatBoost, PyTorch MLP 모델을 학습합니다.
   - F1 점수, ROC-AUC, 혼동 행렬로 모델을 비교합니다.
   - CatBoost SHAP 분석과 오류 분석을 통해 불만족 리뷰의 주요 요인을 해석합니다.
   - 그래프와 표는 `output/`에 저장합니다.

## 노트북 실행 순서

전체 흐름을 한 번에 검토하려면 아래 통합 노트북을 확인합니다.

```text
notebooks/00_full_pipeline/Team6_Full_Pipeline.ipynb
```

단계별로 실행하거나 수정할 때는 아래 순서를 권장합니다.

```text
1. notebooks/01_eda_sampling/ML_Sampling_EDA.ipynb
2. notebooks/02_feature_engineering/Create_Business_Location_CSV.ipynb
3. notebooks/02_feature_engineering/Feature_Engineering.ipynb
4. notebooks/03_text_embedding/RoBERTa_PCA.ipynb
5. notebooks/04_modeling_analysis/Modeling.ipynb
```

## 실행 환경 준비

로컬에서 실행할 경우 프로젝트 루트에서 가상환경을 만든 뒤 필요한 라이브러리를 설치합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

VS Code에서 노트북을 실행할 때는 `.venv/bin/python` 또는 `Team-6 (.venv)` 커널을 선택합니다.

## 주요 데이터 파일

`data/interim/`

```text
yelp_subset_philly_15k.csv
yelp_subset_tucson_15k.csv
yelp_subset_new_orleans_15k.csv
business_location.csv
```

`data/processed/`

```text
yelp_subset_philly_15k_features.csv
yelp_subset_tucson_15k_features.csv
yelp_subset_new_orleans_15k_features.csv
```

`data/embeddings/`

```text
philly_pca_32.csv
tucson_pca_32.csv
new_orleans_pca_32.csv
```

파일별 행 수와 컬럼 수는 `data/DATA_CATALOG.md`에서 확인할 수 있습니다.

## 산출물

현재 생성된 산출물은 `output/`에 정리되어 있습니다.

```text
output/figures/   # 도시별 타깃 분포, 주요 단어 그래프 등
output/maps/      # 도시별 리뷰 빈도 히트맵 HTML
output/tables/    # EDA 요약표, 데이터 인벤토리
output/reports/   # 최종 보고서 보관 위치
```

만일 산출물을 다시 생성하고 싶다면 다음 명령을 실행하면 됩니다.

```bash
python scripts/generate_output_artifacts.py
```

## GitHub 업로드 기준

GitHub에는 다음 파일을 포함했습니다

- 노트북: `notebooks/`
- 요약 문서: `README.md`, `docs/`, `data/DATA_CATALOG.md`
- 재사용 가능한 CSV: `data/interim/`, `data/processed/`, `data/embeddings/*_pca_32.csv`
- 가벼운 결과물: `output/figures/`, `output/tables/`

다음 파일은 대용량이므로 GitHub에 올리지 않았습니다

- Yelp 원본 JSON
- RoBERTa 원본 임베딩 `.npy`
- 학습된 모델 체크포인트 `.pt`, `.pth`, `.ckpt`
