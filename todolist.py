from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)


class Menu:
    def __init__(self, session):
        self.session = session

    def main_menu(self):
        print("1) Today's tasks")
        print('2) Add task')
        print('0) Exit')

        user_input = input()
        if user_input == '1':
            self.today_tasks()
        elif user_input == '2':
            self.new_task()
        elif user_input == '0':
            exit()
        else:
            self.main_menu()

    def today_tasks(self):
        rows = self.session.query(Table).all()
        print('Today:')
        if rows:
            print('\n'.join(f'{row.id}. {row}' for row in rows))
        else:
            print('Nothing to do!')
        self.main_menu()

    def new_task(self):
        user_input = input('Enter task\n')
        new_row = Table(task=user_input)
        self.session.add(new_row)
        self.session.commit()
        print('The task has been added!')
        self.main_menu()


def main():
    Session = sessionmaker(bind=engine)
    session = Session()

    Menu(session).main_menu()


if __name__ == '__main__':
    main()
