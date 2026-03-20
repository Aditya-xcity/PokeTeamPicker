(function () {
    const loadGameForm = document.getElementById("loadGameForm");
    const loadingOverlay = document.getElementById("loadingOverlay");

    if (loadGameForm) {
        loadGameForm.addEventListener("submit", function () {
            if (loadingOverlay) {
                loadingOverlay.classList.add("active");
                loadingOverlay.setAttribute("aria-hidden", "false");
            }
        });
    }

    const teamForm = document.getElementById("teamForm");
    if (!teamForm) {
        return;
    }

    const cards = Array.from(document.querySelectorAll(".pokemon-card"));
    const checkboxes = Array.from(document.querySelectorAll(".card-check"));
    const selectedCountEl = document.getElementById("selectedCount");
    const autoBtn = document.getElementById("autoTeamBtn");

    function selectedCount() {
        return checkboxes.filter((cb) => cb.checked).length;
    }

    function syncCardStates() {
        checkboxes.forEach((cb) => {
            const card = cb.closest(".pokemon-card");
            if (!card) return;
            card.classList.toggle("selected", cb.checked);
        });

        if (selectedCountEl) {
            selectedCountEl.textContent = `${selectedCount()} / 6 selected`;
        }
    }

    cards.forEach((card) => {
        card.addEventListener("click", function (event) {
            const target = event.target;
            if (!(target instanceof HTMLElement)) return;

            if (target.closest(".cry-btn") || target.classList.contains("card-check")) {
                return;
            }

            const checkbox = card.querySelector(".card-check");
            if (!checkbox) return;

            if (!checkbox.checked && selectedCount() >= 6) {
                return;
            }

            checkbox.checked = !checkbox.checked;
            syncCardStates();
        });
    });

    checkboxes.forEach((cb) => {
        cb.addEventListener("change", function () {
            if (cb.checked && selectedCount() > 6) {
                cb.checked = false;
                alert("You can only select 6 Pokemon.");
            }
            syncCardStates();
        });
    });

    document.querySelectorAll(".cry-btn").forEach((btn) => {
        btn.addEventListener("click", function () {
            const audioId = btn.getAttribute("data-audio");
            if (!audioId) return;
            const audio = document.getElementById(audioId);
            if (!(audio instanceof HTMLAudioElement)) return;
            audio.currentTime = 0;
            audio.play();
        });
    });

    if (autoBtn) {
        autoBtn.addEventListener("click", function () {
            const ranked = cards
                .map((card) => ({
                    card,
                    profit: Number(card.getAttribute("data-profit") || 0),
                }))
                .sort((a, b) => b.profit - a.profit)
                .slice(0, 6);

            checkboxes.forEach((cb) => {
                cb.checked = false;
            });

            ranked.forEach((entry) => {
                const cb = entry.card.querySelector(".card-check");
                if (cb) {
                    cb.checked = true;
                }
            });

            syncCardStates();
        });
    }

    teamForm.addEventListener("submit", function (event) {
        if (selectedCount() !== 6) {
            event.preventDefault();
            alert("Select exactly 6 Pokemon before submitting.");
        }
    });

    syncCardStates();
})();
