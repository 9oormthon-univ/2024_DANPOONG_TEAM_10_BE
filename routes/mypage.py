from flask import Blueprint, request,redirect,session,jsonify


mypage = Blueprint("mypage", __name__)

@mypage.route("/")
def