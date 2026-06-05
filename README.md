<div align="center">

# 🐳 Workflow-CI — MLflow CI/CD & Docker Pipeline

### HR Attrition Model • Automated Build & Deploy

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-2.19.0-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Hub-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12.7-3776AB?style=for-the-badge&logo=python&logoColor=white)

---

Repositori ini berisi **CI/CD pipeline otomatis** yang melatih model Machine Learning, mem-package-nya ke dalam Docker image menggunakan MLflow, lalu mem-push image tersebut ke Docker Hub — **sepenuhnya otomatis** setiap kali ada push ke branch `main`.

[🐳 Docker Hub Image](https://hub.docker.com/r/akramdwf/hr-attrition-model) · [📊 Repo Utama](https://github.com/Akram-Dwf/Eksperimen_SML_Akram-Alfadli-Tamir)

</div>

---

## 📑 Daftar Isi

- [Alur Pipeline](#-alur-pipeline)
- [Struktur Repositori](#-struktur-repositori)
- [MLflow Project](#-mlflow-project)
- [CI/CD Pipeline](#-cicd-pipeline)
- [GitHub Secrets](#-github-secrets)
- [Docker Hub](#-docker-hub)
- [Cara Menjalankan Lokal](#-cara-menjalankan-lokal)
- [Bagian dari Proyek Utama](#-bagian-dari-proyek-utama)

---

## 🔄 Alur Pipeline

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│  Push ke     │────►│  GitHub      │────►│  MLflow Project  │
│  branch main │     │  Actions     │     │  (mlflow run .)  │
└──────────────┘     └──────────────┘     └────────┬─────────┘
                                                   │
                                                   ▼
                                          ┌──────────────────┐
                                          │  Training Model  │
                                          │  RandomForest    │
                                          │  + log to mlruns │
                                          └────────┬─────────┘
                                                   │
                                                   ▼
                                          ┌──────────────────┐
                                          │  Extract Run ID  │
                                          │  dari mlruns/0   │
                                          └────────┬─────────┘
                                                   │
                              ┌────────────────────┼────────────────────┐
                              ▼                    ▼                    ▼
                     ┌────────────────┐  ┌─────────────────┐  ┌──────────────┐
                     │ Upload mlruns  │  │ Build Docker    │  │ Push to      │
                     │ as Artifact    │  │ Image (MLflow)  │  │ Docker Hub   │
                     └────────────────┘  └─────────────────┘  └──────────────┘
```

---

## 📂 Struktur Repositori

```
Workflow-CI/
│
├── 📁 MLProject/                    # MLflow Project Directory
│   ├── MLProject                    # Konfigurasi entry point MLflow
│   ├── conda.yaml                   # Environment dependencies
│   ├── modelling.py                 # Training script (self-contained)
│   └── Tautan_Docker_Hub.txt        # Link ke Docker Hub image
│
├── 📁 .github/workflows/
│   └── ci.yml                       # GitHub Actions CI/CD pipeline
│
└── README.md                        # Dokumentasi ini
```

---

## 📦 MLflow Project

Proyek ini dikemas sebagai **MLflow Project** standar sehingga bisa dijalankan secara reproducible di environment manapun.

### `MLProject`

```yaml
name: hr_attrition_ci
conda_env: conda.yaml
entry_points:
  main:
    command: "python modelling.py"
```

### `conda.yaml`

```yaml
name: hr_attrition_env
channels:
  - conda-forge
dependencies:
  - python=3.12.7
  - pip
  - pip:
      - mlflow==2.19.0
      - scikit-learn
```

### `modelling.py`

Script training yang **self-contained** (tidak memerlukan file data eksternal):

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from mlflow.sklearn import log_model

# Generate dummy data secara mandiri
X, y = make_classification(n_samples=100, n_features=20, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Log model ke MLflow
log_model(model, "model")
```

> **Catatan**: Script menggunakan `make_classification()` untuk generate data secara mandiri agar pipeline CI/CD bisa berjalan tanpa bergantung pada file CSV eksternal.

---

## ⚙️ CI/CD Pipeline

Pipeline GitHub Actions (`ci.yml`) terdiri dari **9 tahap** yang berjalan otomatis:

| Step | Aksi | Detail |
|:---:|---|---|
| 1 | **Checkout** | Clone repository ke runner |
| 2 | **Setup Python** | Install Python 3.12.7 |
| 3 | **Check Env** | Verifikasi versi Python & pip |
| 4 | **Install Deps** | `pip install mlflow==2.19.0 scikit-learn` |
| 5 | **Run MLflow Project** | `mlflow run . --env-manager=local` |
| 6 | **Extract Run ID** | Ambil Run ID dari direktori `mlruns/` |
| 7 | **Upload Artifacts** | Simpan `mlruns/` sebagai GitHub Artifact |
| 8 | **Build Docker** | `mlflow models build-docker` → image lokal |
| 9 | **Push to Docker Hub** | Login, tag, & push image |

### Trigger

```yaml
on:
  push:
    branches:
      - main
```

Pipeline berjalan **otomatis** setiap kali ada push ke branch `main`.

---

## 🔑 GitHub Secrets

Untuk menjalankan pipeline secara penuh, Anda harus mengkonfigurasi **2 secrets** di repository GitHub:

| Secret | Deskripsi | Cara Setting |
|---|---|---|
| `DOCKER_USERNAME` | Username Docker Hub Anda | Settings → Secrets → Actions → New |
| `DOCKER_PASSWORD` | Password / Access Token Docker Hub | Settings → Secrets → Actions → New |

**Langkah konfigurasi:**
1. Buka repository di GitHub
2. Klik **Settings** → **Secrets and variables** → **Actions**
3. Klik **New repository secret**
4. Tambahkan kedua secret di atas

---

## 🐳 Docker Hub

Setelah pipeline berhasil berjalan, Docker image akan tersedia di:

```
akramdwf/hr-attrition-model:latest
```

🔗 **Link**: [https://hub.docker.com/r/akramdwf/hr-attrition-model](https://hub.docker.com/r/akramdwf/hr-attrition-model)

### Pull & Run Image

```bash
# Pull image dari Docker Hub
docker pull akramdwf/hr-attrition-model:latest

# Jalankan container
docker run -p 5001:8080 akramdwf/hr-attrition-model:latest
```

---

## 💻 Cara Menjalankan Lokal

Jika ingin menjalankan MLflow Project secara lokal tanpa Docker:

```bash
# Clone repository
git clone https://github.com/Akram-Dwf/Workflow-CI.git
cd Workflow-CI

# Install dependencies
pip install mlflow==2.19.0 scikit-learn

# Jalankan MLflow Project
mlflow run . --env-manager=local

# Lihat hasil di MLflow UI
mlflow ui
# Buka http://localhost:5000
```

---

## 🔗 Bagian dari Proyek Utama

Repositori ini merupakan bagian dari proyek **End-to-End MLOps System** untuk tugas akhir **Membangun Sistem Machine Learning (MSML)**:

| Repositori | Kriteria | Deskripsi |
|---|---|---|
| [**Eksperimen_SML**](https://github.com/Akram-Dwf/Eksperimen_SML_Akram-Alfadli-Tamir) | 1, 2 | Preprocessing, EDA, Modelling, MLflow Tracking |
| **Workflow-CI** ← *Anda di sini* | 3 | CI/CD Pipeline, Docker Containerization |
| Monitoring dan Logging | 4 | FastAPI Serving, Prometheus, Grafana |

---

<div align="center">

**Dibuat oleh Akram Alfadli Tamir**

*Automated ML Pipeline — From Training to Docker Hub*

</div>
