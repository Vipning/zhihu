from web.controllers.api import route_api
from flask import request,jsonify
from application import app,db
from common.libs.Helper import getCurrentDate,getInterval
from common.models.answer.Answer import Answer
from common.models.member.Member import Member

@route_api.route('/answer/reply',methods =['POST','GET'])
def reply():
    resp = {'code': 200, 'msg': '传输成功', 'data': {}}  # 返回值
    req = request.values  # 前台的数据
    # app.logger.info(req)
    content = req['answer'] if 'answer' in req else ''
    member_id = req['token'].split('#')[1] if 'token' in req else ''
    question_id =req['question_id'] if 'question_id' in req else 0

    if member_id != '' and question_id!=0:
        model_answer = Answer()
        model_answer.member_id = member_id
        model_answer.question_id=question_id
        model_answer.content = content
        model_answer.created_time = model_answer.updated_time = getCurrentDate()
        db.session.add(model_answer)
        db.session.commit()
        resp['msg'] = '插入成功'
    return jsonify(resp)

@route_api.route('/answer/getAnswer',methods =['POST','GET'])
def getAnswer():
    resp = {'code': 200, 'msg': '传输成功', 'data': []}  # 返回值
    req = request.values  # 前台的数据
    question_id = req['qid'] if 'qid' in req else 0
    if question_id!=0:
        answerInfo=Answer.query.filter_by(question_id=question_id).all()
        for item in answerInfo:
            memberInfo=Member.query.filter_by(id=item.member_id).first()
            tempInfo={
                'nickname':memberInfo.nickname,
                'avatar':memberInfo.avatar,
                'content':item.content,
                'good_num':item.good_num,
                'comment_num':item.comment_num,
                'interval':getInterval(item.updated_time)
            }
            resp['data'].append(tempInfo)
    return jsonify(resp)