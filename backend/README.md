# Bug Prediction Backend

## Setup

```bash
pip install -r requirements.txt
```

## Run API Server

```bash
cd src
python api.py
```

API will be available at `http://localhost:8000`

## Train Model (Optional)

```bash
cd src
python trainer.py
```

## API Endpoints

- `GET /` - Health check
- `POST /predict` - Predict bug risk for repository
