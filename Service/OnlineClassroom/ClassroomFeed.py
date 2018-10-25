from flask import Blueprint
from bson import ObjectId
from flask import Flask, render_template, request, redirect, session
from Database.database import db


def show_news_feed():
    pymongo_cursor = db.hello_world123.find()
    all_data = list(pymongo_cursor)
    data = all_data
    return data


def update_post(data):
    data = {"posttext": data['message'],"postfile": data['files'] , "authors": "forkkr"}
    posts = db.hello_world123
    post_id = posts.insert_one(data).inserted_id
    return


def comment_entry(id):
    poststring=db.hello_world123.find_one({'_id': ObjectId(id)});
    pymongo_cursor = db.comments.find( { "postid" : id} )
    all_comments = list(pymongo_cursor)
    comments= all_comments
    return poststring, comments


def update_comment(id , data):
    data = {"posttext": data['message'],"postid":id ,  "authors": "forkkr"}
    posts = db.comments
    post_id = posts.insert_one(data).inserted_id
    return
