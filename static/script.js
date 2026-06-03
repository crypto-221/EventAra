
  // Floating dots
  const dotsEl = document.getElementById('dots');
  for (let i = 0; i < 25; i++) {
    const d = document.createElement('div');
    d.className = 'dot';
    const size = Math.random() * 4 + 2;
    d.style.cssText = `
      width:${size}px; height:${size}px;
      left:${Math.random()*100}%;
      bottom:${Math.random()*-20}%;
      animation-duration:${Math.random()*15+10}s;
      animation-delay:${Math.random()*10}s;
      opacity:${Math.random()*0.4+0.1};
    `;
    dotsEl.appendChild(d);
  }

  function switchTab(tab) {
    const tLogin = document.getElementById('tabLogin');
    const tSignup = document.getElementById('tabSignup');
    const pLogin = document.getElementById('panelLogin');
    const pSignup = document.getElementById('panelSignup');

    if (tab === 'login') {
      tLogin.classList.add('active'); tSignup.classList.remove('active');
      pLogin.classList.add('active'); pSignup.classList.remove('active');
    } else {
      tSignup.classList.add('active'); tLogin.classList.remove('active');
      pSignup.classList.add('active'); pLogin.classList.remove('active');
    }
  }

  function showToast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3500);
  }

  function doLogin() {
    const email = document.getElementById('loginEmail').value.trim();
    const pass = document.getElementById('loginPass').value.trim();
    if (!email || !pass) { showToast('⚠️ Please fill in all fields'); return; }
    const name = email.split('@')[0].split('.')[0];
    revealSearch(name.charAt(0).toUpperCase() + name.slice(1));
    showToast('✅ Welcome back! Find your next event.');
  }

  function doSignup() {
    const first = document.getElementById('firstName').value.trim();
    const email = document.getElementById('signupEmail').value.trim();
    const pass = document.getElementById('signupPass').value.trim();
    if (!first || !email || !pass) { showToast('⚠️ Please fill in all fields'); return; }
    if (pass.length < 8) { showToast('⚠️ Password must be 8+ characters'); return; }
    revealSearch(first);
    showToast('🎉 Account created! Start exploring events.');
  }

  function revealSearch(name) {
    document.getElementById('authCard').style.display = 'none';
    document.getElementById('userName').textContent = name;
    document.getElementById('searchPanel').classList.add('visible');
    document.querySelector('.badge').style.display = 'none';
    document.querySelector('h1').textContent = '';
    document.querySelector('.hero-sub').style.display = 'none';
  }



    function useGPS() {
        const btn = document.querySelector('.gps-btn');
        const detected = document.getElementById('detectedCity');
        const detectedText = document.getElementById('detectedCityText');
        const citySelect = document.getElementById('citySelect');

        btn.innerHTML = `
            <svg class="gps-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 2v3M12 19v3M2 12h3M19 12h3"/>
            </svg>
            Detecting...
        `;
        btn.style.color = '#ff6b35';

        if (!navigator.geolocation) {
            detectedText.textContent = 'GPS not supported';
            detected.classList.add('show');
            return;
        }

        navigator.geolocation.getCurrentPosition(
            async (pos) => {
                const lat = pos.coords.latitude;
                const lng = pos.coords.longitude;

                // Reverse geocode with free API
                try {
                    const res = await fetch(
                        `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`
                    );
                    const data = await res.json();
                    const city = data.address.city
                        || data.address.town
                        || data.address.state_district
                        || 'Mumbai';

                    detectedText.textContent = `Detected: ${city}`;
                    detected.classList.add('show');

                    // Select city in dropdown if it exists
                    for (let option of citySelect.options) {
                        if (option.value.toLowerCase() === city.toLowerCase()) {
                            option.selected = true;
                            break;
                        }
                    }

                    // Hidden input for city value from GPS
                    let hiddenInput = document.getElementById('gpsCity');
                    if (!hiddenInput) {
                        hiddenInput = document.createElement('input');
                        hiddenInput.type = 'hidden';
                        hiddenInput.id = 'gpsCity';
                        hiddenInput.name = 'city';
                        document.querySelector('form').appendChild(hiddenInput);
                    }
                    hiddenInput.value = city;

                } catch (err) {
                    detectedText.textContent = 'Could not detect city';
                    detected.classList.add('show');
                }

                btn.innerHTML = `
                    <svg class="gps-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M20 6L9 17l-5-5"/>
                    </svg>
                    Got it!
                `;
            },
            () => {
                detectedText.textContent = 'Location access denied';
                detected.classList.add('show');
                btn.innerHTML = `
                    <svg class="gps-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="3"/>
                        <path d="M12 2v3M12 19v3M2 12h3M19 12h3"/>
                    </svg>
                    Use GPS
                `;
                btn.style.color = '';
            }
        );
    }