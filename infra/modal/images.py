# infra/modal/images.py
from modal import Image

api_image = (
    Image.debian_slim(python_version="3.11")
    .add_local_dir(  # <-- mount your local src/ tree verbatim
        "src",  # host‐side path (relative from infra/modal/)
        remote_path="/root/src",  # container path
        copy=True,  # bake into the image layer so imports see it
    )
    # mount your scripts (so your PEM ends up at /root/scripts/clerk_rsa_public.pem)
    .add_local_dir(
        "scripts",  # host-side path, from infra/modal → up two levels → scripts/
        remote_path="/root/scripts",
        copy=True,
    )
    .pip_install(
        # core framework
        "fastapi==0.115.0",
        "pydantic==2.11.7",
        # MongoDB driver
        "motor==3.4.0",
        "pymongo==4.5.0",
        # .env support
        "python-dotenv==1.0.1",
        # JWT verification
        "python-jose==3.5.0",
        "requests==2.32.3",
        # logging
        "logfire==3.7.1",
        # tracing / instrumentation
        "opentelemetry-instrumentation-fastapi==0.51b0",
        # retry logic
        "tenacity==9.0.0",
        # timezones
        "pytz==2024.1",
        # modal SDK
        "modal==1.0.5",
        # Email Validator
        "email_validator==2.2.0",
        # AI
        "openai==0.28.0",
    )
)
