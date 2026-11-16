(() => {
    const searchForm = document.querySelector("#vehicleSearchForm");
    const queryInput = document.querySelector("#vehicleQuery");
    const categoryInput = document.querySelector("#vehicleCategory");
    const maxPriceInput = document.querySelector("#maxPrice");
    const vehicleCards = Array.from(document.querySelectorAll("[data-vehicle-card]"));
    const resultsCount = document.querySelector("#vehicleResultsCount");
    const filterEmptyState = document.querySelector("#vehicleFilterEmpty");

    const applyVehicleFilters = () => {
        const query = queryInput?.value.trim().toLocaleLowerCase() || "";
        const category = categoryInput?.value || "";
        const maxPriceValue = Number.parseFloat(maxPriceInput?.value || "");
        const maxPrice = Number.isFinite(maxPriceValue) ? maxPriceValue : Infinity;
        let visibleCount = 0;

        vehicleCards.forEach((card) => {
            const matchesQuery = `${card.dataset.name} ${card.dataset.brand} ${card.dataset.categoryName}`
                .toLocaleLowerCase()
                .includes(query);
            const matchesCategory = !category || card.dataset.category === category;
            const matchesPrice = Number(card.dataset.price) <= maxPrice;
            const isVisible = matchesQuery && matchesCategory && matchesPrice;

            card.hidden = !isVisible;
            visibleCount += Number(isVisible);
        });

        if (resultsCount) {
            resultsCount.textContent = `${visibleCount} ${visibleCount === 1 ? "ride" : "rides"} available`;
        }
        if (filterEmptyState) {
            filterEmptyState.hidden = visibleCount > 0;
        }
    };

    if (searchForm) {
        const parameters = new URLSearchParams(window.location.search);
        queryInput.value = parameters.get("q") || "";
        categoryInput.value = parameters.get("category") || "";
        maxPriceInput.value = parameters.get("max_price") || "";

        searchForm.addEventListener("submit", (event) => {
            event.preventDefault();
            applyVehicleFilters();
            document.querySelector("#vehicles")?.scrollIntoView({ behavior: "smooth" });
        });
        searchForm.addEventListener("input", applyVehicleFilters);
        searchForm.addEventListener("change", applyVehicleFilters);
        applyVehicleFilters();
    }

    document.querySelector("#clearVehicleFilters")?.addEventListener("click", () => {
        searchForm?.reset();
        applyVehicleFilters();
        window.history.replaceState({}, "", `${window.location.pathname}#vehicles`);
        queryInput?.focus();
    });

    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const revealGroups = [
        {
            selector: ".benefits-heading, .vehicles-section .section-intro, .destinations-section .section-intro, .cta-content, .main-footer .container",
            stagger: 0,
        },
        { selector: ".benefit-item", stagger: 110 },
        { selector: ".vehicle-card", stagger: 100 },
        { selector: ".destination-card", stagger: 90 },
    ];

    if (reducedMotion) {
        return;
    }

    const gsap = window.gsap;
    const scrollTrigger = window.ScrollTrigger;

    if (gsap && scrollTrigger) {
        gsap.registerPlugin(scrollTrigger);

        const intro = gsap.timeline({ defaults: { ease: "power3.out" } });
        intro.fromTo("main", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.55, ease: "power1.out" });
        intro.fromTo(".hero-tag", { autoAlpha: 0, y: 16 }, { autoAlpha: 1, y: 0, duration: 0.5 }, 0.08);
        intro.fromTo(".hero-content h1", { autoAlpha: 0, y: 22 }, { autoAlpha: 1, y: 0, duration: 0.7 }, 0.18);
        intro.fromTo(".hero-content p", { autoAlpha: 0, y: 18 }, { autoAlpha: 1, y: 0, duration: 0.6 }, 0.32);
        intro.fromTo(".hero-buttons", { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.55 }, 0.44);
        intro.fromTo(".booking-card", { autoAlpha: 0, x: 22 }, { autoAlpha: 1, x: 0, duration: 0.7 }, 0.25);

        revealGroups.forEach(({ selector, stagger }) => {
            const elements = gsap.utils.toArray(selector);
            if (!elements.length) {
                return;
            }

            const trigger = elements[0].closest(
                ".benefits-section, .vehicles-section, .destinations-section, .cta-section, .main-footer"
            ) || elements[0];

            gsap.fromTo(
                elements,
                { autoAlpha: 0, y: 24 },
                {
                    autoAlpha: 1,
                    y: 0,
                    duration: 0.7,
                    ease: "power3.out",
                    stagger: stagger / 1000,
                    scrollTrigger: {
                        trigger,
                        start: "top 84%",
                        once: true,
                    },
                }
            );
        });

        gsap.utils.toArray(".vehicle-image img, .destination-card img").forEach((image) => {
            const card = image.closest(".vehicle-card, .destination-card");
            gsap.fromTo(
                image,
                { autoAlpha: 0.78, scale: 1.045 },
                {
                    autoAlpha: 1,
                    scale: 1,
                    duration: 0.9,
                    ease: "power2.out",
                    scrollTrigger: {
                        trigger: card,
                        start: "top 88%",
                        once: true,
                    },
                }
            );
        });

        window.addEventListener("load", () => scrollTrigger.refresh(), { once: true });
        return;
    }

    if (!("IntersectionObserver" in window)) {
        return;
    }

    const observer = new IntersectionObserver((entries, activeObserver) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("is-visible");
                activeObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12 });

    revealGroups.forEach(({ selector, stagger }) => {
        document.querySelectorAll(selector).forEach((element, index) => {
            element.classList.add("motion-reveal");
            element.style.setProperty("--motion-delay", `${Math.min(index * stagger, 360)}ms`);
            observer.observe(element);
        });
    });

    document.querySelectorAll(".hero-tag, .hero-content h1, .hero-content p, .hero-buttons, .booking-card")
        .forEach((element, index) => {
            element.classList.add("motion-reveal");
            element.style.setProperty("--motion-delay", `${index * 100}ms`);
            observer.observe(element);
        });
})();
