from fastapi import FastAPI

from api.chat_v2 import router as chat_router
from api.upload_v3 import router as upload_router
from fastapi import Request
print("========== MAIN_V3 STARTED ==========")


app = FastAPI(
    title="RAG Chatbot API",
    version="1.0.0"
)
@app.middleware("http")
async def log_requests(request: Request, call_next):

    print("REQUEST RECEIVED")

    try:
        response = await call_next(request)

        print("REQUEST FINISHED")

        return response

    except Exception as e:

        import traceback

        print("MIDDLEWARE EXCEPTION")

        traceback.print_exc()

        raise


# -------------------------
# ROOT ROUTE
# Railway Health Check
# -------------------------
@app.get("/")
def root():
    print("ROOT CALLED")
    return {
        "status": "healthy",
        "message": "RAG Chatbot API is running"
    }


# -------------------------
# HEALTHCHECK ROUTE
# -------------------------
@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# -------------------------
# API ROUTES
# -------------------------
app.include_router(chat_router)
app.include_router(upload_router)