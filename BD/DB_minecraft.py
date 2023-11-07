from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Создание соединения с базой данных
engine = create_engine('sqlite:///minecraft.db')
Session = sessionmaker(bind=engine)
session = Session()

# Определение модели данных
Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    score = Column(Integer)

# Создание таблицы
Base.metadata.create_all(engine)

# Вставка данных в таблицу
player1 = Player(name='Steve', score=100)
player2 = Player(name='Alex', score=200)
session.add(player1)
session.add(player2)
session.commit()

# Получение данных из таблицы
players = session.query(Player).all()
for player in players:
    print(player.name, player.score)

# Закрытие соединения с базой данных
session.close()