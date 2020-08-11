import json


class Expenses:
    def __init__(self):
        try:
            with open("expenses.json", "r") as f:
                self.expenses = json.load(f)
        except FileNotFoundError:
            self.expenses = [
                {
                    "id": 1,
                    "title": "Czynsz",
                    "description": "bez dodatkowych opłat",
                    "koszt": 200
                },
                {
                    "id": 2,
                    "title": "Media",
                    "description": "Gaz, energia, woda, internet, telefon",
                    "koszt": 400
                }
            ]

    def all(self):
        return self.expenses

    def get(self, id):
        expense = [expense for expense in self.all() if expense['id'] == id]
        if expense:
            return expense[0]
        return []

    def create(self, data):
        new_id = 1
        while (self.get(new_id) != []):
            new_id += 1
        print("data", data)
        data['id'] = new_id
        self.expenses.append(data)
        self.save_all()

    def save_all(self):
        with open("expenses.json", "w") as f:
            json.dump(self.expenses, f)

    def update(self, id, data):
        expense = self.get(id)
        if expense:
            index = self.expenses.index(expense)
            self.expenses[index] = data
            self.save_all()
            return True
        return False

    def delete(self, id):
        expense = self.get(id)
        if expense:
            self.expenses.remove(expense)
            self.save_all()
            return True
        return False


expenses = Expenses()
