# Team-6 Machine Learning Project

## Project Structure

```text
Team-6/
  data/
    raw/          # Large original files. Do not commit raw Yelp JSON files.
    interim/      # Sampled CSV files and small shared lookup tables.
    processed/    # Feature-engineered CSV files.
    embeddings/   # RoBERTa vectors and PCA outputs. Large files are ignored.

  eda_sampling/          # Step 1: EDA and sampling notebooks.
  feature_engineering/   # Step 2: Feature engineering notebooks and plans.
  text_embedding/        # Step 3: RoBERTa embedding notebooks.
  modeling/              # Step 4: Baseline ML and CatBoost notebooks.
  deep_learning/         # Step 5: PyTorch hybrid MLP notebooks.
  xai_analysis/          # Evaluation, SHAP, and business insight documents.
```

## Pipeline

1. EDA and sampling: create city-level sampled review CSV files in `data/interim/`.
2. Feature engineering: add text, date, user, business, and location-cluster features. Save outputs to `data/processed/`.
3. RoBERTa embedding: convert review text into vectors and optionally compress with PCA. Save large vector files to `data/embeddings/`.
4. Modeling: train logistic regression and CatBoost baselines with cost-sensitive learning.
5. Deep learning and XAI: train hybrid PyTorch MLP models, evaluate F1-score, and interpret results with SHAP.
