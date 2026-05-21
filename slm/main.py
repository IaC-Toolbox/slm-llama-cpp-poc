from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


# @asynccontextmanager
# async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
#     global llm
#     llm = Llama(
#         model_path=os.environ["MODEL_PATH"],
#         n_ctx=2048,
#         n_threads=8,
#     )
#     yield

# The service name is the label that scopes all your alerts and dashboards.
# Must match OTEL_SERVICE_NAME if you set it via environment variable.
resource = Resource(attributes={"service.name": "my-api"})

exporter = OTLPMetricExporter(
    endpoint="http://localhost:4317",  # replace with your Alloy host
    insecure=True,
)

reader = PeriodicExportingMetricReader(exporter, export_interval_millis=15_000)
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)


app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

health_router = APIRouter()


@health_router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(health_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
