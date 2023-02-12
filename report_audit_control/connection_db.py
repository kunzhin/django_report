from django.conf import settings
from sqlalchemy import create_engine
import sqlalchemy

user = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']
database_name = settings.DATABASES['default']['NAME']
host = settings.DATABASES['default']['HOST']
port = settings.DATABASES['default']['PORT']

database_url = 'mysql+mysqldb://{user}:{password}@{host}:{port}/{database_name}?charset=utf8'.format(
    user=user,
    password=password,
    database_name=database_name,
    host=host,
    port=port
)

engine = create_engine(database_url, echo=False)


# Функция формирования словаря для типов данных SQL
def sqlcol(dfparam):
    dtypedict = {}
    for i, j in zip(dfparam.columns, dfparam.dtypes):
        if "object" in str(j):
            dtypedict.update({i: sqlalchemy.types.NVARCHAR(length=255)})

        if "datetime" in str(j):
            dtypedict.update({i: sqlalchemy.types.Date()})

        if "float" in str(j):
            dtypedict.update({i: sqlalchemy.types.Float(precision=3, asdecimal=True)})

        if "int" in str(j):
            dtypedict.update({i: sqlalchemy.types.INT()})

        if "int64" in str(j):
            dtypedict.update({i: sqlalchemy.types.BIGINT()})

    return dtypedict
