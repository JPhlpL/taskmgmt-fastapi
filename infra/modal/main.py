# infra/Modal/main.py

from modal import App, asgi_app, Secret
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.local")

# your shared defaults live in src/core/defaults.py
from src.core.defaults import (
    API_STUB_NAME,
    MODAL_PRODUCTION_ENVIRONMENT,
    MODAL_DEVELOPMENT_ENVIRONMENT,
    SECRETS_NAME,
)

# import the image you just defined
from infra.modal.images import api_image

# pick the right secret‐environment
MODAL_ENVIRONMENT = os.environ.get("MODAL_ENVIRONMENT", "")
is_prod = MODAL_ENVIRONMENT == MODAL_PRODUCTION_ENVIRONMENT
secrets_env = MODAL_PRODUCTION_ENVIRONMENT if is_prod else MODAL_DEVELOPMENT_ENVIRONMENT

# declare your Modal app
app = App(name=API_STUB_NAME)


# wrap your FastAPI app under a Modal function
@app.function(
    image=api_image,
    secrets=[Secret.from_name(SECRETS_NAME, environment_name=secrets_env)],
    cloud="auto",  # or "aws", "gcp", etc.
    region="us-east",  # or your preferred region
    timeout=60 * 60,
    allow_concurrent_inputs=1000,
)
@asgi_app()
def fastapi_app():
    # import your FastAPI instance
    from src.main import web_app  # noqa: E402
    from src.core.logger import setup_logger  # noqa: E402

    logger = setup_logger()
    logger.info(
        f"FastAPI app started in region {os.environ['MODAL_REGION']} "
        f"on cloud {os.environ['MODAL_CLOUD_PROVIDER']} "
        f"with image id {os.environ['MODAL_IMAGE_ID']}"
    )
    return web_app


# local‐only entrypoint for testing
@app.local_entrypoint()
def main() -> None:
    # If you want to do any local tasks, you can call fastapi_app() here
    return None
