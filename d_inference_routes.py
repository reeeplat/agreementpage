# 📁 routes/d_inference_routes.py

from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from models.model import MongoDBClient

# 블루프린트 생성
d_inference_bp = Blueprint("d_inference", __name__)  

# MongoDB 클라이언트 연결
mongo = MongoDBClient().db

@d_inference_bp.route("/api/inference-results/<string:result_id>/opinion", methods=["PUT"])
def update_doctor_opinion(result_id):
    """
    특정 진단 결과에 대한 의사 의견을 업데이트하는 API 엔드포인트.
    result_id를 URL 경로 변수로부터 직접 받아옵니다.
    """
    
    # 요청 본문에서 데이터 추출
    data = request.get_json()
    opinion = data.get("opinion")
    doctor_id = data.get("doctor_id")

    # 필수 필드가 누락되었는지 확인
    if not all([opinion, doctor_id]):
        return jsonify({"error": "Missing fields"}), 400

    try:
        # ObjectId로 변환 가능한지 확인 (오류 방지)
        object_id = ObjectId(result_id)
    except Exception:
        return jsonify({"error": "Invalid result_id format"}), 400

    # MongoDB에서 해당 진단 결과 찾기
    target = mongo["inference_results"].find_one({"_id": object_id})
    if not target:
        return jsonify({"error": "해당 결과 없음"}), 404

    # 진단 결과 문서 업데이트
    mongo["inference_results"].update_one(
        {"_id": object_id},
        {"$set": {
            "doctor_opinion": opinion,
            "doctor_id": doctor_id,
            "opinion_datetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }}
    )

    return jsonify({"message": "MongoDB에 의견 저장 완료"}), 200


