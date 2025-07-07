let api, index, 一级, 二级, 内容, 一级列表, 二级列表;
fetch("Excel_Toolkit.json")
    .then((response) => response.json())
    .then((data) => {
        index = data;
        一级列表 = document.getElementById("一级列表");
        二级列表 = document.getElementById("二级列表");
        内容 = document.getElementById("内容栏");
        add_level1();
        一级 = Object.keys(index)[0];
        add_level2(一级);

    });

window.addEventListener("pywebviewready", () => {
    api = window.pywebview.api;
});
function add_level1() {
    let class_name = "一级列表项 激活"
    let html = "";
    for (let i in index) {
        html += `<div class="${class_name}">${i}</div>`;
        class_name = "一级列表项";
    }
    一级列表.innerHTML = html;
    一级列表.querySelectorAll('.一级列表项').forEach(item => {
        item.addEventListener('click', level1_click);
    });
}
function add_level2(level1) {
    let level2_arr = index[level1];
    let html = "";
    for (let i in level2_arr) {
        let key = Object.keys(level2_arr[i])[0];
        let value = level2_arr[i][key];
        html += `<div class="二级列表项" data-key="${key}">
                    <div class="列表键">${key}</div>
                    <div class="列表值">${value}</div>
                 </div>`;
    }
    二级列表.innerHTML = html;
    二级列表.querySelectorAll('.二级列表项').forEach(item => {
        item.addEventListener('click', level2_click);
    });
}
function level1_click() {
    一级列表.querySelectorAll('.一级列表项').forEach(item => {
        item.classList.remove('激活');
    });
    this.classList.add('激活');
    一级 = this.textContent;
    内容.innerHTML = "";
    add_level2(一级);
}
function level2_click() {
    二级列表.querySelectorAll('.二级列表项').forEach(item => {
        item.classList.remove('激活');
    });
    this.classList.add('激活');
    二级 = this.querySelector('.列表键').textContent
    add_insert(一级, 二级)
}
function add_insert(一级, 二级) {
    let path = `data/${一级}/${二级}.html`;
    api.get_content(path).then((html) => {
        内容.innerHTML = "";
        内容.innerHTML = html;
    });
}
