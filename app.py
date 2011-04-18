#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = 'KO.2011.0415'
print 'ver:', __version__

import sqlite3
import web
import uuid
render = web.template.render('templates/')
web.config.debug = False

urls = [
    '/', 'cdn',
    '(.*)/ru', 'ru',
    '(.*)/cdx', 'cdx',
    '(.*)/cdx1', 'cdx1',
    '(.*)/reguseradd','reguseradd',
    '(.*)/prexit', 'prexit',
]
class cdn(object):
    def GET(self): # Окно приглашение к индентификации пользователя.
        print '2222', 'cdx'
        web.header('Content-type', 'text/html; charset=utf-8')
        return render.index('Введите свой логин и пароль!')

class cdx(object):
    def GET(self,name): #идентификация сессии и идентификация пользователя.
        print '2222', 'cdx'
        web.header('Content-type', 'text/html; charset=utf-8')
        con = sqlite3.connect('overhead.sqlite')
        cur = con.cursor()
        i = web.input()
        if i: #Открыть навую сессию после идентификации пользователя
            n = i.name
            p = i.passw
            sql = u"select * from auth_ko where user=? and passw=?"
            cur.execute(sql, (n, p))
            r = cur.fetchall()
            if r:
                rez = r[0][1]
                sid = uuid.uuid4().hex
                sid = str(sid)
                sqlu = u"update auth_ko set sid=? where user=? and passw=?"
                cur.execute(sqlu, (sid, n, p))
                con.commit()
                web.setcookie('sid', sid, 3600)
                print rez, 'sid=',sid
                raise web.redirect('/cdx1')  #Начата новая сессия. Переходим на следующий шаг.
            else:
                return render.index('Логин или пароль неверен! ')
        else:
            raise web.redirect('/cdn') #Сюда попал, если логин и пароль не введены.

class cdx1(object):
    def GET(self, name):
        print '2222', 'cdx1'
        web.header('Content-type', 'text/html; charset=utf-8')
        con = sqlite3.connect('overhead.sqlite')
        cur = con.cursor()
        try:
            #sid = web.getcookie('sid')
            sid = web.cookies().get('sid')
        except:
            sid =''
        print 'sid=', sid
        if sid:  #Сессия существует? Работа с пользователем продолжается?
            sql = u"select * from auth_ko where sid=?"
            cur.execute(sql, (sid,))
            r = cur.fetchall()
            if r:
                print r
                return render.prexit('На этом пока все!')
        else:
            return render.index('Введите свой логин и пароль!')

        return render.prexit('На этом пока все!')

class ru(object):
    def GET(self, name):
        print '2222', 'ru'
        print '111111', 'reguser'
        return render.reguseradd('Введите свои данные!')   # Переходим на следующий шаг.


class reguseradd(object):
    def GET(self, name):
        print '2222', 'reguseradd'
        web.header('Content-type', 'text/html; charset=utf-8')
        i = web.input()
        if i: #Открыть навую сессию после идентификации пользователя
            n = i.name
            p = i.passw
            if (n and p):
                con = sqlite3.connect('overhead.sqlite')
                cur = con.cursor()
                sql = u"select * from auth_ko where user=?"
                cur.execute(sql, (n,))
                r = cur.fetchall()
                if r:
                    return render.reguseradd('Найдите другой логин! Этот занят!')
                else:
                    cur.execute('select count(id) from auth_ko')
                    r1 =cur.fetchall()
                    kz = r1[0][0] +1
                    sid = uuid.uuid4().hex
                    sqladd = u"insert into auth_ko (sid, user, passw, act, id) values(?,?,?,?,?)"
                    cur.execute(sqladd, (sid, n, p, 1, kz))
                    con.commit()
                    return render.prexit('На этом пока все!')   # Переходим на следующий шаг.

            else:
                return render.reguseradd('Только после ввода логин и пароля!')
        else:
            return render.reguseradd('Только после ввода логин и пароля!')

class prexit(object):
    def GET(self, name):
        print '2222', 'prexit'
        raise web.redirect('/')


app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
