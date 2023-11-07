import os
import time
import re
import requests
from typing import Optional, List, Dict
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.background import BackgroundTask

__version__ = '1.0.1'

CONSOLE_APP_URL = os.getenv("CONSOLE_APP_URL", "https://api.console.hectiq.ai")

def send_metrics(ressource: str,
                 path: Optional[str] = None,
                 latency: Optional[float] = None,
                 metrics: Optional[dict] = None,
                 declared_metrics: Optional[Dict[str, str]] = None):
    headers = {
    }
    body = {
        "path": path,
        "latency": latency,
    }
    if declared_metrics is not None:
        # Add declared metrics to the body
        body["metrics"] = []
        for key, value in metrics.items():
            if key in declared_metrics:
                body["metrics"].append({"type": declared_metrics[key], "name": key, "value": value})
    else:
        body["metrics"] = [{"type": "float", "name": key, "value": value} for key, value in metrics.items()]

    url = f"{CONSOLE_APP_URL}/app/ressources/{ressource}/metrics"
    res = requests.post(url, json=body, headers=headers)

def send_heartbeat(ressource: str, custom_metrics: Optional[Dict[str, str]] = None):
    headers = {
        "content-type": 'application/x-www-form-urlencoded'
    }
    body = {
    }
    url = f"{CONSOLE_APP_URL}/app/ressources/{ressource}/heartbeat"
    res = requests.post(url, headers=headers, json=body)
    if res.status_code == 200:
        print(f"✅ Heartbeat succesful with the hectiq console. Your ressource {ressource} is monitored.")
    else:
        print(f"❌ Heartbeat failed with the hectiq console. Your ressource {ressource} is not monitored.")
    return res

class HectiqConsoleFastAPIMiddleware(BaseHTTPMiddleware):
    """
    Middleware that sends metrics to the hectiq console.

    Arguments:
        ressource: The ressource name
        secret_key: The secret key of the ressource
        custom_metrics: A dict of custom metrics to send to the hectiq console. This
            dict should be of the form {"metric_name": "metric_type"}. Example: {"random-number": "float"}
            It is used a declaration to make sure that the metric is correctly sent to the hectiq console.
        include_paths: A list of routes to include in the metrics. If None, all routes are included (except the ones in exclude_paths). 
            If specified, only the routes in include_paths are included.
        exclude_paths: A list of routes to exclude from the metrics. If None, all routes are included.
            Example: exclude_paths=["/docs", "/openapi.json"]. You can also use wildcard, for example:
            exclude_paths=["/docs", r"/app/ressources/*/metrics"]
    """
    def __init__(self, app, 
                 ressource: str, 
                 custom_metrics: Optional[Dict[str, str]] = None,
                 include_paths: Optional[List] = None,
                 exclude_paths: Optional[List] = None):
        super().__init__(app)
        self._ressource = ressource
        self.include_paths = include_paths
        self.exclude_paths = exclude_paths
        self._declared_metrics = custom_metrics
        send_heartbeat(ressource=ressource, custom_metrics=custom_metrics)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        request.state.metrics = {}

        # Include paths
        if self.include_paths is not None:
            for include_path in self.include_paths:
                if include_path == path or re.match(include_path, path):
                    break
            else:
                return await call_next(request)
            
        # Exclude paths
        if self.exclude_paths is not None:
            for exclude_path in self.exclude_paths:
                if exclude_path == path or re.match(exclude_path, path):
                    return await call_next(request)
        
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.background = BackgroundTask(send_metrics, 
                                             latency=process_time, 
                                             metrics=request.state.metrics, 
                                             path=request.url.path,
                                             ressource=self._ressource,
                                             declared_metrics=self._declared_metrics)
        return response
    
def store_metrics(request: Request, key: str, value: float):
    """
    Store a metrics in the state of the request
    Should use ContextVar in future releases (remove request params).
    """
    if hasattr(request.state, "metrics"):
        request.state.metrics[key] = value