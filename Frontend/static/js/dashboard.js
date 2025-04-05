document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('imageUpload');
    const uploadButton = document.querySelector('.upload-button');
    const previewContainer = document.querySelector('.image-area');
    const imageTitle = document.querySelector('.image-head');
    const back = document.querySelector('.back');
    const userDisplayElement = document.querySelector('.login-name');
    const analyze = document.querySelector('.analyze-button');
    const markdownArea = document.querySelector('.markdown-area');
    const userName = localStorage.getItem('loginName');

    // ========== Set Logged-In Username ==========
    if (userName && userDisplayElement) {
        userDisplayElement.innerHTML = `<span style="font-size: 2rem;">👤</span> ${userName}`;
    }

    // ========== Back Button Navigation ==========
    back.addEventListener('click', function () {
        window.location.href = '/';
    });

    // ========== Upload Button Triggers File Input ==========
    uploadButton.addEventListener('click', function () {
        fileInput.click();
    });

    // ========== Preview and Store Uploaded Images ==========
    let formData = new FormData();

    fileInput.addEventListener('change', function () {
        imageTitle.style.display = 'block';
        document.querySelectorAll('.preview-image').forEach(img => img.remove());
        formData = new FormData(); // reset

        Array.from(fileInput.files).forEach(file => {
            if (file.type.startsWith('image/')) {
                formData.append('images', file);

                const reader = new FileReader();
                reader.onload = function (e) {
                    const imageDiv = document.createElement('div');
                    imageDiv.classList.add('preview-image');
                    imageDiv.style.backgroundImage = `url('${e.target.result}')`;
                    previewContainer.appendChild(imageDiv);
                };

                reader.readAsDataURL(file);
            }
        });
    });

    // ========== Analyze Button Click ========== 
    if (analyze) {
        analyze.addEventListener('click', async function () {
            const allAnalysis = await uploadImages(formData);

            if (allAnalysis && Array.isArray(allAnalysis)) {
                const chatHead = markdownArea.querySelector('.chat-head');
                const loader = markdownArea.querySelector('.markdown-loader');

                // Clear old responses
                markdownArea.querySelectorAll('.receipt-response').forEach(el => el.remove());

                // Append chatHead and loader if not already present
                if (chatHead && !markdownArea.contains(chatHead)) {
                    markdownArea.appendChild(chatHead);
                }

                if (loader && !markdownArea.contains(loader)) {
                    markdownArea.appendChild(loader);
                }

                // Append new analysis results
                allAnalysis.forEach(text => {
                    const responseDiv = document.createElement('div');
                    responseDiv.classList.add('receipt-response');
                    responseDiv.textContent = text;
                    markdownArea.appendChild(responseDiv);
                });
            }
        });
    }
});

// ========== Image Upload & Analyze Function ==========
async function uploadImages(formData) {
    const markdownArea = document.querySelector('.markdown-area');
    const loader = markdownArea.querySelector('.markdown-loader');

    try {
        console.log('Uploading images...');
        alert('Images uploaded successfully! Analysis starting...');

        // Clear old content
        markdownArea.querySelectorAll('.receipt-response').forEach(el => el.remove());

        // Show loader
        if (loader) loader.style.display = 'flex';

        const response = await fetch('/api/upload-images', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        // Hide loader
        if (loader) loader.style.display = 'none';

        if (result.status === 'success') {
            alert('Analysis completed!');

            result.all_analysis.forEach(text => {
                const responseDiv = document.createElement('div');
                responseDiv.classList.add('receipt-response');
                responseDiv.textContent = text;
                markdownArea.appendChild(responseDiv);
            });

            return result.all_analysis;
        } else {
            alert('Upload failed: ' + result.error);
        }
    } catch (error) {
        console.error('Error uploading images:', error);
        if (loader) loader.style.display = 'none';
    }
}
