# This file perfroms Social Guru
# Given a user id, find the 5 most recent feedback they posted
from flask import Blueprint, jsonify, request
from .models.productcomment import ProductComment

bp = Blueprint('usercomment', __name__, url_prefix='/usercomments')

@bp.route('/<int:userid>', methods=['GET'])
def get_user_comments(userid):
    # 调用 ProductComment 类中一个方法 get_comments_by_user(userid)
    # 该方法根据用户ID获取最新的5条评论
    comments = ProductComment.get_comments_by_user(userid)
    # 将查询结果转换为 JSON 格式并返回
    return jsonify(comments)

