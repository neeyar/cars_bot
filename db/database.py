from sqlalchemy import (
    create_engine, 
    MetaData, 
    Table, 
    Column,
    String,
    Text,
    Integer, 
    select
)

from config import MYSQL_URL

engine = create_engine(MYSQL_URL)
meta = MetaData()

class CarManager():

    def __init__(self, engine) -> None:
        self.engine = engine
        self.car = self.get_table_schema()

    def get_table_schema(self):
        car = Table(
            "cars", meta,
            Column("id",Integer, primary_key=True),
            Column("title", String(200)),
            Column("som", Integer),
            Column("dollar", Integer),
            Column("mobile", String(50)),
            Column("description", Text),
            Column("link", String(255), nullable=False, unique=True)
        )
        return car
    
    def create_table(self):
        meta.create_all(self.engine, checkfirst=True)
        print("Таблица успешно создано")


    def insert_car(self, data):
        ins = self.car.insert().values(
           **data
        )
        connect = self.engine.connect()
        result = connect.execute(ins)
        connect.commit()
    
    def check_car_url(self, url):
        sel = select(self.car).where(self.car.c.link==url)
        connect = self.engine.connect()
        result = connect.execute(sel)
        result = result.fetchone()
        return result is not None
    
    def search_by_name(self, name):
        query = select(self.car).where(self.car.c.title.like(f"%{name}%"))
        connect = self.engine.connect()
        result = connect.execute(query)
        cars = result.fetchall()
        return cars

    def search_by_price(self, start, end):
        query = select(self.car).where(self.car.c.dollar.between(start,end))
        connect = self.engine.connect()
        result = connect.execute(query)
        cars = result.fetchall()
        return cars

manager = CarManager(engine=engine)