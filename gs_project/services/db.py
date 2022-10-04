from sqlalchemy import Column, Date, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from services.helpers import convert_usd_to_rub

Base = declarative_base()

# Path for your DB
db = 'your path for DB'

# Create an Engine object to communicate with the DB
engine = create_engine(db)

# Creates tables in the database defined with DeclarativeBase
Base.metadata.create_all(engine)

# Create a session object from the Session factory
Session = sessionmaker(bind=engine)
session = Session()


class DataBaseSheet(Base):
    # Your table name
    __tablename__ = 'Order'

    # Fields for Database
    id = Column(Integer, nullable=False, unique=True, primary_key=True,
                autoincrement=True)
    number_order = Column(Integer, nullable=False, unique=True)
    cost_usd = Column(Integer, nullable=False)
    cost_rub = Column(Integer, nullable=False)
    delivery = Column(Date, nullable=False)

    # Override str method
    def __str__(self):
        return f"{self.number_order}"

    @staticmethod
    def delete(orders):
        """Delete rows in database"""
        for row in orders:
            session.query(DataBaseSheet).filter(DataBaseSheet.number_order == row). \
                delete(synchronize_session=False)
            session.commit()

    @staticmethod
    def update(data_order):
        """Update data in database"""
        id_number, number_order, cost_usd, delivery = data_order
        session.query(DataBaseSheet).filter(DataBaseSheet.number_order == number_order).update(
            {
                "id": id_number,
                "number_order": number_order,
                "cost_usd": cost_usd,
                "cost_rub": convert_usd_to_rub(cost_usd),
                "delivery": delivery
            },
            synchronize_session=False
        )
        session.commit()

    @staticmethod
    def is_exist(number_order):
        """Check if such row is existed in database"""
        exist = session.query(DataBaseSheet). \
                    filter_by(number_order=number_order).first() is not None

        return exist

    @staticmethod
    def is_changes(date_sheet):
        """Check if such row has any changes comparing with 'date_sheet'"""
        change = False
        id, number_order, cost_usd, delivery = date_sheet
        row = session.query(DataBaseSheet).filter_by(number_order=number_order).first()

        if  row.id != id or \
            row.cost_usd != cost_usd or \
            row.delivery != delivery:
            change = True

        return change
