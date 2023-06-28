function generateChoice(slug, answers) {

    answers = answers.replace(/'/g, '"');
    answers = answers.replace(/\\\\/g, '\\');
    var answers_obj = JSON.parse(answers);

    if (Object.keys(answers_obj).length == 0) {
        return;
    }
    var item_div = document.getElementById("item-" + slug.replace(/\//g, '-'));
    item_div.className = "item";


    var canvas = document.createElement("canvas");
    canvas.id = `canvas-${slug}-chart`;

    document.getElementById(slug).appendChild(item_div);
    item_div.appendChild(canvas);

    var barColors = [
        "#b91d47",
        "#00aba9",
        "#2b5797",
        "#e8c3b9",
        "#1e7145"
    ];
    var x = Object.keys(answers_obj)
    var y = [];
    for (var key in answers_obj){
        y.push(answers_obj[key])
    }
    generateChart(slug, y, x, "pie", barColors);
}


function getWrongLines(answer, correct) {
    var answer_lines = answer.split("\n");
    var correct_lines = correct.split("\n");
    var wrong_lines = [];
    if (correct.length == 0)
        return [];
    for (var i = 0; i < answer_lines.length; i++) {
        if (correct_lines[i] != answer_lines[i])
            wrong_lines.push(i + 1);
    }
    return wrong_lines;
}

function generateParson(slug, answers, correct) {

    answers = answers.replace(/'/g, '"');
    answers = answers.replace(/\\\\/g, '\\');


    var answers_obj = JSON.parse(answers);
    
    if (Object.keys(answers_obj).length == 0) {
        return;
    }
    var item_div = document.getElementById("item-" + slug.replace(/\//g, '-'));
    item_div.className = "item";

    var canvas = document.createElement("canvas");
    canvas.id = `canvas-${slug}-chart`;

    answer_div = document.createElement("div");
    answer_div.className = "parson-answers";

    document.getElementById(slug).appendChild(item_div);
    item_div.appendChild(canvas);
    item_div.appendChild(answer_div);

    var colors = [];
    var x_values = [];

    for (var answer in answers_obj) {
        var color = `#${Math.floor(Math.random() * 16777215).toString(16)}`;
        colors.push(color);
        x_values.push(answers_obj[answer]);

        var lines = getWrongLines(answer, correct);
        var code_div = document.createElement("div");
        var pre = document.createElement("pre");
        var code = document.createElement("code");

        code.className = "language-python";
        code.innerHTML = answer;
        pre.setAttribute("data-line", lines.join(","));
        code_div.style.backgroundColor = color;
        code_div.className = "parson-code";

        answer_div.appendChild(code_div);
        code_div.appendChild(pre);
        pre.appendChild(code);


        Prism.highlightElement(code);

    }
    labels = [];
    //create label list from A until length of x_values in one line
    for (var i = 0; i < x_values.length; i++) {
        labels.push(String.fromCharCode(65 + i));
    }

    generateChart(slug, x_values, labels, "bar", colors);

}

function generateChart(name, data, labels, type, colors) {

    Chart.defaults.global.legend.display = false;
    if (type == "pie")
        scales = {};
    else
        scales = {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        };

    new Chart(`canvas-${name}-chart`, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                backgroundColor: colors,
                data: data
            }]
        },
        options: {
            title: {
                display: true,
                text: name
            },
            responsive: false,
            maintainAspectRatio: false,
            scales: scales,

        }
    });

}

function generateWordCloud(slug, answers){

    answers = answers.replace(/'/g, '"');
    answers = answers.replace(/\\\\/g, '\\');
    var answers_obj = JSON.parse(answers);
    if (Object.keys(answers_obj).length == 0) {
        return;
    }
    var item_div = document.getElementById("item-" + slug.replace(/\//g, '-'));
    document.getElementById(slug).appendChild(item_div);
    var canvas = document.createElement("canvas");
    canvas.id = `canvas-${slug}`
    item_div.appendChild(canvas);    
    WordCloud(document.getElementById(`canvas-${slug}`), { list: answers_obj} );



}
