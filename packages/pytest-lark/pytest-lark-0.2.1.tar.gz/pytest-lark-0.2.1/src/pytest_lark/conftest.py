import os

def pytest_html_report_title(report):
    report.title = "My test report"

def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.H1("My Test Summary")])
    summary.insert(1, html.P("custom stuff"))
    postfix.extend([html.P("more custom stuff")])

def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.pop()

def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.pop()

def pytest_html_results_table_cell(cell):
    if hasattr(cell, 'html'):
        cell.html = cell.html.replace('<pre>', '<pre style="white-space: pre-wrap;">')

def pytest_html_report_html(report, data):
    data.append(pytest_html.utils.get_stylesheet())
    data.append(pytest_html.utils.get_script('sorttable.js'))
    data.append(pytest_html.utils.get_script('my.js'))

def pytest_collection_modifyitems(items):
    for item in items:
        item.parent.nodeid = item.parent.fspath.relto(os.getcwd())

def pytest_html_results_table_row(report, cells):
    cells.insert(0, html.td(report.nodeid.split("::")[0]))
    cells.pop()

def pytest_html_results_table_header(cells):
    cells.insert(0, html.th('Directory'))
    cells.pop()

def pytest_html_results_table_row(report, cells):
    cells.insert(0, html.td(os.path.dirname(report.nodeid.split("::")[0])))
    cells.pop()

def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Code Example'))
    cells.pop()

def pytest_html_results_table_row(report, cells):
    source = inspect.getsource(report.obj)
    cells.insert(2, html.td(html.Code(source).render()))
    cells.pop()
