# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from application import db


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


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    send_id = db.Column(db.ForeignKey('member.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    receive_id = db.Column(db.ForeignKey('member.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    content = db.Column(db.String(400), nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    receive = db.relationship('Member', primaryjoin='Message.receive_id == Member.id', backref='member_messages')
    send = db.relationship('Member', primaryjoin='Message.send_id == Member.id', backref='member_messages_0')
