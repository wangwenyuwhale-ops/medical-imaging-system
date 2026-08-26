# main.py
from flask import Flask, request, jsonify
from app.models.database import db, Patient, Study
from app.services.dicom_service import DicomValidationEngine
import os

app = Flask(__name__)
# 使用 SQLite 作为本地测试数据库，轻量快捷
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medical_qa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'test_data/uploads'

db.init_app(app)
validator = DicomValidationEngine()

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/api/dicom/upload', methods=['POST'])
def upload_dicom():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 保存文件
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # 调用验证引擎
    validation_result = validator.validate_and_extract(file_path)
    
    if validation_result["status"] == "FAIL":
        # 故意不删除错误文件，留作 QA 缺陷调查 (Defect Investigation) 的证据
        return jsonify(validation_result), 400
        
    # 如果验证通过，存入数据库 (模拟业务逻辑)
    metadata = validation_result["metadata"]
    try:
        # 检查患者是否存在，不存在则创建
        patient = Patient.query.get(metadata['PatientID'])
        if not patient:
            patient = Patient(
                patient_id=metadata['PatientID'],
                patient_name=metadata['PatientName']
            )
            db.session.add(patient)
            
        # 检查 Study 是否存在，不存在则创建
        study = Study.query.get(metadata['StudyInstanceUID'])
        if not study:
            study = Study(
                study_uid=metadata['StudyInstanceUID'],
                patient_id=metadata['PatientID'],
                modality=metadata['Modality']
            )
            db.session.add(study)
            
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        validation_result["status"] = "FAIL"
        validation_result["error_reason"] = f"Database error: {str(e)}"
        return jsonify(validation_result), 500

    return jsonify(validation_result), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 初始化数据库表
    app.run(debug=True, port=5000)