from web.controllers.api import route_api
from flask import request,jsonify
from application import app,db
from common.libs.Helper import getCurrentDate
from common.models.question.Question import Question
from common.models.answer.Answer import Answer
from common.models.member.Member import Member
from sqlalchemy import or_

@route_api.route('/question/ask',methods =['POST','GET'])
def ask():
    resp = {'code': 200, 'msg': '传输成功', 'data': {}}  # 返回值
    req = request.values  # 前台的数据
    # app.logger.info(req)
    content=req['content'] if 'content' in req else ''
    topic=req['topic'] if 'topic' in req else ''
    descrip=req['descrip'] if 'descrip' in req else ''
    member_id=req['token'].split('#')[1] if 'token' in req else ''

    if member_id!='':
        model_question=Question()
        model_question.member_id=member_id
        model_question.content=content
        model_question.notes=descrip
        model_question.topic=topic
        model_question.created_time=model_question.updated_time=getCurrentDate()
        db.session.add(model_question)
        db.session.commit()
        resp['msg']='插入成功'
    return jsonify(resp)

@route_api.route('/question/getQuesInfo',methods=['POST','GET'])
def getQuesInfo():
    resp = {'code': 200, 'msg': '传输成功', 'data':{}}
    req=request.values
    question_id=req['qid'] if 'qid' in req else 0
    if(question_id!=0):
        question_info=Question.query.filter_by(id=question_id).first()
        resp['data']['topic']=question_info.topic
        resp['data']['content']=question_info.content
        resp['data']['notes']=question_info.notes
        question_info.visited_num=question_info.visited_num+1
        db.session.add(question_info)
        db.session.commit()
        resp['data']['visited_num']=question_info.visited_num


    return jsonify(resp)


@route_api.route('/question/show_ques',methods =['POST','GET'])
def show_ques():
    resp={'code': 200, 'msg': '传输成功', 'data':[]}
    question_list=Question.query.filter_by().all()

    if question_list:
        for item in question_list:
            # app.logger.info(item.id)
            member_info=Member.query.filter_by(id=item.member_id).first()
            answer_info=Answer.query.filter_by(question_id=item.id).first()
            temp_data={
                'question_id':item.id,
                'member_id':item.member_id,
                'nickname': member_info.nickname,
                'avatar': member_info.avatar,
                'question':item.content,
                'topic':item.topic,
                'notes':item.notes,
            }
            if answer_info:
                temp_data['answer_id']=answer_info.id,
                temp_data['answer']= answer_info.content,
                temp_data['good_num']=answer_info.good_num,
                temp_data['comment_num']=answer_info.comment_num,
            resp['data'].append(temp_data)
    return jsonify(resp)

@route_api.route('/question/search',methods =['POST','GET'])
def search():
    resp={'code': 200, 'msg': '传输成功', 'data':[]}
    req = request.values['keyword']
    question_list=Question.query.filter(or_(Question.topic.like('%'+req+'%'),Question.content.like('%'+req+'%'))).all()
    member_id=Member.query.filter(Member.nickname.like('%'+req+'%')).first()
    if member_id:
        question_list=Question.query.filter_by(member_id=member_id.id).all()
    if question_list:
        for item in question_list:
            # app.logger.info(item.id)
            member_info=Member.query.filter_by(id=item.member_id).first()
            answer_info=Answer.query.filter_by(question_id=item.id).first()
            temp_data={
                'question_id':item.id,
                'member_id':item.member_id,
                'nickname': member_info.nickname,
                'avatar': member_info.avatar,
                'question':item.content,
                'topic':item.topic,
                'notes':item.notes,
            }
            if answer_info:
                temp_data['answer_id']=answer_info.id,
                temp_data['answer']= answer_info.content,
                temp_data['good_num']=answer_info.good_num,
                temp_data['comment_num']=answer_info.comment_num,
            resp['data'].append(temp_data)
    return jsonify(resp)