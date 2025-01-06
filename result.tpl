<!DOCTYPE html>
<html>
<head>
    <title>分析結果</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <h1>あなたのイデオロギー分析結果</h1>
    
    <div class="result">
        <h2>あなたのイデオロギーは「{{ ideology_name }}」です</h2>
        <p>{{ ideology_description }}</p>
    </div>

    <h2>各軸の詳細分析</h2>
    % for axis, data in axes_data.items():
        <div class="result">
            <h3>{{axis_descriptions[axis][0]}}</h3>
            <p>あなたの傾向: <strong>{{data[0]}} ({{data[2]}}%)</strong></p>
            <p>この軸について：</p>
            <ul>
                <li><strong>X側の特徴：</strong> {{axis_descriptions[axis][1]}}</li>
                <li><strong>Y側の特徴：</strong> {{axis_descriptions[axis][2]}}</li>
            </ul>
        </div>
    % end

    <a href="/">もう一度テストを受ける</a>
</body>
</html>
