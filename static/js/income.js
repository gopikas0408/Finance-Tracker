// ======================================
// DELETE MODAL
// ======================================

const deleteModal = document.getElementById("deleteModal");

if (deleteModal) {

    deleteModal.addEventListener("show.bs.modal", function (event) {

        const button = event.relatedTarget;

        const url = button.getAttribute("data-url");

        document.getElementById("deleteLink").href = url;

    });

}

// ======================================
// SEARCH (Enter Key)
// ======================================

const searchInput = document.querySelector("input[name='search']");

if (searchInput) {

    searchInput.addEventListener("keypress", function (e) {

        if (e.key === "Enter") {

            this.form.submit();

        }

    });

}

// ======================================
// AUTO HIDE DJANGO MESSAGE
// ======================================

setTimeout(function () {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (item) {

        item.style.transition = ".4s";

        item.style.opacity = "0";

        setTimeout(() => {

            item.remove();

        }, 400);

    });

}, 3000);

// ======================================
// TABLE ROW HOVER
// ======================================

document.querySelectorAll(".dashboard-table tbody tr").forEach(function (row) {

    row.addEventListener("mouseenter", function () {

        row.style.transition = ".3s";

    });

});

// ======================================
// BUTTON LOADING
// ======================================

document.querySelectorAll("form").forEach(function (form) {

    form.addEventListener("submit", function () {

        const btn = form.querySelector("button[type='submit']");

        if (btn) {

            btn.disabled = true;

            btn.innerHTML = '<i class="bi bi-arrow-repeat spin"></i> Please Wait...';

        }

    });

});