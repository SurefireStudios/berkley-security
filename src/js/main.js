(function() {
  'use strict';

  const BerkleySecurity = {
    init() {
      this.initMobileMenu();
      this.initScrollEffects();
      this.initTestimonials();
      this.initFormValidation();
      this.initSmoothScroll();
    },

    initMobileMenu() {
      const menuBtn = document.getElementById('menu-btn');
      const mobileMenu = document.getElementById('mobile-menu');
      const menuOverlay = document.getElementById('menu-overlay');
      const closeMenu = document.getElementById('close-menu');

      if (!menuBtn || !mobileMenu) return;

      menuBtn.addEventListener('click', () => {
        mobileMenu.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
      });

      const closeMobileMenu = () => {
        mobileMenu.classList.add('hidden');
        document.body.style.overflow = '';
      };

      if (closeMenu) closeMenu.addEventListener('click', closeMobileMenu);
      if (menuOverlay) menuOverlay.addEventListener('click', closeMobileMenu);

      mobileMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', closeMobileMenu);
      });
    },

    initScrollEffects() {
      const header = document.getElementById('header');
      if (!header) return;

      let lastScroll = 0;
      window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 50) {
          header.classList.add('shadow-lg');
        } else {
          header.classList.remove('shadow-lg');
        }
        lastScroll = currentScroll;
      }, { passive: true });

      const fadeElements = document.querySelectorAll('.fade-up');
      if (fadeElements.length > 0 && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              entry.target.classList.add('fade-up-active');
              observer.unobserve(entry.target);
            }
          });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        fadeElements.forEach(el => observer.observe(el));
      }
    },

    initTestimonials() {
      const carousel = document.getElementById('testimonial-carousel');
      if (!carousel) return;

      const slides = carousel.querySelectorAll('.testimonial-slide');
      const dotsContainer = carousel.querySelector('.carousel-dots');
      let currentSlide = 0;
      let autoplayInterval;

      if (slides.length <= 1) return;

      slides.forEach((_, i) => {
        const dot = document.createElement('button');
        dot.className = `carousel-dot w-2 h-2 rounded-full transition-all ${i === 0 ? 'bg-blue-500 w-4' : 'bg-gray-400'}`;
        dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
        dot.addEventListener('click', () => goToSlide(i));
        dotsContainer.appendChild(dot);
      });

      function goToSlide(index) {
        slides[currentSlide].classList.add('hidden');
        slides[currentSlide].classList.remove('block');
        dotsContainer.children[currentSlide].className = 'carousel-dot w-2 h-2 rounded-full bg-gray-400 transition-all';
        dotsContainer.children[currentSlide].classList.remove('bg-blue-500', 'w-4');

        currentSlide = index;
        slides[currentSlide].classList.remove('hidden');
        slides[currentSlide].classList.add('block');
        dotsContainer.children[currentSlide].className = 'carousel-dot w-2 h-2 rounded-full bg-blue-500 w-4 transition-all';
      }

      function nextSlide() {
        goToSlide((currentSlide + 1) % slides.length);
      }

      function startAutoplay() {
        autoplayInterval = setInterval(nextSlide, 5000);
      }

      function stopAutoplay() {
        clearInterval(autoplayInterval);
      }

      carousel.addEventListener('mouseenter', stopAutoplay);
      carousel.addEventListener('mouseleave', startAutoplay);
      startAutoplay();
    },

    initFormValidation() {
      const form = document.getElementById('contact-form');
      if (!form) return;

      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        let isValid = true;

        form.querySelectorAll('[required]').forEach(field => {
          const errorEl = form.querySelector(`#${field.id}-error`);
          if (!field.value.trim()) {
            isValid = false;
            field.classList.add('border-red-500');
            if (errorEl) {
              errorEl.textContent = 'This field is required';
              errorEl.classList.remove('hidden');
            }
          } else if (field.type === 'email' && !this.isValidEmail(field.value)) {
            isValid = false;
            field.classList.add('border-red-500');
            if (errorEl) {
              errorEl.textContent = 'Please enter a valid email';
              errorEl.classList.remove('hidden');
            }
          } else {
            field.classList.remove('border-red-500');
            if (errorEl) errorEl.classList.add('hidden');
          }
        });

        const consent = form.querySelector('#consent');
        if (consent && !consent.checked) {
          isValid = false;
          const errorEl = form.querySelector('#consent-error');
          if (errorEl) {
            errorEl.textContent = 'Please check this box to continue';
            errorEl.classList.remove('hidden');
          }
        }

        if (isValid) {
          const submitBtn = form.querySelector('button[type="submit"]');
          const originalText = submitBtn ? submitBtn.textContent : '';
          
          if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Sending...';
          }

          try {
            const formData = new FormData(form);
            const response = await fetch('/api/contact', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
              },
              body: new URLSearchParams(formData).toString(),
            });

            if (response.ok) {
              const successMessage = document.getElementById('form-success');
              const formContent = document.getElementById('form-content');
              if (successMessage && formContent) {
                formContent.classList.add('hidden');
                successMessage.classList.remove('hidden');
              }
            } else {
              throw new Error('Failed to send');
            }
          } catch (error) {
            alert('There was an error sending your message. Please try again or call us directly.');
            if (submitBtn) {
              submitBtn.disabled = false;
              submitBtn.textContent = originalText;
            }
          }
        }
      });

      form.querySelectorAll('input, select, textarea').forEach(field => {
        field.addEventListener('input', () => {
          field.classList.remove('border-red-500');
          const errorEl = form.querySelector(`#${field.id}-error`);
          if (errorEl) errorEl.classList.add('hidden');
        });
      });
    },

    isValidEmail(email) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    },

    initSmoothScroll() {
      document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
          const targetId = anchor.getAttribute('href');
          if (targetId === '#') return;
          const target = document.querySelector(targetId);
          if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        });
      });
    }
  };

  document.addEventListener('DOMContentLoaded', () => BerkleySecurity.init());
})();
