## FISHAUTH

FISHAUTH is a library that allows you to manage models to create an authentication system

Installation
------------

To install, run `pip install fishauth`


Basic Usage
-----------
Usage of Alembic starts with creation of the Migration Environment. This is a directory of scripts that is specific to a particular application. The migration environment is created just once, and is then maintained along with the application’s source code itself. The environment is created using the init command of Alembic, and is then customizable to suit the specific needs of the application.

The structure of this environment, including some generated migration scripts, looks like:

```bash
yourproject/
alembic/
    env.py
    README
    script.py.mako
    versions/
        3512b954651e_migrations1.py
        2b1ae634e5cd_migrations2.py
        3adcc9a56557_migrationsN.py
```

Now in `env.py` in our alembic folder, we have to make some changes. To detect auto changes by alembic we need to give our model path to `env.py`

```python
# env.py

from fishauth.models.base import Base as BaseFish
target_metadata = [BaseFish.metadata,...,Base.metadata1,Base.metadata1,Base.metadataN ]

```

As shown above, we have to give the model base file to alembic env file. Now we are all set for our first migration.

```bash
alembic revision --autogenerate -m "First commit"
```

Using the above command alembic generate our first migration commit file in versions folder. you can see the version file now in the versions folder.

Once this file generates we are ready for database migration.
```bash
alembic upgrade head
```
