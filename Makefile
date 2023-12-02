start_dev:
	poetry run uvicorn fastapi_logging_ex.main:app --reload --port 8008 --host 0.0.0.0