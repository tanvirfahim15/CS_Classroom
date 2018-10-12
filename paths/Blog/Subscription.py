from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, session, Blueprint
from utility.database import db


app = Blueprint('blog_subscribe', __name__)