import json
import requests

def countTaskCompletionFrequency(tasks):
    completed_task_dict = {}
    for record in tasks:
        # odwołanie do wartości dla klucza słownika to index[key]
        if record["completed"] == True:
            try:
                # weź wartość dla klucza "userId" i dodaj do niej 1
                completed_task_dict[record["userId"]] += 1
            except KeyError:
                # musi tu być except, bo na początek klucz "userId" nie istnieje, więc tworzymy klucz userId i ustawiamy
                # jego wartość na 1, ale tylko przy pierwszym przejściu. Dla kolejnych dodajemy z bloku "try"
                completed_task_dict[record["userId"]] = 1
    return completed_task_dict


def chooseHighestCompleters(task_dict):
    highest_completers = []
    for userId, tasks_completed in completed_task_dict.items():
        max_amount_tasks_completed = max(completed_task_dict.values())
        if tasks_completed == max_amount_tasks_completed:
            highest_completers.append(userId)
    return highest_completers


# sposób nr 1 na rozwiązanie. Pobranie strony raz, przetworzenie do słownika, obróbka na miejscu
def get_users(highest_completers):
    user_list = []
    try:
        users_response = requests.get("https://jsonplaceholder.typicode.com/users").json()
    except json.decoder.JSONDecodeError:
        print("The site doesn't contain json data.")
    else:
        for entry in users_response:
            if entry["id"] in highest_completers:
                user_list.append(entry["name"])
        return user_list


# sposób nr 2. Podstawienie id usera z "highest completers" do linku i łączenie się ze stroną oddzielnie za każdym razem
# o ile sposób działa, o tyle jest wolny, ponieważ wąskim gardłem jest prędkość łączenia się ze stroną
def get_users2(highest_completers):
    user_list = []
    for entry in highest_completers:
        try:
            users_response = requests.get("https://jsonplaceholder.typicode.com/users/" + str(entry))
            completers = users_response.json()
            user_list.append(completers["name"])
        except json.decoder.JSONDecodeError:
            print("The site doesn't contain json data.")
    return user_list


def make_string_from_list(highest_completers):
    t_string = ""
    for id in highest_completers:
        t_string += "id=" + str(id) + "&"
    # string.rstrip() usuwa z prawej strony ostatni określony znak
    string_completers = t_string.rstrip("&")
    return string_completers


# sposób nr 3. Używamy faktu, że do strony jsonplaceholder można używać parametru, który łączy wszystkie wejścia
# w jedną stronę
def get_users3(string_completers):
    user_list = []
    try:
        users_response = requests.get("https://jsonplaceholder.typicode.com/users/", params=string_completers)
        completers = users_response.json()
    except json.decoder.JSONDecodeError:
        print("The site doesn't contain json data.")
    else:
        for user in completers:
            user_list.append(user["name"])
    return user_list

if __name__ == '__main__':
    response = requests.get("https://jsonplaceholder.typicode.com/todos")

try:
    tasks = response.json()
except json.decoder.JSONDecodeError:
    print("The site doesn't contain json data.")
else:
    completed_task_dict = countTaskCompletionFrequency(tasks)
    highest_completers = chooseHighestCompleters(completed_task_dict)
    users = get_users(highest_completers)
    # rozwiązanie 1
    print("First solution: The cookie gets distributed to: ", users)
    users2 = get_users2(highest_completers)
    print("Second solution: The cookie gets distributed to: ", users2)
    string_completers = make_string_from_list(highest_completers)
    users3 = get_users3(string_completers)
    print("Third solution: The cookie gets distributed to: ", users3)