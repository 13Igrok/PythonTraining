from pickle import APPEND
from flask import Flask, render_template


def main():
    return render_template('index.html')


@APPEND.route('/about')
def showSignUp():
    return render_template('about.html')
