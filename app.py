import hashlib
from flask_cors import CORS
from flask import Flask, request, jsonify
import generation
from main import generate_questions  # 假设你已经修改 generate_questions 使其返回题目列表

app = Flask(__name__)
CORS(app)

DEFAULT_QUESTION_NUM = 5
DEFAULT_RULE_NUM = 3
@app.route('/generate', methods=['POST'])
def generate():
    global DEFAULT_QUESTION_NUM, DEFAULT_RULE_NUM
    data = request.get_json()
    secret = data.get('secret_key')
    if secret:
        if secret != 'admin':
            return jsonify({"error": "错误的Secret Key"}), 400
        try:
            question_num = int(data.get('question_num', 5))
            rule_num = int(data.get('rule_num', 3))
        except ValueError:
            return jsonify({"error": "question_num 和 rule_num 必须为整数"}), 400

        # 更新全局默认参数，后续学生模式将采用这些参数生成题目
        DEFAULT_QUESTION_NUM = question_num
        DEFAULT_RULE_NUM = rule_num

        return jsonify({"message": f"参数更新成功：题目数量={question_num}, 最少使用规则数={rule_num}"})
    else:
        # 学生模式：要求提供 student_id
        student_id = data.get('student_id')
        if not student_id:
            return jsonify({"error": "Missing student_id"}), 400

        student_id = student_id.encode('utf-8')
        m = hashlib.md5()
        m.update(student_id)
        generation.number = m.hexdigest()

        # 使用全局参数（老师更新的参数或默认值）
        question_num = DEFAULT_QUESTION_NUM
        rule_num = DEFAULT_RULE_NUM

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
