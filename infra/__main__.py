"""A Python Pulumi program"""

import pulumi
import pulumi_command as command

create_venv = command.local.Command("create-venv",
    create="cd ~/mini-digi && python3 -m venv venv",
)

install_packages = command.local.Command("install-packages",
    create="cd ~/mini-digi && ./venv/bin/pip install -r requirements.txt",
    opts=pulumi.ResourceOptions(depends_on=[create_venv]),
)

install_postgres = command.local.Command("install-postgres",
    create="sudo apt update && sudo apt install -y postgresql postgresql-contrib",
)

setup_db = command.local.Command("setup-db",
    create="""
    sudo -u postgres psql -c "CREATE DATABASE minidigi;" || true
    sudo -u postgres psql -c "CREATE USER minidigi_user WITH PASSWORD 'minidigi_pass';" || true
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE minidigi TO minidigi_user;" || true
    """,
    opts=pulumi.ResourceOptions(depends_on=[install_postgres]),
)

migrate = command.local.Command("migrate",
    create="cd ~/mini-digi && ./venv/bin/python manage.py migrate",
    opts=pulumi.ResourceOptions(depends_on=[install_packages, setup_db]),
)