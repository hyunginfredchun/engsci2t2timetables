from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request

engsci = DBHelper()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/get_timetable')
def get_timetable():
    query = request.args.get('name')

    names = []

    timetable = False

    if query != None:
        name = query

        current_user = engsci.get_user(name)

        if current_user != None:
            timetable = current_user['timetable']

            for x in range(len(timetable)):
                day = current_user['timetable'][x]

                names.append([])

                for y in range(len(day)):
                    hour = day[y]

                    names[x].append([])

                    users = engsci.db.users.find()

                    for user in users:
                        if hour == user['timetable'][x][y]:
                            names[x][y].append(user['name'])

                    names[x][y].sort()

        else:
            return 'Name not found.'

    return render_template('get_timetable.html', names=names, timetable=timetable)


@app.route('/add_timetable')
def add_timetable():
    query = request.args.get('name')

    if query != None:
        name = query

        query = request.args.getlist('timetable')

        timetable = [[] for x in range(5)]

        for x in range(len(query)):
            if x % 5 == 0:
                timetable[0].append(query[x])

            elif x % 5 == 1:
                timetable[1].append(query[x])

            elif x % 5 == 2:
                timetable[2].append(query[x])

            elif x % 5 == 3:
                timetable[3].append(query[x])

            else:
                timetable[4].append(query[x])

        engsci.add_user(name, timetable)

        return 'Your timetable has been successfully entered.'

    return render_template('add_timetable.html')


if __name__ == '__main__':
    app.run()
