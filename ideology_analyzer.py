import pandas as pd
from collections import defaultdict
from typing import List, Tuple, Dict
import random
import os
import bottle
from bottle import Bottle, template, request, static_file

# Vercel用のアプリケーション設定
app = Bottle()

# テンプレートパスの設定
current_dir = os.path.dirname(os.path.abspath(__file__))
bottle.TEMPLATE_PATH = [current_dir]

# CSVファイルの読み込み
questions_df = pd.read_csv(os.path.join(current_dir, 'questions.csv'))
ideologies_df = pd.read_csv(os.path.join(current_dir, 'ideologies.csv'))
axes_df = pd.read_csv(os.path.join(current_dir, 'axes.csv'))

# 1軸あたりの質問数
QUESTIONS_PER_AXIS = 3

# イデオロギーの分析関数
def analyze_ideology(answers: Dict[str, List[int]]):
    result = {}
    # イデオロギーのパターンを構築
    ideology_pattern = {}
    for axis, responses in answers.items():
        # XとYのスコアを計算
        x_score = sum(3 - answer for answer in responses) / len(responses)
        y_score = sum(answer - 3 for answer in responses) / len(responses)
        
        # XとYのどちらが強いか判定
        side = 'X' if x_score >= y_score else 'Y'
        score = x_score if side == 'X' else y_score
        percentage = score / 2 * 100
        ideology_pattern[axis] = side
        
        result[axis] = (side, score, percentage)
    
    # 該当するイデオロギーを特定
    ideology_row = ideologies_df[
        (ideologies_df['AX_C'] == ideology_pattern['C']) &
        (ideologies_df['AX_D'] == ideology_pattern['D']) &
        (ideologies_df['AX_A'] == ideology_pattern['A']) &
        (ideologies_df['AX_B'] == ideology_pattern['B'])
    ].iloc[0]

    result_data = {
        "ideology_name": ideology_row['name'],
        "ideology_description": ideology_row['description1'],
        "axes_data": result
    }
    return result_data

@app.route('/')
def index():
    return template('index')

@app.route('/question')
def question():
    all_questions = []
    axis_questions = {}

    # 各軸から質問を選択
    for axis in 'ABCD':
        questions = questions_df[questions_df['Axis'] == axis].sample(n=QUESTIONS_PER_AXIS)
        axis_questions[axis] = []
        for _, question_row in questions.iterrows():
            question_data = {
                'axis': axis,
                'question': question_row['Question'],
                'option_a': question_row['X'],
                'option_b': question_row['Y']
            }
            all_questions.append(question_data)
            axis_questions[axis].append(question_data)

    # 質問をランダムに並び替え
    random.shuffle(all_questions)
    
    # 質問にIDを付与
    for i, q in enumerate(all_questions, 1):
        q['id'] = f"q_{i}"

    return template('question', questions=all_questions)

@app.route('/analyze', method='POST')
def analyze():
    # 各軸の回答を集計
    answers = defaultdict(list)
    for key, value in request.forms.items():
        if key.startswith('axis_'):  # 例: "axis_A_q_1" の形式
            axis = key.split('_')[1]
            answers[axis].append(int(value))

    result_data = analyze_ideology(answers)

    # 軸の説明を追加
    axis_descriptions = {}
    for axis in "CDAB":
        axis_row = axes_df[axes_df['name'] == axis].iloc[0]
        axis_descriptions[axis] = (axis_row['exp'], axis_row['x'], axis_row['y'])

    result_data['axis_descriptions'] = axis_descriptions
    return template('result', **result_data)

# CSSやJSなどの静的ファイルにアクセスするためのルート
@app.route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root=os.path.join(current_dir, 'static'))

# Vercelのためのエントリーポイント
application = app = app.default_app()
