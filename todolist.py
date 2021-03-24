from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class Menu:
    def __init__(self):
        self.todo = Todo()
        self.menu = {"Today's tasks": self.todo.today_tasks,
                     "Week's tasks": self.todo.week_tasks,
                     "All tasks": self.todo.all_tasks,
                     "Missed tasks": self.todo.missed_tasks,
                     "Add task": self.todo.new_task,
                     "Delete task": self.todo.delete_task,
                     "Exit": exit}

    def start(self):
        while True:
            self.main_loop()

    def main_loop(self):
        raw_input = input('\n' + '\n'.join(f'{(i + 1) % len(self.menu)}) {x}' for i, x in enumerate(self.menu)))
        list(self.menu.values())[(int(raw_input) - 1)]()


class Todo:
    def __init__(self):
        engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()

    def new_task(self):
        task_input = input('Enter task\n')
        deadline_input = input('Enter deadline\n')
        date = datetime.strptime(deadline_input, '%Y-%m-%d')
        new_row = Table(task=task_input, deadline=date)
        self.session.add(new_row)
        self.session.commit()
        print('The task has been added!')

    def today_tasks(self):
        today = datetime.today().date()
        rows = self.session.query(Table).filter(Table.deadline == today).all()
        print(f'Today {today.strftime("%d %b")}:')
        if rows:
            print('\n'.join(f'{row.id}. {row}' for row in rows))
        else:
            print('Nothing to do!')

    def week_tasks(self):
        for i in range(7):
            date = datetime.today().date() + timedelta(days=i)
            rows = self.session.query(Table).filter(Table.deadline == date).order_by(Table.deadline).all()
            print(f'{date.strftime("%A %d %b")}:')
            if rows:
                print('\n'.join(f'{row.id}. {row}' for row in rows))
            else:
                print('Nothing to do!')
            print('')

    def all_tasks(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        if rows:
            print('\n'.join(f'{row.id}. {row}. {row.deadline.strftime("%d %b")}' for row in rows))
        else:
            print('Nothing to do!')

    def missed_tasks(self):
        rows = self.session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
        print('Missed tasks:')
        if rows:
            print('\n'.join(f'{row.id}. {row}. {row.deadline.strftime("%d %b")}' for row in rows))
        else:
            print('Nothing is missed!')

    def delete_task(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print('Choose the number of the task you want to delete:')
        if rows:
            print('\n'.join(f'{row.id}. {row}. {row.deadline.strftime("%d %b")}' for row in rows))
        else:
            print('Nothing to delete!')
            return
        user_input = int(input())
        self.session.query(Table).filter(Table.id == user_input).delete()
        self.session.commit()


Menu().start()
