// --- Slider Logic ---
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.progress-dot');
    const totalSlides = slides.length;
    let slideInterval;

    function goToSlide(index) {
      if (index >= totalSlides) index = 0;
      if (index < 0) index = totalSlides - 1;

      slides.forEach(s => s.classList.remove('active'));
      dots.forEach(d => d.classList.remove('active'));

      slides[index].classList.add('active');
      dots[index].classList.add('active');
      
      currentSlide = index;
      startAutoSlide();
    }

    function nextSlide() { goToSlide(currentSlide + 1); }
    function prevSlide() { goToSlide(currentSlide - 1); }

    function startAutoSlide() {
      clearInterval(slideInterval);
      slideInterval = setInterval(nextSlide, 5000);
    }

    document.getElementById('nextSlide').addEventListener('click', nextSlide);
    document.getElementById('prevSlide').addEventListener('click', prevSlide);

    document.getElementById('progressDots').addEventListener('click', (e) => {
      if (e.target.classList.contains('progress-dot')) {
        goToSlide(parseInt(e.target.dataset.index));
      }
    });

    startAutoSlide();

    // Scroll Reveal
    const revealElements = document.querySelectorAll('.reveal');
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) entry.target.classList.add('active');
      });
    }, { threshold: 0.1 });

    revealElements.forEach(el => revealObserver.observe(el));