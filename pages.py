
from flask import Flask, Blueprint, request, jsonify, render_template, url_for, redirect
import examples1
import examples2
import examples3
import examples4
import examples5
import examples6
import examples7

pages = Blueprint('pages', 'pages')


capturing = False     # set to True to create pages for the static website


@pages.route('/')
def home():
    html = render_template('home')
    if capturing:
        capture('index', html.replace('">&bull;', '.html">&bull;'))
    return html

@pages.route('/examples1' )
def exset1():
    svgset = examples1.run_all()
    html = render_template('examples1', svgset=svgset)
    if capturing:
        capture('examples1', html.replace('examples1_static', 'examples1_static.html'))
    return html

@pages.route('/examples1_static' )
def exset1_static():
    html = render_template('examples1_static')
    if capturing:
        capture('examples1_static', html)
    return html

@pages.route('/examples2' )
def exset2():
    svgset = examples2.run_all()
    html = render_template('examples2', svgset=svgset)
    if capturing:
        capture('examples2', html)
    return html

@pages.route('/examples3' )
def exset3():
    svgset = examples3.run_all()
    html = render_template('examples3', svgset=svgset)
    if capturing:
        capture('examples3', html)
    return html

@pages.route('/examples4' )
def exset4():
    svgset = examples4.run_all()
    html = render_template('examples4', svgset=svgset)
    if capturing:
        capture('examples4', html.replace('examples6', 'examples6.html'))
    return html

@pages.route('/examples5' )
def exset5():
    svgset = examples5.run_all()
    html = render_template('examples5', svgset=svgset)
    if capturing:
        capture('examples5', html)
    return html

@pages.route('/examples6' )
def exset6():
    svgset = examples6.run_all()
    html = render_template('examples6', svgset=svgset)
    if capturing:
        capture('examples6', html)
    return html

@pages.route('/examples7' )
def exset7():
    svgset = examples7.run_all()
    html = render_template('examples7', svgset=svgset)
    if capturing:
        capture('examples7', html)
    return html

@pages.route('/examples8' )
def exset8():
    html = render_template('examples8')
    if capturing:
        capture('examples8', html)
    return html

@pages.route('/docs' )
def docs():
    if capturing:
        capture('docs', html)
    return render_template('docs')

@pages.route('/docs_old' )
def docs_old():
    return render_template('docs_old')


def capture(tfile, html):
    fp = open(f'site/{tfile}.html', 'w')
    print(html, file=fp)
    fp.close()
    return 
