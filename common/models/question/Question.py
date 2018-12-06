# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from application import db


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.ForeignKey('member.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    answer_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    attention_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    content = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    topic = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    notes = db.Column(db.String(100), server_default=db.FetchedValue())
    visited_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    member = db.relationship('Member', primaryjoin='Question.member_id == Member.id', backref='questions')
