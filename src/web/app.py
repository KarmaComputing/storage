from flask import Flask, render_template, request
from db import get_db, close_db
import sqlalchemy
from logger import log
import paramiko
from dotenv import load_dotenv
import os
import secrets

load_dotenv(verbose=True)

STORAGE_HOST = os.getenv("STORAGE_HOST", None)
CEPH_FILESYSTEM_NAME = os.getenv("CEPH_FILESYSTEM_NAME", None)


app = Flask(__name__)
app.teardown_appcontext(close_db)


def get_storage_credentials():
    ssh_client = paramiko.client.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(STORAGE_HOST, username="root")
    client_name = secrets.token_hex(25)
    command = f"ceph fs authorize {CEPH_FILESYSTEM_NAME} client.{client_name} /{client_name} rw"  # noqa: E501
    stdin, stdout, stderr = ssh_client.exec_command(command)
    result = stdout.read().decode("utf-8")
    return result


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        credentials = get_storage_credentials()
        return render_template("complete.html", credentials=credentials)
    return render_template("index.html")


@app.route("/health")
def health():
    log.info("Checking /health")
    db = get_db()
    health = "BAD"
    try:
        result = db.execute("SELECT NOW()")
        result = result.one()
        health = "OK"
        log.info(
            f"/health reported OK including database connection: {result}"
        )  # noqa: E501
    except sqlalchemy.exc.OperationalError as e:
        msg = f"sqlalchemy.exc.OperationalError: {e}"
        log.error(msg)
    except Exception as e:
        msg = f"Error performing healthcheck: {e}"
        log.error(msg)

    return health
