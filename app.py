import hashlib
from flask_cors import CORS
from flask import Flask, request, jsonify
import generation
from main import generate_questions  # 假设你已经修改 generate_questions 使其返回题目列表

app = Flask(__name__)
CORS(app)
@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    student_id = data.get('student_id')
    if not student_id:
        return jsonify({"error": "Missing student_id"}), 400

    student_id = student_id.encode('utf-8')
    m = hashlib.md5()
    m.update(student_id)
    generation.number = m.hexdigest()

    question_num = data.get('question_num', 5)  # 默认生成 5 道题
    rule_num = data.get('rule_num', 3)

    # 生成题目，比如生成5道题，至少使用3条规则
    try:
        question_num = int(question_num)
        rule_num = int(rule_num)
    except ValueError:
        return jsonify({"error": "question_num 和 rule_num 必须为整数"}), 400

    try:
        questions = generate_questions(question_num, rule_num)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"questions": questions})


if __name__ == '__main__':
    app.run(debug=True)
