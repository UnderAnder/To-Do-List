from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
    def __init__(self):
        self.todo = Todo()
        self.run = True

    def start(self):
        while self.run:
            self.main_menu()

    def main_menu(self):
        print("\n1) Today's tasks")
        print("2) Week's tasks")
        print('3) All tasks')
        print('4) Missed tasks')
        print('5) Add task')
        print('6) Delete task')
        print('0) Exit')

        user_input = input()
        if user_input == '1':
            self.todo.today_tasks()
        elif user_input == '2':
            self.todo.week_tasks()
        elif user_input == '3':
            self.todo.all_tasks()
        elif user_input == '4':
            self.todo.missed_tasks()
        elif user_input == '5':
            self.todo.new_task()
        elif user_input == '6':
            self.todo.delete_task()
        elif user_input == '0':
            self.run = False
        else:
            print('1 - 6 or 0 for exit')


class Todo:
    def __init__(self):
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
        today = datetime.today().date()
        rows = self.session.query(Table).filter(Table.deadline < today).order_by(Table.deadline).all()
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

if __name__ == '__main__':
    try:
        Menu().start()
    except KeyboardInterrupt:
        print('Bye!')
        exit()
