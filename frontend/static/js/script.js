document.addEventListener('DOMContentLoaded', () => {
    // State
    let currentTheme = 'light';
    let currentTab = 'upload';
    let stream = null;

    // Elements
    const themeToggle = document.getElementById('theme-toggle');
    const tabUpload = document.getElementById('tab-upload');
    const tabCamera = document.getElementById('tab-camera');
    const uploadArea = document.getElementById('upload-area');
    const cameraArea = document.getElementById('camera-area');
    const fileInput = document.getElementById('file-input');
    const video = document.getElementById('camera-preview');
    const captureBtn = document.getElementById('capture-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    const heroSection = document.getElementById('hero-section');
    const dashboardSection = document.getElementById('dashboard-section');
    const imagePreview = document.getElementById('image-preview');

    // Theme Handling
    themeToggle.addEventListener('click', () => {
        currentTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', currentTheme);
        themeToggle.textContent = currentTheme === 'light' ? '🌙' : '☀️';
    });

    // Tab Handling
    function switchTab(tab) {
        currentTab = tab;
        if (tab === 'upload') {
            tabUpload.classList.add('active');
            tabCamera.classList.remove('active');
            uploadArea.classList.remove('hidden');
            cameraArea.classList.add('hidden');
            stopCamera();
        } else {
            tabUpload.classList.remove('active');
            tabCamera.classList.add('active');
            uploadArea.classList.add('hidden');
            cameraArea.classList.remove('hidden');
            startCamera();
        }
    }

    tabUpload.addEventListener('click', () => switchTab('upload'));
    tabCamera.addEventListener('click', () => switchTab('camera'));

    // Camera Logic
    async function startCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
        } catch (err) {
            console.error("Error accessing camera:", err);
            alert("Could not access camera. Please check permissions.");
        }
    }

    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
    }

    // Capture Photo
    captureBtn.addEventListener('click', () => {
        if (!video.srcObject || !video.srcObject.active) {
            alert('Camera is not ready. Please try again.');
            return;
        }

        const canvas = document.createElement('canvas');
        
        let width = video.videoWidth;
        let height = video.videoHeight;
        
        if (width === 0 || height === 0) {
            alert('Camera feed is not ready. Please wait a moment and try again.');
            return;
        }
        
        const maxWidth = 1280;
        
        if (width > maxWidth) {
            height = height * (maxWidth / width);
            width = maxWidth;
        }
        
        canvas.width = width;
        canvas.height = height;
        canvas.getContext('2d').drawImage(video, 0, 0, width, height);
        
        // Convert to blob for better handling
        canvas.toBlob((blob) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const base64Data = e.target.result;
                imagePreview.src = base64Data;
                imagePreview.classList.remove('hidden');
                analyzeBtn.disabled = false;
                analyzeBtn.onclick = () => analyzeImage(null, base64Data);
            };
            reader.readAsDataURL(blob);
        }, 'image/jpeg', 0.85);
    });

    // File Upload
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                imagePreview.classList.remove('hidden');
            };
            reader.readAsDataURL(file);
            
            analyzeBtn.onclick = () => analyzeImage(file, null);
            analyzeBtn.disabled = false;
        }
    });

    // Analysis Logic
    async function analyzeImage(file, base64Data) {
        // Show Loading
        const btnText = analyzeBtn.innerHTML;
        analyzeBtn.innerHTML = '<span class="loader"></span> Analyzing...';
        analyzeBtn.disabled = true;

        const formData = new FormData();
        if (file) {
            formData.append('image', file);
        } else if (base64Data) {
            formData.append('image_base64', base64Data);
        }

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.status === 'success') {
                renderResults(data);
            } else {
                console.error("Analysis Error:", data);
                alert('Analysis failed: ' + (data.error || 'Unknown error'));
            }
        } catch (err) {
            console.error("Request Error:", err);
            alert('Error connecting to server: ' + err.message);
        } finally {
            analyzeBtn.innerHTML = btnText;
            analyzeBtn.disabled = false;
        }
    }

    // Render Results
    function renderResults(data) {
        if (!data || data.status === 'error') {
            alert('Analysis failed: ' + (data.error || 'Unknown error'));
            return;
        }

        heroSection.classList.add('hidden');
        dashboardSection.classList.remove('hidden');

        const final = data.results || {};
        const analysis = data.analysis || {};
        
        // Update Object Card
        document.getElementById('res-image').src = "data:image/png;base64," + (data.image_b64 || '');
        document.getElementById('res-title').textContent = final.object_type || 'Unknown';
        document.getElementById('res-verdict').textContent = final.verdict || 'N/A';
        document.getElementById('res-materials').textContent = (analysis.material_composition || []).join(', ') || 'Unknown';
        document.getElementById('res-safety').textContent = `🛡️ Safety Score: ${analysis.safety_score || final.score || 0}/100`;
        document.getElementById('res-condition').textContent = final.condition_summary || 'No summary available.';

        // Update Impact Card
        const co2 = analysis.estimated_co2_saved_kg || 0.5;
        document.getElementById('res-co2-unit').textContent = `${co2} kg`;
        document.getElementById('res-co2-total').textContent = `${(co2 * 2.5).toFixed(2)} kg`;

        // Update Pricing if available
        if (data.results.pricing) {
            const pricing = data.results.pricing;
            const priceRange = pricing.suggested_price_range;
            const confidence = pricing.pricing_confidence || 'Medium';
            
            document.getElementById('res-price-range').textContent = `₹${priceRange.min} - ₹${priceRange.max}`;
            document.getElementById('res-price-confidence').textContent = `Confidence: ${confidence}`;
        }

        // Render Suggestions
        const suggestionsContainer = document.getElementById('suggestions-container');
        suggestionsContainer.innerHTML = '';

        const suggestions = analysis.suggestions || final.suggestions || [];
        if (suggestions.length === 0) {
            suggestionsContainer.innerHTML = '<p style="color: var(--text-600);">No specific reuse ideas generated for this item.</p>';
        }

        suggestions.forEach(rec => {
            const div = document.createElement('div');
            div.className = 'rec-item';
            div.innerHTML = `
                <div class="rec-header">
                    <div>
                        <div class="rec-badges">
                            <span class="badge badge-emerald">${rec.category || 'Upcycle'}</span>
                            <span class="badge badge-amber">${rec.difficulty || 'Medium'}</span>
                        </div>
                        <h4 style="margin: 0.5rem 0; font-size: 1.1rem;">${rec.title || rec.use_case}</h4>
                        <p style="color: var(--text-600); font-size: 0.9rem;">${rec.description || rec.explanation}</p>
                    </div>
                </div>
                <div style="background: var(--bg-color); padding: 1rem; border-radius: 0.5rem;">
                    <strong>✅ Instructions:</strong>
                    <ol style="margin-top: 0.5rem; padding-left: 1.5rem; color: var(--text-600);">
                        ${(rec.steps || []).map(s => `<li>${s}</li>`).join('')}
                    </ol>
                </div>
            `;
            suggestionsContainer.appendChild(div);
        });

        // Scroll to results
        dashboardSection.scrollIntoView({ behavior: 'smooth' });
    }

    // Back Button
    document.getElementById('back-btn').addEventListener('click', () => {
        dashboardSection.classList.add('hidden');
        heroSection.classList.remove('hidden');
        stopCamera();
        imagePreview.classList.add('hidden');
        imagePreview.src = '';
        fileInput.value = '';
    });
});
