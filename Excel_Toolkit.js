class Ele {
    constructor() {
        this.level1 = document.getElementById("一级列表");
        this.level2 = document.getElementById("二级列表");
        this.content = document.getElementById("内容栏");
        this.searchButton = document.getElementById("searchButton");
        this.searchInput = document.getElementById("searchInput");
    }
}
class Api {
    constructor() {
        let api = window.pywebview.api;
        this.get_level1 = api.get_level1;
        this.get_level2 = api.get_level2;
        this.get_by_menu = api.get_by_menu;
        this.get = api.get;
    }
}

class Layout {
    constructor() {
        this.level1 = ''
        this.level2 = ''
        this.api = new Api();
        this.ele = new Ele();
        this.load_level1();
    }

    load_level1() {
        this.api
            .get_level1()
            .then(level1_arr => {
                let html = '', class_name = "一级列表项 激活";
                for (let level1_item of level1_arr) {
                    html += `<div class="${class_name}" onclick="layout.level1_click(this)">${level1_item}</div>`;
                    class_name = "一级列表项";
                }
                this.ele.level1.innerHTML = html;
                this.level1 = this.ele.level1.firstElementChild.textContent;
                this.laod_level2_list()
            });
    }
    level1_click(click_ele) {
        this.ele.level1
            .childNodes
            .forEach(ele => ele.classList.remove('激活'));
        click_ele.classList.add('激活');
        this.level1 = click_ele.textContent;
        this.ele.content.innerHTML = '';
        this.laod_level2_list()
    }
    laod_level2_list() {
        this.api
            .get_level2(this.level1)
            .then(obj_list => this.load_level2(obj_list))
    }
    load_level2(obj_list) {
        let html = '';
        for (let item of obj_list) {
            html += `<div class="二级列表项" data-key="${item.level2}" onclick="layout.level2_click(this)")>
                        <div class="列表键">${item.level2}</div>
                        <div class="列表值">${item.info}</div>
                    </div>`;
        }
        this.ele.level2.innerHTML = html;
    }
    level2_click(click_ele) {
        this.ele.level2
            .childNodes
            .forEach(ele => ele.classList.remove('激活'));
        click_ele.classList.add('激活');
        this.level2 = click_ele.dataset.key;
        this.load_content();
    }
    load_content() {
        this.api
            .get_by_menu(this.level1, this.level2)
            .then(obj => {
                this.ele.content.innerHTML = obj.content;
                this.ele.content.scrollTo({ top: 0, behavior: "smooth" })
            });
    }
    search() {
        this.api
            .get(this.ele.searchInput.value)
            .then(obj_list => this.load_level2(obj_list));
        this.ele.level1.childNodes
            .forEach(ele => ele.classList.remove('激活'));
    }
}
let layout;
window.addEventListener("pywebviewready", () => {
    layout = new Layout()
})