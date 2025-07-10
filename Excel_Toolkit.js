let api, level1, level2;
let level1_arr, level2_arr;
let ele_level1, ele_level2, ele_content, ele_searchButton, ele_searchInput;



window.addEventListener("pywebviewready", () => {
    api = window.pywebview.api;
    api.get_level1().then((x) => {
        level1_arr = x;
        ele_content = document.getElementById("内容栏");
        ele_level1 = document.getElementById("一级列表");
        ele_level2 = document.getElementById("二级列表");
        ele_searchButton = document.getElementById("searchButton");
        ele_searchInput = document.getElementById("searchInput");
        load_level1(level1_arr);
        load_level2(level1_arr[0]);
        ele_searchInput.addEventListener("keyup", function (event) { if (event.key === "Enter") { search(); } });
    });
});
function load_level1(level1_arr) {
    let class_name = "一级列表项 激活";
    let html = "";
    for (let i of level1_arr) {
        html += `<div class="${class_name}">${i}</div>`;
        class_name = "一级列表项";
    }
    ele_level1.innerHTML = html;
    ele_level1.querySelectorAll(".一级列表项").forEach((item) => {
        item.addEventListener("click", level1_click);
    });
}
function load_level2(level1_key) {
    api.get_level2(level1_key).then((x) => {
        let html = "";
        for (let i of x) {
            html += `<div class="二级列表项" data-key="${i[0]}">
                    <div class="列表键">${i[0]}</div>
                    <div class="列表值">${i[1]}</div>
                 </div>`;
        }
        ele_level2.innerHTML = html;
        ele_level2.querySelectorAll(".二级列表项").forEach((item) => {
            item.addEventListener("click", level2_click);
        });
    });
}
function search() {
    api.get(ele_searchInput.value).then(x => {
        html = ""
        for (i of x) {
            html += `<div class="二级列表项" data-key="${i[1]}">
                    <div class="列表键">${i[1]}</div>
                    <div class="列表值">${i[2]}</div>
                 </div>`;
        }
        console.log(html)
        ele_level2.innerHTML = html;
        ele_level2.querySelectorAll(".二级列表项").forEach((item) => {
            item.addEventListener("click", level2_click);
        });
    })
}

function load_content(level1_key, level2_key) {
    api
        .get_by_menu(level1_key, level2_key)
        .then(x => {
            ele_content.innerHTML = "";
            ele_content.innerHTML = x[0][3];
            ele_content.scrollTo({ top: 0, behavior: "smooth" });
        })
}
function level1_click() {
    ele_level1.querySelectorAll(".一级列表项").forEach((item) => {
        item.classList.remove("激活");
    });
    this.classList.add("激活");
    level1 = this.textContent;
    ele_content.innerHTML = "";
    load_level2(level1);
}
function level2_click() {
    ele_level2.querySelectorAll(".二级列表项").forEach((item) => {
        item.classList.remove("激活");
    });
    this.classList.add("激活");
    level2 = this.querySelector(".列表键").textContent;
    load_content(level1, level2);
}