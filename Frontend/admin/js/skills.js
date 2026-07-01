// Predefined icon list for the visual picker
const ICON_LIST = [
    { class: "fa-brands fa-python", label: "Python" },
    { class: "fa-brands fa-js", label: "JavaScript" },
    { class: "fa-brands fa-html5", label: "HTML5" },
    { class: "fa-brands fa-css3-alt", label: "CSS3" },
    { class: "fa-brands fa-react", label: "React" },
    { class: "fa-brands fa-vuejs", label: "Vue.js" },
    { class: "fa-brands fa-angular", label: "Angular" },
    { class: "fa-brands fa-node-js", label: "Node.js" },
    { class: "fa-brands fa-php", label: "PHP" },
    { class: "fa-brands fa-laravel", label: "Laravel" },
    { class: "fa-brands fa-java", label: "Java" },
    { class: "fa-brands fa-bootstrap", label: "Bootstrap" },
    { class: "fa-brands fa-sass", label: "Sass" },
    { class: "fa-brands fa-git-alt", label: "Git" },
    { class: "fa-brands fa-github", label: "GitHub" },
    { class: "fa-brands fa-docker", label: "Docker" },
    { class: "fa-brands fa-aws", label: "AWS" },
    { class: "fa-brands fa-linux", label: "Linux" },
    { class: "fa-brands fa-windows", label: "Windows" },
    { class: "fa-brands fa-apple", label: "Apple" },
    { class: "fa-brands fa-android", label: "Android" },
    { class: "fa-brands fa-figma", label: "Figma" },
    { class: "fa-brands fa-npm", label: "NPM" },
    { class: "fa-brands fa-wordpress", label: "WordPress" },
    { class: "fa-solid fa-database", label: "Database" },
    { class: "fa-solid fa-server", label: "Server" },
    { class: "fa-solid fa-code", label: "Code" },
    { class: "fa-solid fa-terminal", label: "Terminal" },
    { class: "fa-solid fa-bug", label: "Debug" },
    { class: "fa-solid fa-gears", label: "Settings" },
    { class: "fa-solid fa-cloud", label: "Cloud" },
    { class: "fa-solid fa-mobile-screen", label: "Mobile" },
    { class: "fa-solid fa-desktop", label: "Desktop" },
    { class: "fa-solid fa-chart-line", label: "Analytics" },
    { class: "fa-solid fa-shield-halved", label: "Security" },
    { class: "fa-solid fa-lock", label: "Lock" },
    { class: "fa-solid fa-fire", label: "Firebase" },
    { class: "fa-solid fa-leaf", label: "Leaf" },
    { class: "fa-solid fa-robot", label: "AI/ML" },
    { class: "fa-solid fa-microchip", label: "Chip" },
    { class: "fa-solid fa-palette", label: "Design" },
    { class: "fa-solid fa-pen-ruler", label: "UI/UX" },
    { class: "fa-solid fa-wand-magic-sparkles", label: "Magic" },
    { class: "fa-solid fa-cube", label: "3D" },
    { class: "fa-solid fa-bolt", label: "Fast" },
    { class: "fa-solid fa-brain", label: "Brain" },
    { class: "fa-solid fa-diagram-project", label: "Flow" },
    { class: "fa-solid fa-flask", label: "Flask" },
];

document.addEventListener("DOMContentLoaded", function () {
    const formSkill = document.getElementById("form-skill");
    const skillsGridContainer = document.getElementById("skills-grid-container");
    const skillIdInput = document.getElementById("skill-id");
    const namaSkillInput = document.getElementById("nama_skill");
    const kategoriInput = document.getElementById("kategori");
    const formTitle = document.getElementById("form-title");
    const btnCancel = document.getElementById("btn-cancel");
    const iconPickerGrid = document.getElementById("icon-picker-grid");
    const selectedPreview = document.getElementById("selected-icon-preview");
    const previewIcon = document.getElementById("preview-icon");
    const previewLabel = document.getElementById("preview-label");
    const iconSearch = document.getElementById("icon-search");

    // Build the icon picker grid
    buildIconPicker();

    // Search/filter icons
    iconSearch.addEventListener("input", function () {
        const query = this.value.toLowerCase().trim();
        const items = iconPickerGrid.querySelectorAll(".icon-option");
        let visibleCount = 0;

        // Remove existing "no results" message
        const existingMsg = iconPickerGrid.querySelector(".icon-no-results");
        if (existingMsg) existingMsg.remove();

        items.forEach(item => {
            const label = item.querySelector("span").textContent.toLowerCase();
            const iconClass = item.getAttribute("data-icon-class").toLowerCase();
            const match = !query || label.includes(query) || iconClass.includes(query);
            item.style.display = match ? "" : "none";
            if (match) visibleCount++;
        });

        if (visibleCount === 0 && query) {
            const msg = document.createElement("div");
            msg.className = "icon-no-results";
            msg.textContent = `Tidak ada icon yang cocok dengan "${this.value}"`;
            iconPickerGrid.appendChild(msg);
        }
    });

    loadSkills();

    function buildIconPicker() {
        iconPickerGrid.innerHTML = "";
        ICON_LIST.forEach(icon => {
            const div = document.createElement("div");
            div.className = "icon-option";
            div.setAttribute("data-icon-class", icon.class);
            div.innerHTML = `<i class="${icon.class}"></i><span>${icon.label}</span>`;
            div.addEventListener("click", () => selectIcon(icon.class, icon.label, div));
            iconPickerGrid.appendChild(div);
        });
    }

    function selectIcon(iconClass, label, element) {
        // Remove previous selection
        document.querySelectorAll(".icon-option.selected").forEach(el => el.classList.remove("selected"));
        // Mark selected
        element.classList.add("selected");
        // Update hidden input
        kategoriInput.value = iconClass;
        // Show preview
        selectedPreview.style.display = "flex";
        previewIcon.className = iconClass;
        previewLabel.textContent = label;
    }

    function clearIconSelection() {
        document.querySelectorAll(".icon-option.selected").forEach(el => el.classList.remove("selected"));
        kategoriInput.value = "";
        selectedPreview.style.display = "none";
    }

    function highlightSelectedIcon(iconClass) {
        document.querySelectorAll(".icon-option.selected").forEach(el => el.classList.remove("selected"));
        const match = document.querySelector(`.icon-option[data-icon-class="${iconClass}"]`);
        if (match) {
            match.classList.add("selected");
            const iconData = ICON_LIST.find(i => i.class === iconClass);
            selectedPreview.style.display = "flex";
            previewIcon.className = iconClass;
            previewLabel.textContent = iconData ? iconData.label : iconClass;
        }
    }

    // 1. GET DATA & RENDER
    function loadSkills() {
        fetch('/admin/api/skills')
            .then(res => res.json())
            .then(data => {
                skillsGridContainer.innerHTML = "";
                if (!data || data.length === 0) {
                    skillsGridContainer.innerHTML = `<p style="color: var(--text-muted); padding: 10px;">Belum ada data skill.</p>`;
                    return;
                }
                
                data.forEach(skill => {
                    const id = skill.id;
                    const nama = skill.nama_skill || "";
                    const iconClass = skill.kategori || "";

                    const box = document.createElement("div");
                    box.style.cssText = "background: #fff; border: 1px solid #ede9fe; border-radius: 16px; width: 140px; padding: 20px; text-align: center; display: flex; flex-direction: column; align-items: center; box-shadow: 0 4px 15px rgba(168,85,247,0.06); transition: all 0.3s ease;";
                    
                    box.innerHTML = `
                        <div style="font-size: 36px; margin-bottom: 12px; height: 50px; display: flex; align-items: center; background: linear-gradient(135deg, #a855f7, #f472b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                            <i class="${iconClass}"></i>
                        </div>
                        <h4 style="font-weight: 700; font-size: 14px; margin-bottom: 15px; color: #1e1b2e;">${nama}</h4>
                        
                        <div style="display: flex; gap: 6px;">
                            <button class="btn-edit" data-id="${id}" data-nama="${nama}" data-icon="${iconClass}" style="background: linear-gradient(135deg, #a855f7, #c084fc); border: none; color: #fff; padding: 5px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; cursor: pointer;"><i class="fas fa-edit"></i></button>
                            <button class="btn-delete" data-id="${id}" style="background: linear-gradient(135deg, #f472b6, #ec4899); border: none; color: #fff; padding: 5px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; cursor: pointer;"><i class="fas fa-trash"></i></button>
                        </div>
                    `;
                    skillsGridContainer.appendChild(box);
                });

                initActionButtons();
            })
            .catch(err => {
                console.error("Gagal memuat skills:", err);
                skillsGridContainer.innerHTML = `<p style="color: #f472b6; padding: 10px;">Gagal memuat data skills.</p>`;
            });
    }

    // 2. EDIT & DELETE
    function initActionButtons() {
        document.querySelectorAll(".btn-edit").forEach(btn => {
            btn.addEventListener("click", function () {
                formTitle.innerText = "Ubah Data Skill";
                skillIdInput.value = this.getAttribute("data-id");
                namaSkillInput.value = this.getAttribute("data-nama");
                const iconClass = this.getAttribute("data-icon");
                kategoriInput.value = iconClass;
                highlightSelectedIcon(iconClass);
                btnCancel.style.display = "inline-block";
                // Scroll to form
                document.querySelector(".skills-manager-container").scrollIntoView({ behavior: "smooth" });
            });
        });

        document.querySelectorAll(".btn-delete").forEach(btn => {
            btn.addEventListener("click", function () {
                const id = this.getAttribute("data-id");
                if (confirm("Apakah Anda yakin ingin menghapus skill ini?")) {
                    fetch(`/admin/api/skills/${id}`, { method: "DELETE" })
                        .then(res => res.json())
                        .then(result => {
                            if (result.success) {
                                loadSkills();
                            } else {
                                alert("Gagal menghapus: " + (result.message || "Unknown error"));
                            }
                        })
                        .catch(err => {
                            console.error(err);
                            alert("Terjadi kesalahan koneksi saat menghapus.");
                        });
                }
            });
        });
    }

    // 3. SAVE (POST / PUT)
    formSkill.addEventListener("submit", function (e) {
        e.preventDefault();

        if (!kategoriInput.value) {
            alert("Silakan pilih icon untuk skill ini.");
            return;
        }

        const id = skillIdInput.value;
        const payload = {
            nama_skill: namaSkillInput.value,
            kategori: kategoriInput.value
        };

        const url = id ? `/admin/api/skills/${id}` : '/admin/api/skills';
        const method = id ? "PUT" : "POST";

        fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(result => {
            if (result.success) {
                alert(id ? "Skill berhasil diperbarui!" : "Skill baru berhasil ditambahkan!");
                resetForm();
                loadSkills();
            } else {
                alert("Gagal menyimpan: " + (result.message || "Unknown error"));
            }
        })
        .catch(err => {
            console.error(err);
            alert("Terjadi kesalahan koneksi saat menyimpan.");
        });
    });

    btnCancel.addEventListener("click", resetForm);

    function resetForm() {
        formTitle.innerText = "Tambah / Edit Skill";
        skillIdInput.value = "";
        formSkill.reset();
        clearIconSelection();
        btnCancel.style.display = "none";
        // Reset search
        iconSearch.value = "";
        iconPickerGrid.querySelectorAll(".icon-option").forEach(el => el.style.display = "");
        const msg = iconPickerGrid.querySelector(".icon-no-results");
        if (msg) msg.remove();
    }
});
