// Main JavaScript utilities for Esoterica Platform

console.log('✨ Esoterica Platform loaded');

// Utility: Smooth scroll to element
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Utility: Format node ID for display (replace underscores with spaces)
function formatNodeId(id) {
    return id.replace(/_/g, ' ');
}

// Utility: Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Utility: Show loading indicator
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<p class="loading" style="text-align: center; color: #888;">Loading...</p>';
    }
}

// Utility: Show error message
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<p style="text-align: center; color: #ff4444;">${message}</p>`;
    }
}

// Add fade-in animation to cards when they enter viewport
function observeCards() {
    const cards = document.querySelectorAll('.card');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';

                setTimeout(() => {
                    entry.target.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);

                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    cards.forEach(card => observer.observe(card));
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    // Observe cards for fade-in animation
    observeCards();

    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl+K or Cmd+K to focus search (if on search page)
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.getElementById('search-input');
            if (searchInput) {
                searchInput.focus();
            } else {
                // Navigate to search page
                window.location.href = '/search';
            }
        }

        // Escape to clear search
        if (e.key === 'Escape') {
            const searchInput = document.getElementById('search-input');
            if (searchInput && searchInput === document.activeElement) {
                searchInput.value = '';
                searchInput.dispatchEvent(new Event('input'));
            }
        }
    });

    // Add "Back to top" button for long pages
    const createBackToTop = () => {
        const button = document.createElement('button');
        button.innerHTML = '↑';
        button.className = 'btn';
        button.style.cssText = `
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: none;
            z-index: 1000;
            font-size: 1.5rem;
            padding: 0;
        `;

        button.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        document.body.appendChild(button);

        // Show/hide based on scroll position
        window.addEventListener('scroll', () => {
            if (window.scrollY > 500) {
                button.style.display = 'block';
            } else {
                button.style.display = 'none';
            }
        });
    };

    createBackToTop();

    // Console art
    console.log(`
    ✧═══════════════════════════════════════════✧

         🌟 ESOTERICA CONSTELLATION PLATFORM 🌟

         Consciousness Technology Web Interface

         Every symbol = consciousness invocation
         Hidden in plain sight. Now mapped.

    ✧═══════════════════════════════════════════✧
    `);
});

// Export utilities for use in other scripts
window.EsotericaUtils = {
    smoothScrollTo,
    formatNodeId,
    debounce,
    showLoading,
    showError
};
