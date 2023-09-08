from peewee import SqliteDatabase, Model, CharField, BooleanField, TextField, IntegerField


database = SqliteDatabase('tasks-database.db')


class Task(Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=32, unique=True)
    is_completed = BooleanField(default=False)
    desc = TextField(null=True)

    class Meta:
        database = database

    def __str__(self):
        return self.name

    @classmethod
    def last_id(cls):
        return cls.select().order_by(Task.id.desc())[0].id

    @classmethod
    def latest_uncompleted_task(cls):
        return cls.select().where(cls.is_completed == False).order_by(Task.id.desc())[0]

    @classmethod
    def latest_completed_task(cls):
        return cls.select().where(cls.is_completed == True).order_by(Task.id.desc())[0]

    @classmethod
    def earliest_uncompleted_task(cls):
        return cls.select().where(cls.is_completed == False).order_by(Task.id.asc())[0]

    @classmethod
    def earliest_completed_task(cls):
        return cls.select().where(cls.is_completed == True).order_by(Task.id.asc())[0]

    @classmethod
    def add_task(cls, name, desc=None):
        id = Task.last_id() + 1
        return cls.create(name=name, desc=desc, is_completed=False, id=id)

    @classmethod
    def complete_task(cls, id):
        try:
            task = cls.get(id=id)
        except Exception as e:
            print(f"Task with ID {id} is not available")
            return None

        task.is_completed = True
        task.save()
        return task
