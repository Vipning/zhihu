from web.controllers.api import route_api
from flask import request,jsonify
from application import app,db
import requests,json
from common.models.member.Member import Member
from common.libs.Helper import getCurrentDate
from common.libs.member.MemberService import MemberService

@route_api.route('/member/login',methods =['POST','GET'])
def login():
    resp={'code':200,'msg':'操作成功','data':{}}#返回值

    req=request.values#前台的数据
    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''

    code =req['code'] if 'code' in req else ''
    if not code or len(code)<1:
        resp['code']=-1
        resp['msg']='需要code'
        return jsonify(resp)
    openid=MemberService.getWeChatOpenId(code)
    #判断用户是否已经注册
    member_info=Member.query.filter_by(openid=openid).first()
    resp['msg'] = '已经注册'
    if not member_info:
        model_member = Member()
        model_member.openid=openid
        model_member.nickname = nickname
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = MemberService.geneSalt()
        model_member.updated_time = model_member.created_time = getCurrentDate()
        db.session.add(model_member)
        db.session.commit()
        member_info =model_member
        resp['msg']='注册成功'

    member_info = Member.query.filter_by(id=member_info.id).first()
    resp['code'] = 200
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}
    return jsonify(resp)

@route_api.route('/member/check-reg',methods =['POST','GET'])
def checkReg():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}  # 返回值
    req = request.values  # 前台的数据
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        return jsonify(resp)
    openid = MemberService.getWeChatOpenId(code)
    member_info = Member.query.filter_by(openid=openid).first()
    if not member_info:
        resp['code']=-1
        resp['msg']='未注册'
        return jsonify(resp)

    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data']={'token':token}#返回给前端
    return jsonify(resp)