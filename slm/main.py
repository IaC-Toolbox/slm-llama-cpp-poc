import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
# from phoenix.otel import register

from slm.routes.routes import create_router

# tracer_provider = register(
#   project_name="default",
#   auto_instrument=True
# )

resource = Resource(attributes={"service.name": "slm-llama-cpp-poc-service"})

exporter = OTLPMetricExporter(
    endpoint=f"http://{os.getenv('ALLOY_HOST')}:4317",  # replace with your Alloy host
    insecure=True,
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
