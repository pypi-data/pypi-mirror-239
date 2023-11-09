"""FastAPI application."""
from stac_fastapi.api.app import StacApi
from stac_fastapi.api.models import create_get_request_model, create_post_request_model
from stac_fastapi.elasticsearch.config import ElasticsearchSettings
from stac_fastapi.elasticsearch.core import (
    BulkTransactionsClient,
    CoreClient,
    EsAsyncBaseFiltersClient,
    TransactionsClient,
)
from stac_fastapi.elasticsearch.database_logic import create_collection_index
from stac_fastapi.elasticsearch.extensions import QueryExtension
from stac_fastapi.elasticsearch.session import Session
from stac_fastapi.extensions.core import (
    ContextExtension,
    FieldsExtension,
    FilterExtension,
    SortExtension,
    TokenPaginationExtension,
    TransactionExtension,
)
from stac_fastapi.extensions.third_party import BulkTransactionExtension

settings = ElasticsearchSettings()
session = Session.create_from_settings(settings)

extensions = [
    TransactionExtension(client=TransactionsClient(session=session), settings=settings),
    BulkTransactionExtension(client=BulkTransactionsClient(session=session)),
    FieldsExtension(),
    QueryExtension(),
    SortExtension(),
    TokenPaginationExtension(),
    ContextExtension(),
    FilterExtension(client=EsAsyncBaseFiltersClient()),
]

post_request_model = create_post_request_model(extensions)

api = StacApi(
    settings=settings,
    extensions=extensions,
    client=CoreClient(session=session, post_request_model=post_request_model),
    search_get_request_model=create_get_request_model(extensions),
    search_post_request_model=post_request_model,
)
app = api.app


@app.on_event("startup")
async def _startup_event() -> None:
    await create_collection_index()


def run() -> None:
    """Run app from command line using uvicorn if available."""
    try:
        import uvicorn

        uvicorn.run(
            "stac_fastapi.elasticsearch.app:app",
            host=settings.app_host,
            port=settings.app_port,
            log_level="info",
            reload=settings.reload,
        )
    except ImportError:
        raise RuntimeError("Uvicorn must be installed in order to use command")


if __name__ == "__main__":
    run()


def create_handler(app):
    """Create a handler to use with AWS Lambda if mangum available."""
    try:
        from mangum import Mangum

        return Mangum(app)
    except ImportError:
        return None


handler = create_handler(app)
