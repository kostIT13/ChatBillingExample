FROM python:3.12.7-slim

COPY requirements.txt pyproject.toml uv.lock ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.__init__:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]