# Eagle Eyes

## Development Setup

Installing Pyenv is recommended to not mess up the system Python installation.

- Install pyenv: `curl https://pyenv.run | bash`
- Install Python 3.7.2: `pyenv install 3.7.2 && pyenv global 3.7.2`
- Install virtualenv: `pip install virtualenv`
- Create virtualenv: `virtualenv venv`
- Activate virtualenv: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Run migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`

Now you're ready. Run the server with `python manage.py runserver` and visit http://localhost:8000/admin/
Make sure to `source venv/bin/activate` every time you open a new shell.
