import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter  # changed: grpc -> http
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from phoenix.otel import register
from slm.routes.routes import create_router

import logging


tracer_provider = register(
  project_name="default",
  auto_instrument=True,
  endpoint=os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:4318/v1/traces")
)

logging.basicConfig(level=logging.DEBUG)

# Silence noisy libraries, keep OTel visible
logging.getLogger("opentelemetry").setLevel(logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.DEBUG)  # shows actual HTTP calls

resource = Resource(attributes={"service.name": "slm-llama-cpp-poc-service"})

exporter = OTLPMetricExporter(
    endpoint=f"http://{os.getenv('ALLOY_HOST')}:4318/v1/metrics",  # changed: 4317 -> 4318, added /v1/metrics, removed insecure=True
)

reader = PeriodicExportingMetricReader(exporter, export_interval_millis=15_000)
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)

app = FastAPI()

FastAPIInstrumentor.instrument_app(app)

app.include_router(create_router())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)