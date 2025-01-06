<!DOCTYPE html>
<html>
<head>
    <title>質問</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <h1>イデオロギー分析テスト</h1>
    <p class="description">以下の12個の質問に答えてください。それぞれの質問に対して、あなたの考えに最も近い選択肢を選んでください。</p>
    
    <form action="/analyze" method="post">
        % for i, q in enumerate(questions, 1):
        <div class="question">
            <h2>質問 {{i}}/12</h2>
            <p>{{q['question']}}</p>
            <div class="options">
                <p><strong>A:</strong> {{q['option_a']}}</p>
                <p><strong>B:</strong> {{q['option_b']}}</p>
                <div class="radio-group">
                    % for value in range(1, 6):
                    <label class="radio-label">
                        <input type="radio" name="axis_{{q['axis']}}_{{q['id']}}" value="{{value}}" required>
                        <span class="radio-text">
                            % if value == 1:
                            Aに強く賛成
                            % elif value == 2:
                            Aにやや賛成
                            % elif value == 3:
                            どちらでもない
                            % elif value == 4:
                            Bにやや賛成
                            % elif value == 5:
                            Bに強く賛成
                            % end
                        </span>
                    </label>
                    % end
                </div>
            </div>
        </div>
        % end
        <input type="submit" value="結果を見る">
    </form>
</body>
</html>