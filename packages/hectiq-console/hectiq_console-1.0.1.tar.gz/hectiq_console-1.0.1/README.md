# Hectiq console collector

A python package to track your inference API using the Hectiq Console.

**This service is for Hectiq's client only.**

## Installation

The installation is only possible from the repo for now.

```bash
pip install hectiq-console
```

## FastAPI

Below is an example how to use the middleware for FastAPI application.

```python
import time
import random
from fastapi import FastAPI, Request
from hectiq_console import HectiqConsoleFastAPIMiddleware, store_metrics

app = FastAPI(title="Demo application")
app.add_middleware(HectiqConsoleFastAPIMiddleware, 
                   ressource="hectiq-e2729",
                   custom_metrics={
                    "random-number": "float"  
                   },
                   include_paths=["/predict"])

@app.get("/")
async def root():
    return {"message": "🚨 This route is not monitored by the hectiq console."}

@app.get("/predict")
async def root(request: Request):
    # Store a random number
    store_metrics(request=request, key="random-number", value=random.random())
    return {"message": "✅ This route is monitored by the hectiq console."}
```

### Send a file

🔨 To do.

### Create an incident

🔨 To do.