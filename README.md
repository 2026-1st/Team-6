# Team-6 머신러닝 프로젝트

Yelp 레스토랑 리뷰를 이용해 Philadelphia, Tucson, New Orleans의 불만족 리뷰를 예측하고 모델이 활용한 주요 패턴을 분석한다.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/2026-1st/Team-6/blob/main/notebooks/00_full_pipeline/Team6_Full_Pipeline.ipynb)

## 가장 빠른 실행 방법

별도의 데이터 준비 없이 Google Colab에서 전체 결과를 확인할 수 있다.

1. 위의 **Open In Colab** 버튼을 누른다.
2. 필요하면 `런타임 > 런타임 유형 변경`에서 T4 GPU를 선택한다.
3. 첫 설정 셀의 아래 옵션을 기본값으로 둔다.

```python
RUN_RAW_PIPELINE = False
RUN_EMBEDDING = False
```

4. `런타임 > 모두 실행`을 선택한다.
5. EDA, 피처 엔지니어링, 모델 평가, ROC, SHAP, 오류 분석 결과를 셀 출력에서 확인한다.

기본 실행은 저장소에 포함된 CSV를 사용하므로 Kaggle 토큰이나 Google Drive가 필요하지 않다. 분석 결과는 파일로 저장하지 않고 Colab 화면과 런타임 메모리에만 표시한다.

## 실행 환경

권장 환경은 다음과 같다.

| 항목 | 권장 설정 |
| --- | --- |
| 실행 환경 | Google Colab 또는 Linux |
| Python | 3.11 이상 |
| 메모리 | Colab 기본 RAM 이상 |
| GPU | 기본 실행에서는 선택 사항, 임베딩 재생성 시 필수 권장 |
| 인터넷 | 저장소 clone, 패키지 및 모델 다운로드에 필요 |
| 기본 노트북 | `notebooks/00_full_pipeline/Team6_Full_Pipeline.ipynb` |

Colab 첫 셀은 저장소를 `/content/Team-6`에 clone하고 Colab 기본 이미지에 없는 핵심 패키지를 설치한다.

## 라이브러리 버전

로컬 실행 기준 최소 버전은 `requirements.txt`와 같다.

| 용도 | 라이브러리 | 버전 |
| --- | --- | --- |
| 노트북 | `ipykernel` | `>=7.0` |
| 노트북 | `jupyter` | `>=1.1` |
| 데이터 처리 | `numpy` | `>=2.0` |
| 데이터 처리 | `pandas` | `>=2.2` |
| 머신러닝 | `scikit-learn` | `>=1.5` |
| 시각화 | `matplotlib` | `>=3.9` |
| 시각화 | `seaborn` | `>=0.13` |
| 시각화 | `wordcloud` | `>=1.9` |
| 지도 | `folium` | `>=0.17` |
| 임베딩 | `transformers` | `>=4.45` |
| 임베딩 | `torch` | `>=2.5` |
| 임베딩 | `tqdm` | `>=4.66` |
| 모델링 | `catboost` | `>=1.2` |
| 해석 | `shap` | `>=0.46` |
| 원본 다운로드 | `kaggle` | `>=1.6` |

Colab에서는 호환성 변화를 줄이기 위해 노트북이 `catboost<2`, `shap<1`, `wordcloud<2`, `kaggle<2` 범위로 설치한다.

## 기본 실행 절차

통합 노트북은 위에서부터 다음 순서로 실행된다.

### 1. 환경 준비

- GitHub 저장소를 Colab 런타임에 clone한다.
- 필요한 패키지와 한글 글꼴을 설치한다.
- 입력 데이터 경로와 실행 옵션을 설정한다.

### 2. EDA

- 도시별 긍정·부정 리뷰 분포를 확인한다.
- 리뷰 길이 분포와 워드클라우드를 비교한다.
- 지도에서 리뷰가 집중된 식당 및 상권을 확인한다.

### 3. 피처 엔지니어링

- 텍스트 길이, 단어 수, 문장 수를 생성한다.
- 날짜, 사용자, 식당 통계 피처를 생성한다.
- 위도·경도와 K-Means 상권 클러스터를 추가한다.
- 결과는 `feature_datasets`에 보관한다.

### 4. 임베딩과 PCA

기본 실행에서는 저장소의 32차원 PCA CSV를 사용한다. 따라서 `distilroberta-base` 임베딩을 다시 계산하지 않는다.

### 5. 모델링과 해석

- 저장소에 포함된 가공 CSV와 PCA CSV를 모델 입력으로 사용한다.
- Logistic Regression, CatBoost, PyTorch MLP를 학습한다.
- Accuracy, F1, ROC-AUC와 혼동행렬을 확인한다.
- 도시별 ROC 곡선을 비교한다.
- CatBoost SHAP 요약 및 의존성 그래프를 확인한다.
- 불만족 리뷰의 예측 성공·실패 집단을 비교한다.
- PCA 축의 높은 값과 낮은 값에 대응하는 리뷰 표현을 살펴본다.

## 정상 실행 확인

전체 실행이 완료되면 노트북에서 다음 결과를 확인할 수 있다.

| 단계 | 확인할 출력 |
| --- | --- |
| 환경 설정 | 실행 환경, 프로젝트 루트, 두 실행 옵션 |
| EDA | 도시별 요약표, 만족도 분포, 텍스트 길이, 워드클라우드 |
| 위치 분석 | 도시별 리뷰 위치 집계와 인터랙티브 히트맵 |
| 피처 엔지니어링 | 도시별 데이터 크기와 결측치 요약 |
| 데이터 분할 | 도시마다 학습 12,000건, 평가 3,000건 |
| 모델 평가 | 세 모델의 Accuracy, F1, ROC-AUC, 혼동행렬 |
| 모델 해석 | ROC, SHAP 요약, SHAP 의존성, 오류 분석 |
| PCA 해석 | PCA 값 상·하위 리뷰와 주요 단어 |

세 도시의 가공 CSV와 PCA CSV는 각각 15,000행이어야 한다. 행 수가 다르거나 PCA 32개 컬럼이 없으면 노트북이 오류를 발생시킨다.

## 선택 실행

### Yelp 원본부터 다시 샘플링

첫 설정 셀에서 다음 값을 사용한다.

```python
RUN_RAW_PIPELINE = True
RUN_EMBEDDING = False
```

이 경우 Kaggle에서 발급한 `kaggle.json` 업로드가 필요하다. Yelp 원본 압축 파일은 크기가 크므로 Colab 디스크 공간과 실행 시간을 확인해야 한다.

### RoBERTa 임베딩과 PCA 다시 계산

Colab GPU 런타임을 선택하고 다음 값을 사용한다.

```python
RUN_RAW_PIPELINE = False
RUN_EMBEDDING = True
```

세 도시 45,000개 리뷰를 다시 임베딩하므로 기본 실행보다 오래 걸린다. 생성 결과는 `pca_datasets`에만 보관하며 파일로 저장하지 않는다.

두 옵션을 모두 `True`로 설정하면 원본 다운로드부터 임베딩까지 전체 계산을 수행한다.

## 로컬 실행

저장소 루트에서 다음 명령을 실행한다.

```bash
git clone https://github.com/2026-1st/Team-6.git
cd Team-6

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m ipykernel install --user --name team6 --display-name "Team-6"
jupyter lab
```

Jupyter에서 `Team-6` 커널을 선택한 뒤 통합 노트북을 위에서부터 실행한다. 로컬에 NanumGothic이 없으면 한글 글꼴 경고가 나올 수 있지만 분석 계산에는 영향을 주지 않는다.

## 주요 데이터

저장소에는 기본 실행에 필요한 데이터가 포함되어 있다.

```text
data/interim/
  yelp_subset_philly_15k.csv
  yelp_subset_tucson_15k.csv
  yelp_subset_new_orleans_15k.csv
  business_location.csv

data/processed/
  yelp_subset_philly_15k_features.csv
  yelp_subset_tucson_15k_features.csv
  yelp_subset_new_orleans_15k_features.csv

data/embeddings/
  philly_pca_32.csv
  tucson_pca_32.csv
  new_orleans_pca_32.csv
```

파일별 행과 컬럼 정보는 `data/DATA_CATALOG.md`에서 확인할 수 있다. Yelp 원본 JSON과 768차원 원본 임베딩은 용량이 커서 GitHub에 포함하지 않는다.

## 프로젝트 구조

```text
Team-6/
  data/                         # 입력 CSV와 단계별 데이터
  notebooks/
    00_full_pipeline/           # Colab 전체 실행용 노트북
    01_eda_sampling/            # EDA 및 샘플링
    02_feature_engineering/     # 피처 엔지니어링
    03_text_embedding/          # RoBERTa와 PCA
    04_modeling_analysis/       # 모델링과 SHAP 분석
  docs/                         # 작업 계획과 기록
  output/                       # 기존에 생성한 참고 결과물
  requirements.txt              # 로컬 환경 의존성
```

## 라이선스 및 외부 자산

### 프로젝트 코드

팀이 작성한 프로젝트 코드는 저장소 루트의 `LICENSE`에 명시된 MIT License를 따른다. MIT License는 코드의 사용, 복제, 수정, 병합, 게시, 배포, 재라이선스, 판매를 허용하되, 저작권 고지와 라이선스 고지를 함께 유지할 것을 요구한다.

단, 이 라이선스는 팀이 작성한 코드와 문서에 적용된다. Yelp 데이터, 외부 모델, 외부 라이브러리는 각자의 이용 조건과 라이선스를 따른다.

### Yelp Open Dataset

이 프로젝트의 리뷰와 사업장 정보는 [Yelp Open Dataset](https://business.yelp.com/data/resources/open-dataset/)을 기반으로 한다. Yelp는 해당 데이터셋을 교육 목적으로 제공하며, 데이터 사용과 배포에는 Yelp가 제공하는 이용 조건이 적용된다.

- Yelp 원본 데이터와 이를 기반으로 만든 CSV는 프로젝트 코드 라이선스의 적용 대상이 아니다.
- 데이터는 수업, 연구 및 교육 목적 범위에서 사용한다.
- Yelp 데이터에 대한 소유권을 주장하거나 별도의 오픈 데이터 라이선스로 재허가하지 않는다.
- 프로젝트를 복제하거나 외부에 배포하기 전에 Yelp Open Dataset에 포함된 최신 이용 조건을 확인해야 한다.
- Yelp 원본 JSON은 용량과 이용 조건을 고려해 저장소에 포함하지 않는다.

저장소의 도시별 샘플 및 파생 CSV에는 리뷰 원문이 들어 있다. 저장소를 공개하거나 다른 목적으로 배포할 때는 Yelp의 데이터 재배포 조건을 우선 확인해야 한다.

### DistilRoBERTa

텍스트 임베딩에는 Hugging Face의 [`distilbert/distilroberta-base`](https://huggingface.co/distilbert/distilroberta-base)를 사용한다. 이 모델은 [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)으로 제공된다.

모델 자체의 저작권과 라이선스는 원 저작자에게 있으며 프로젝트 코드 라이선스와 별도로 적용된다. 모델을 수정하거나 가중치와 함께 재배포할 경우 Apache License 2.0의 저작권 고지와 라이선스 조건을 유지해야 한다.

### 외부 라이브러리

`requirements.txt`에 명시된 Python 라이브러리는 각각의 라이선스를 따른다. 이 프로젝트는 해당 라이브러리를 의존성으로 설치해 사용하며, 각 라이브러리의 저작권이나 라이선스를 대체하지 않는다.

이 절은 출처와 일반적인 이용 조건을 정리한 것이며 법률 자문이 아니다. 최종 공개 또는 상업적 이용 전에는 각 데이터와 소프트웨어의 최신 라이선스 원문을 확인해야 한다.
