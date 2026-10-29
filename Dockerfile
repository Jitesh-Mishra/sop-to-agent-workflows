FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY sopflow ./sopflow
COPY data ./data
ENV SOPFLOW_DB_DIR=/data/runs
EXPOSE 8000
# REST API by default; for the MCP server over stdio: docker run -i <image> python -m sopflow.mcp_server
CMD ["uvicorn", "sopflow.api:app", "--host", "0.0.0.0", "--port", "8000"]
