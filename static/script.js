document.addEventListener('DOMContentLoaded', () => {

    // ---- Hamburger menu ----
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('nav-links');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            const expanded = hamburger.getAttribute('aria-expanded') === 'true' || false;
            hamburger.setAttribute('aria-expanded', !expanded);
            hamburger.classList.toggle('active');
            navLinks.classList.toggle('show');
        });

        // Close menu when a link is clicked
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navLinks.classList.remove('show');
                hamburger.setAttribute('aria-expanded', 'false');
            });
        });
    }

    // ---- Flash message auto-dismiss ----
    document.querySelectorAll('.flash-close').forEach(btn => {
        btn.addEventListener('click', () => {
            const msg = btn.closest('.flash-message');
            if (msg) msg.remove();
        });
    });

    // Auto-hide flash messages after 4 seconds
    setTimeout(() => {
        document.querySelectorAll('.flash-message').forEach(msg => {
            msg.style.transition = 'opacity 0.5s ease';
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 500);
        });
    }, 4000);

    // ---- Menu filter (accessible tabs) ----
    const tabs = document.querySelectorAll('.tab');
    const menuItems = document.querySelectorAll('.menu-item');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Deactivate all tabs
            tabs.forEach(t => {
                t.classList.remove('active');
                t.setAttribute('aria-pressed', 'false');
            });
            // Activate clicked tab
            tab.classList.add('active');
            tab.setAttribute('aria-pressed', 'true');

            const filter = tab.getAttribute('data-filter');

            menuItems.forEach(item => {
                const category = item.getAttribute('data-category');
                if (filter === 'all' || category === filter) {
                    item.style.display = 'block';
                    // Restart animation
                    item.style.animation = 'none';
                    item.offsetHeight; // force reflow
                    item.style.animation = 'fadeInUp 0.6s ease forwards';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });

    // ---- About text reveal on scroll (Intersection Observer) ----
    const aboutSection = document.querySelector('.about-section');
    const aboutText = document.querySelector('.about-text');

    if (aboutSection && aboutText) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    aboutText.classList.add('revealed');
                    observer.unobserve(aboutSection); // only once
                }
            });
        }, { threshold: 0.3 });

        observer.observe(aboutSection);
    }

    // ---- Back to top button ----
    const backToTop = document.getElementById('back-to-top');
    if (backToTop) {
        const toggleVisibility = () => {
            if (window.scrollY > 300) backToTop.classList.add('show');
            else backToTop.classList.remove('show');
        };

        window.addEventListener('scroll', toggleVisibility, { passive: true });
        // initial check
        toggleVisibility();

        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
            backToTop.blur();
        });

        backToTop.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                backToTop.click();
            }
        });
    }

});