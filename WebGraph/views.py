import os

import pandas
from django.contrib import auth, messages
from django.contrib.auth import logout
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from django.shortcuts import render
from graphos.renderers.gchart import ColumnChart
from graphos.sources.simple import SimpleDataSource

from WebGraph.forms import Login
from analysis import analyze


def index(request):
    return render(request, 'analyze.html')


def login(request):
    return render(request, 'login.html')


def analyze_data(request):
    folder = 'uploads/'
    uploaded_filename = request.FILES['file'].name
    BASE_PATH = 'WebGraph/'

    try:
        os.mkdir(os.path.join(BASE_PATH, folder))
    except:
        pass

    full_filename = os.path.join(BASE_PATH, folder, uploaded_filename)
    fout = open(full_filename, 'wb+')

    file_content = ContentFile(request.FILES['file'].read())

    try:
        for chunk in file_content.chunks():
            fout.write(chunk)
        fout.close()
    except:
        messages.add_message(request, messages.ERROR, 'Some Error Occurred!!!')

    combination, ipc_r, ipc_p, cpc_p, upc_p, ipc_m, cpc_r, cpc_m, upc_r, upc_m = (analyze(full_filename) for i in range(10))

    print("VIEWS.PY " + str(combination))

    if combination is not None:
        classes = ["table", "table-bordered", "table-striped", "table-hover", "table-dark"]

        ipc_r['recall'] = ipc_r['recall'].astype(float)
        ipc_p['precision'] = ipc_p['precision'].astype(float)
        ipc_m['mpr'] = ipc_m['mpr'].astype(float)
        cpc_r['recall'] = cpc_r['recall'].astype(float)
        cpc_p['precision'] = cpc_p['precision'].astype(float)
        cpc_m['mpr'] = cpc_m['mpr'].astype(float)
        upc_r['recall'] = upc_r['recall'].astype(float)
        upc_p['precision'] = upc_p['precision'].astype(float)
        upc_m['mpr'] = upc_m['mpr'].astype(float)

        ipc_r_list = ipc_r.values.tolist()
        ipc_r_list.insert(0, ["IPC", "Recall"])
        ipc_p_list = ipc_r.values.tolist()
        ipc_p_list.insert(0, ["IPC", "PRECISION"])
        ipc_m_list = ipc_m.values.tolist()
        ipc_m_list.insert(0, ["IPC", "MPR"])
        cpc_r_list = cpc_r.values.tolist()
        cpc_r_list.insert(0, ["CPC", "Recall"])
        cpc_p_list = cpc_r.values.tolist()
        cpc_p_list.insert(0, ["CPC", "PRECISION"])
        cpc_m_list = cpc_m.values.tolist()
        cpc_m_list.insert(0, ["CPC", "MPR"])
        upc_r_list = upc_r.values.tolist()
        upc_r_list.insert(0, ["UPC", "Recall"])
        upc_p_list = upc_r.values.tolist()
        upc_p_list.insert(0, ["UPC", "PRECISION"])
        upc_m_list = upc_m.values.tolist()
        upc_m_list.insert(0, ["UPC", "MPR"])

        ipc_r_data = SimpleDataSource(data=ipc_r_list)
        ipc_p_data = SimpleDataSource(data=ipc_p_list)
        ipc_m_data = SimpleDataSource(data=ipc_m_list)
        cpc_r_data = SimpleDataSource(data=cpc_r_list)
        cpc_p_data = SimpleDataSource(data=cpc_p_list)
        cpc_m_data = SimpleDataSource(data=cpc_m_list)
        upc_r_data = SimpleDataSource(data=upc_r_list)
        upc_p_data = SimpleDataSource(data=upc_p_list)
        upc_m_data = SimpleDataSource(data=upc_m_list)

        ipc_chart_r = ColumnChart(ipc_r_data, options={'title': 'IPC Recall', 'width': 800, 'height': 500,
                                                       'hAxis': {'slantedText': 'true', 'slantedTextAngle': 55,
                                                                 'showTextEvery': 1}, })
        ipc_chart_p = ColumnChart(ipc_p_data, options={'title': 'IPC Precision', 'width': 800, 'height': 500,
                                                       'hAxis': {'slantedText': 'true', 'slantedTextAngle': 55,
                                                                 'showTextEvery': 1}, })
        ipc_chart_m = ColumnChart(ipc_m_data, options={'title': 'IPC MPR', 'width': 800, 'height': 500,
                                                       'hAxis': {'slantedText': 'true', 'slantedTextAngle': 55,
                                                                 'showTextEvery': 1}, })
        cpc_chart_r = ColumnChart(cpc_r_data, options={'title': 'CPC Recall', 'width': 800, 'height': 520,
                                                       'hAxis': {'slantedText': 'true', 'slantedTextAngle': 55,
                                                                 'showTextEvery': 1}, })
        cpc_chart_p = ColumnChart(cpc_p_data, options={'title': 'CPC PRECISION', 'width': 800, 'height': 520,
                                                       'hAxis': {'slantedText': 'true', 'slantedTextAngle': 55,
                                                                 'showTextEvery': 1}, })
        cpc_chart_m = ColumnChart(cpc_m_data, options={'title': 'CPC MPR', 'width': 800, 'height': 520,
                                                       'hAxis': {'slantedText': 'true', 'slantedTextAngle': 55,
                                                                 'showTextEvery': 1}, })
        upc_chart_r = ColumnChart(upc_r_data, options={'title': 'UPC Recall', 'width': 800, 'height': 500,
                                                       'hAxis': {'slantedText': 'true', 'slantedTextAngle': 55,
                                                                 'showTextEvery': 1}, })
        upc_chart_p = ColumnChart(upc_p_data, options={'title': 'UPC PRECISION', 'width': 800, 'height': 500,
                                                       'hAxis': {'slantedText': 'true', 'slantedTextAngle': 55,
                                                                 'showTextEvery': 1}, })
        upc_chart_m = ColumnChart(upc_m_data, options={'title': 'UPC MPR', 'width': 800, 'height': 500,
                                                       'hAxis': {'slantedText': 'true', 'slantedTextAngle': 55,
                                                                 'showTextEvery': 1}, })

        ipc_table_r = ipc_r.to_html(index=False, classes=classes)
        ipc_table_p = ipc_p.to_html(index=False, classes=classes)
        ipc_table_m = ipc_m.to_html(index=False, classes=classes)
        cpc_table_r = cpc_r.to_html(index=False, classes=classes)
        cpc_table_p = cpc_p.to_html(index=False, classes=classes)
        cpc_table_m = cpc_m.to_html(index=False, classes=classes)
        upc_table_r = upc_r.to_html(index=False, classes=classes)
        upc_table_p = upc_p.to_html(index=False, classes=classes)
        upc_table_m = upc_m.to_html(index=False, classes=classes)

        combination = pandas.DataFrame(combination, columns=['IPC and CPC', 'IPC and UPC'])
        combination = combination.to_html(index=False, classes=classes)

        context = {
            'ipc_chart_r': ipc_chart_r,
            'ipc_chart_p': ipc_chart_p,
            'ipc_chart_m': ipc_chart_m,
            'cpc_chart_r': cpc_chart_r,
            'cpc_chart_p': cpc_chart_p,
            'cpc_chart_m': cpc_chart_m,
            'upc_chart_r': upc_chart_r,
            'upc_chart_p': upc_chart_p,
            'upc_chart_m': upc_chart_m,

            'ipc_table_r': ipc_table_r,
            'ipc_table_p': ipc_table_p,
            'ipc_table_m': ipc_table_m,
            'cpc_table_r': cpc_table_r,
            'cpc_table_p': cpc_table_p,
            'cpc_table_m': cpc_table_m,
            'upc_table_r': upc_table_r,
            'upc_table_p': upc_table_p,
            'upc_table_m': upc_table_m,
            'combination': combination
        }
        return render(request, 'result.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'Some Error Occurred!!!')
        return redirect('/main/')


def validate_login(request):
    if request.method == 'POST':
        # print("Here!!!")
        form = Login(request.POST)

        if form.is_valid():

            username = form['username'].value()
            password = form['password'].value()

            print("Username " + username)
            print("Password " + password)

            user = auth.authenticate(username=username, password=password)

            if user is not None:

                auth.login(request, user)
                return redirect('/main/')
            else:
                messages.add_message(request, messages.ERROR, 'INCORRECT USERNAME / PASSWORD')
                return redirect('/')
    else:
        return redirect('/')


def result(request):
    return render(request, 'result.html')


def logout_system(request):
    logout(request)
    return redirect('/')