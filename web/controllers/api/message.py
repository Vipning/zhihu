from web.controllers.api import route_api
from flask import request,jsonify
from application import app,db
from common.libs.Helper import getCurrentDate,getInterval
from sqlalchemy import and_
from common.models.attention.Attention import Attention
from common.models.question.Question import Question
from common.models.member.Member import Member
from common.models.answer.Answer import Answer
from common.models.message.Message import Message

@route_api.route('/message/check_focus',methods =['POST','GET'])
def check_focus():
    resp = {'code': 200, 'msg': '传输成功', 'data': {}}  # 返回值
    req = request.values  # 前台的数据
    # app.logger.info(req)
    member_id=req['token'].split('#')[1] if 'token' in req else 0
    question_id=req['question_id'] if 'question_id' in req else 0
    record=Attention.query.filter(and_(Attention.member_id==member_id,Attention.question_id==question_id)).first()
    if record:
        resp['data']['flag']=True
    else:
        resp['data']['flag'] = False
    return jsonify(resp)


@route_api.route('/message/focus',methods =['POST','GET'])
def focus():
    resp = {'code': 200, 'msg': '传输成功', 'data': {}}  # 返回值
    req = request.values  # 前台的数据
    member_id = req['token'].split('#')[1] if 'token' in req else 0
    question_id = req['question_id'] if 'question_id' in req else 0
    if member_id!=0 and question_id!=0:
        model_attention=Attention()
        model_attention.member_id=member_id
        model_attention.question_id=question_id
        model_attention.created_time=model_attention.updated_time=getCurrentDate()
        db.session.add(model_attention)
        db.session.commit()
        resp['msg'] = '插入成功'
    return jsonify(resp)

@route_api.route('/message/no_focus',methods =['POST','GET'])
def no_focus():
    resp = {'code': 200, 'msg': '传输成功', 'data': {}}  # 返回值
    req = request.values  # 前台的数据
    member_id = req['token'].split('#')[1] if 'token' in req else 0
    question_id = req['question_id'] if 'question_id' in req else 0
    record = Attention.query.filter(
        and_(Attention.member_id == member_id, Attention.question_id == question_id)).first()
    db.session.delete(record)
    db.session.commit()
    resp['msg'] = '删除成功'
    return jsonify(resp)

@route_api.route('/message/show_focus',methods =['POST','GET'])
def show_focus():
    resp = {'code': 200, 'msg': '传输成功', 'data': []}  # 返回值
    req = request.values  # 前台的数据
    member_id = req['token'].split('#')[1] if 'token' in req else 0
    quesInfo=Question.query.filter(Question.member_id==member_id).all()
    if quesInfo:
        for ques in quesInfo:
            attentInfo=Attention.query.filter(Attention.question_id==ques.id).all()
            if attentInfo:
                for item in attentInfo:
                    tempInfo={
                        'nickname':Member.query.filter(Member.id==item.member_id).first().nickname,
                        'avatar':Member.query.filter(Member.id==item.member_id).first().avatar,
                        'question':ques.content
                    }
                    resp['data'].append(tempInfo)
    return jsonify(resp)

@route_api.route('/message/show_reply',methods =['POST','GET'])
def show_reply():
    resp = {'code': 200, 'msg': '传输成功', 'data': []}  # 返回值
    req = request.values  # 前台的数据
    user_id = req['token'].split('#')[1] if 'token' in req else 0
    quesInfo = Question.query.filter(Question.member_id == user_id).all()
    if quesInfo:
        for ques in quesInfo:
            answerInfo = Answer.query.filter(Answer.question_id == ques.id).all()
            if answerInfo:
                for item in answerInfo:
                    tempInfo = {
                        'member_id':item.member_id,
                        'nickname': Member.query.filter(Member.id == item.member_id).first().nickname,
                        'avatar': Member.query.filter(Member.id == item.member_id).first().avatar,
                        'question': ques.content,
                        'answer_id':item.id,
                        'question_id':ques.id
                    }
                    resp['data'].append(tempInfo)
    return jsonify(resp)

@route_api.route('/message/show_detail',methods =['POST','GET'])
def show_detail():
    resp = {'code': 200, 'msg': '传输成功', 'data':[]}  # 返回值
    req = request.values  # 前台的数据
    ques_id=req['question_id'] if 'question_id' in req else 0
    answer_id=req['answer_id'] if 'answer_id' in req else 0
    quesInfo = Question.query.filter(Question.id == ques_id).first()
    userInfo = Member.query.filter(Member.id ==quesInfo.member_id).first()
    answerInfo=Answer.query.filter(Answer.id == answer_id).first()
    questionInfo={
        'content':quesInfo.content,
        'notes':quesInfo.notes
    }
    resp['data'].append(questionInfo)
    item={
        'nickname':userInfo.nickname,
        'avatar':userInfo.avatar,
        'content':answerInfo.content,
        'good_num':answerInfo.good_num
    }
    resp['data'].append(item)
    return jsonify(resp)

@route_api.route('/message/send',methods =['POST','GET'])
def send():
    resp = {'code': 200, 'msg': '传输成功', 'data':{}}  # 返回值
    req = request.values  # 前台的数据
    send_id=req['token'].split('#')[1] if 'token' in req else 0
    receive_id=req['receive_id'] if 'receive_id' in req else 0
    content=req['content'] if 'content' in req else ''
    if send_id!=0 and receive_id!=0:
        model_message=Message()
        model_message.send_id=send_id
        model_message.receive_id=receive_id
        model_message.content=content
        model_message.created_time=getCurrentDate()
        db.session.add(model_message)
        db.session.commit()
        resp['msg']='插入成功'
        memberInfo=Member.query.filter(Member.id==send_id).first()
        resp['data']['avatar']=memberInfo.avatar
    return jsonify(resp)

@route_api.route('/message/show_message',methods =['POST','GET'])
def show_message():
    resp = {'code': 200, 'msg': '传输成功', 'data': []}  # 返回值
    req = request.values  # 前台的数据
    receive_id = req['token'].split('#')[1] if 'token' in req else 0
    if receive_id!=0:
        MessageList=Message.query.filter(Message.receive_id==receive_id).all()
        if MessageList:
            for item in MessageList:
                MemberInfo=Member.query.filter(Member.id==item.send_id).first()
                tempdata={
                    'send_id':item.send_id,
                    'nickname':MemberInfo.nickname,
                    'avatar':MemberInfo.avatar,
                    'text':item.content,
                    'interval':getInterval(item.created_time)
                }
                resp['data'].append(tempdata)
    return jsonify(resp)