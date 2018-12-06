# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db
from common.models.member.Member import Member
from common.models.question.Question import Question



class Answer(db.Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.ForeignKey('member.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    question_id = db.Column(db.ForeignKey('question.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    good_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    comment_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    content = db.Column(db.String(400), nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    member = db.relationship('Member', primaryjoin='Answer.member_id == Member.id', backref='answers')
    question = db.relationship('Question', primaryjoin='Answer.question_id == Question.id', backref='answers')


# class Member(db.Model):
#     __tablename__ = 'member'
#
#     id = db.Column(db.Integer, primary_key=True)
#     openid = db.Column(db.String(80), nullable=False, server_default=db.FetchedValue())
#     nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
#     mobile = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue())
#     sex = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
#     avatar = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
#     salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
#     reg_ip = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
#     status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
#     updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
#     created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
#
#
# class Question(db.Model):
#     __tablename__ = 'question'
#
#     id = db.Column(db.Integer, primary_key=True)
#     member_id = db.Column(db.ForeignKey('member.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
#     answer_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
#     attention_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
#     content = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
#     topic = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
#     created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
#     updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
#
#     member = db.relationship('Member', primaryjoin='Question.member_id == Member.id', backref='questions')
