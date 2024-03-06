import time
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime, date, time, timedelta
import peewee, calendar
from model import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/index2.html')  
    

"""Обработчик, работа за сутки.""" 
@app.route('/day')    
def day():
    _,day_count = calendar.monthrange(2024, 2)
    begin_date = date(2024, 2, 1)
    end_date = date(2024, 2, day_count)
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days + 1)):                
            yield start_date + timedelta(n)            
    x = 0
    data = []
    for dat in daterange(begin_date, end_date):
        row = {'date': dat.strftime('%d.%m.%Y')}
        own_day = []
        commercial_day = []
        own_month = []
        commercial_month = []   
        [own_day.append(float(owns.amount)) for owns in Own_transport.select()\
        .where(Own_transport.date == row['date'])]

        [commercial_day.append(float(commercials.amount)) for commercials \
        in Commercial_transport.select().where(Commercial_transport.date == row['date'])]    
        row['number of refills own_day'] =  len(own_day)
        row['V_own_day'] =  sum(own_day)
        row['number of refills commercial_day'] =  len(commercial_day)
        row['V_commercial_day'] =  sum(commercial_day)
        row['number of refills in_total'] =  len(own_day) + len(commercial_day)
        row['V in_total'] =  sum(own_day) + sum(commercial_day)
        data.append(row)  
        print(data[x])
        x += 1    
    [own_month.append(float(owns.amount)) for owns in Own_transport.select()]
    sum_V_own_month = sum(own_month)
    number_of_refills_sum_V_own_month = len(own_month)
    [commercial_month.append(float(commercials.amount)) for commercials in Commercial_transport.select()]
    sun_V_commercial_month = sum(commercial_month)
    number_of_refills_V_commercial_month = len(commercial_month)
    sum_number_of_refills_month = len(own_month) + len(commercial_month)
    sum_V_month = sum(own_month) + sum(commercial_month)  
  
    return render_template('/day.html', data=data, sum_V_own_month=sum_V_own_month, \
                           number_of_refills_sum_V_own_month=number_of_refills_sum_V_own_month, 
                           number_of_refills_V_commercial_month=number_of_refills_V_commercial_month, \
                           sun_V_commercial_month=sun_V_commercial_month,\
                           sum_number_of_refills_month=sum_number_of_refills_month, \
                           sum_V_month=sum_V_month)   


"""Обработчик для собственного транспорта ОБЩИЙ."""
@app.route('/ats', methods=['POST', 'GET']) 
def ats():
    if request.method == 'POST':
        Own_transport(date=request.form['date'], name=request.form['name'], \
                      waybill=request.form['waybill'], driver=request.form['driver'], \
                      amount=request.form['amount'], column=request.form['column'], \
                      note=request.form['note']).save()
        return redirect(url_for('ats'))   
    owns = Own_transport.select()        
    return render_template('ats.html', owns=owns)


"""Перенаправление на обработчик для собственного транспорта смена."""
@app.route('/atss') 
def ats_today():
    return redirect(url_for('dat', dat=datetime.date.today().strftime('%d.%m.%Y')))


"""Обработчик для собственного  транспорта смена."""
@app.route('/ats/<dat>', methods=['POST', 'GET']) 
def dat(dat):
    if request.method == 'POST' and request.form['date'] == dat:
        amount = request.form['amount']
        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            ...
        Own_transport(date=request.form['date'], name=request.form['name'], \
                      waybill=request.form['waybill'], driver=request.form['driver'],
                      amount=amount, column=request.form['column'], note=request.form['note']).save()

        return redirect(url_for('dat', dat=dat))
    owns = Own_transport.select().where(Own_transport.date == dat)

    t = 0
    n = 0
    for i in owns:
        try:
            t += i.amount
            n += 1
        except TypeError:
            pass  
    return render_template('/ats.html', owns=owns, dat=dat, n=n,t=t)


"""Обработчик для стороннего транспорта ОБЩИЙ."""
@app.route('/atsext', methods=['POST', 'GET']) 
def atsext():
    if request.method == 'POST':
        Commercial_transport(date=request.form['date'], name=request.form['name'], \
                             amount=request.form['amount'], money=request.form['money'], \
                             note=request.form['note']).save()
        return redirect(url_for('atsext'))
    commercials = Commercial_transport.select()
    
    return render_template('atsext.html', commercials=commercials)


"""Перенаправление на обработчик для стороннего транспорта смена."""
@app.route('/ext') 
def ats_today_ext():
    return redirect(url_for('dat1', dat1=datetime.date.today().strftime('%d.%m.%Y')))


"""Обработчик для стороннего транспорта смена."""
@app.route('/atsext/<dat1>', methods=['POST', 'GET']) 
def dat1(dat1):
    if request.method == 'POST' and request.form['date'] == dat1:
        if request.form['name'] == 'Хлебозавод' or request.form['name'] == 'Дом быта' \
        or request.form['name'] == 'Автобаза №3' or request.form['name'] == 'Физлицо' \
        or request.form['name'] == '':
            amount = request.form['amount']
            try:
                amount = float(amount.replace(',', '.'))
            except ValueError:
                ...
            money = request.form['money']
            try:
                money = float(money.replace(',', '.'))
            except ValueError:
                ...

            Commercial_transport(date=request.form['date'], name=request.form['name'],\
                                 amount=amount, money=money, note=request.form['note']).save()

            return redirect(url_for('dat1', dat1=dat1))
    commercials = Commercial_transport.select().where(Commercial_transport.date == dat1)
    t = 0
    n = 0
    for i in commercials:
        try:
            t += i.amount
            n += 1
        except TypeError:
            pass 

    return render_template('/atsext.html', commercials=commercials, dat1=dat1, n=n, t=t)


if __name__ == '__main__':    
    app.run(debug=True,)
    
