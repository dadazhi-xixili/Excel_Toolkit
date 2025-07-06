let data = {};
let api = {};
let level_1 = [];
let level_2 = {};
let level_1_div = {};
function add_level_1() {
    const level_1_div = document.getElementById('categoryList');
    const fragment = document.createDocumentFragment();
    let n = 0
    level_1.forEach(i => {
        const but = document.createElement('button');
        but.className = n ? 'category-item' : 'category-item active'; n++;
        but.textContent = i;
        but.addEventListener('click', function () {
            const siblings = level_1_div.querySelectorAll('.category-item');
            siblings.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            api.get_level_2(this.textContent).then(r => { level_2 = r; add_level_2(); });
        });
        fragment.appendChild(but);
    });
    level_1_div.appendChild(fragment);
}
function add_level_2() {
    const level_2_ul = document.getElementById('functionList');
    const fragment = document.createDocumentFragment();
    for (const k in level_2) {
        const html = `<li class="function-item"><div class="function-name">${k}</div><div class="function-desc">${level_2[k]}</div></li>`;
        const li = new DOMParser().parseFromString(html, 'text/html').body.firstChild;
        //此处添加level_2事件 控制内容
        fragment.appendChild(li);
    }
    level_2_ul.innerHTML = ''; level_2_ul.appendChild(fragment);
}

document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('pywebviewready', function () {
        api = window.pywebview.api;
        api.get_data().then(r => { data = r; });
        api.get_level_1()
            .then(r => { level_1 = r; add_level_1(); return api.get_level_2(level_1[0]) })
            .then(r => { level_2 = r; add_level_2(); });
    });
});