from fastapi import FastAPI
from controllers.page_controller import router as page_router

app = FastAPI()

# Register routes
app.include_router(page_router)
