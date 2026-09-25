/**
 * Joseph Ashirumah — Full-Stack Software Engineer Portfolio
 * Interactive frontend scripting
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavbarScroll();
  initMobileNav();
  initBackToTop();
  initTerminalCopy();
  initContactForm();
  initScrollSpy();
});

/**
 * Navbar elevation & backdrop blur on page scroll
 */
function initNavbarScroll() {
  const navbar = document.getElementById('mainNavbar');
  if (!navbar) return;

  const handleScroll = () => {
    if (window.scrollY > 30) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();
}

/**
 * Mobile navigation collapse handler
 */
function initMobileNav() {
    const toggle = document.getElementById("navToggle");
    const mobileNav = document.getElementById("mobileNav");

    if (!toggle || !mobileNav) return;

    toggle.addEventListener("click", () => {
        const isOpen = toggle.classList.toggle("is-open");

        mobileNav.classList.toggle("is-open", isOpen);

        toggle.setAttribute(
            "aria-expanded",
            String(isOpen)
        );

        toggle.setAttribute(
            "aria-label",
            isOpen
                ? "Close navigation"
                : "Open navigation"
        );
    });

    const links = mobileNav.querySelectorAll("a");

    links.forEach((link) => {
        link.addEventListener("click", () => {
            toggle.classList.remove("is-open");
            mobileNav.classList.remove("is-open");

            toggle.setAttribute("aria-expanded", "false");
            toggle.setAttribute("aria-label", "Open navigation");
        });
    });
}

/**
 * Back to top floating button
 */
function initBackToTop() {
  const backToTopBtn = document.getElementById('backToTopBtn');
  if (!backToTopBtn) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 400) {
      backToTopBtn.classList.add('visible');
    } else {
      backToTopBtn.classList.remove('visible');
    }
  }, { passive: true });

  backToTopBtn.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  });
}

/**
 * Copy terminal snippet to clipboard with visual confirmation
 */
function initTerminalCopy() {
  const copyBtn = document.getElementById('btnCopyCode');
  const codeBlock = document.getElementById('heroCodeBlock');

  if (!copyBtn || !codeBlock) return;

  copyBtn.addEventListener('click', async () => {
    try {
      const textToCopy = codeBlock.innerText;
      await navigator.clipboard.writeText(textToCopy);

      const originalHtml = copyBtn.innerHTML;
      copyBtn.innerHTML = '<i class="bi bi-check2 text-success"></i>';
      copyBtn.setAttribute('title', 'Copied to clipboard!');

      setTimeout(() => {
        copyBtn.innerHTML = originalHtml;
        copyBtn.setAttribute('title', 'Copy snippet');
      }, 2000);
    } catch (err) {
      console.warn('Clipboard copy error:', err);
    }
  });
}

/**
 * Active navigation link on scroll (ScrollSpy)
 */
function initScrollSpy() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link, .nav-link-custom, .mobile-nav-link');

  if (!sections.length || !navLinks.length) return;

  const setActive = (id) => {
    navLinks.forEach((link) => {
      const href = link.getAttribute('href') || '';
      if (href.endsWith(`#${id}`) || href === `#${id}`) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  };

  // If at top of page, activate Home
  if (window.scrollY < 200) {
    setActive('hero');
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          setActive(id);
        }
      });
    },
    { rootMargin: '-20% 0px -60% 0px' }
  );

  sections.forEach((section) => observer.observe(section));
}

/**
 * Contact form AJAX submission with inline alerts and button loading state
 */
function initContactForm() {
  const form = document.getElementById('portfolioContactForm');
  const statusAlert = document.getElementById('contactFormAlert');
  const submitBtn = document.getElementById('btnSubmitContact');

  if (!form) return;

  form.addEventListener('submit', async (e) => {
    if (window.fetch && window.FormData) {
      e.preventDefault();

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Sending...';
      }

      if (statusAlert) {
        statusAlert.className = 'd-none';
        statusAlert.innerHTML = '';
      }

      try {
        const formData = new FormData(form);
        const actionUrl = form.getAttribute('action') || '/contact/submit/';

        const response = await fetch(actionUrl, {
          method: 'POST',
          body: formData,
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json',
          },
        });

        const data = await response.json();

        if (response.ok && data.success) {
          form.reset();
          if (statusAlert) {
            statusAlert.className = 'alert alert-success d-flex align-items-center gap-2 mb-4';
            statusAlert.innerHTML = `
              <i class="bi bi-check-circle-fill fs-5 text-success"></i>
              <div>${data.message || 'Thank you! Your message has been sent.'}</div>
            `;
            statusAlert.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }
        } else {
          let errorHtml = '<i class="bi bi-exclamation-triangle-fill fs-5 text-danger me-2"></i><div>';
          if (data.errors) {
            const errorList = Object.entries(data.errors)
              .map(([field, errs]) => `<strong>${field}:</strong> ${errs.join(', ')}`)
              .join('<br>');
            errorHtml += errorList;
          } else {
            errorHtml += (data.message || 'Error sending message. Please check the fields below.');
          }
          errorHtml += '</div>';

          if (statusAlert) {
            statusAlert.className = 'alert alert-danger d-flex align-items-center gap-2 mb-4';
            statusAlert.innerHTML = errorHtml;
            statusAlert.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }
        }
      } catch (err) {
        console.error('AJAX error, submitting normally:', err);
        form.submit();
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = '<i class="bi bi-send-fill me-2"></i> Send Message';
        }
      }
    }
  });
}
