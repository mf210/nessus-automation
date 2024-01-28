FROM python:3.12

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

COPY . /app/

CMD ["pipenv", "run", "python", "export-scan-report.py"]