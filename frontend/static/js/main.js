// ResumeAI Pro - Production Handcrafted JavaScript

document.addEventListener('DOMContentLoaded', () => {
    // 1. Auto-dismiss Flash Alerts
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 7000);
    });

    // 2. Realistic Multi-step Upload & Analysis Flow
    const uploadForm = document.getElementById('resumeUploadForm');
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('resume_file');
    const fileSelectedText = document.getElementById('file_selected_name');
    const uploadProgressContainer = document.getElementById('uploadProgressContainer');
    const uploadProgressBar = document.getElementById('uploadProgressBar');
    const uploadStepStatus = document.getElementById('uploadStepStatus');
    const uploadSubmitBtn = document.getElementById('uploadSubmitBtn');

    if (dropzone && fileInput) {
        dropzone.addEventListener('click', () => fileInput.click());

        dropzone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropzone.classList.add('dragover');
        });

        ['dragleave', 'dragend'].forEach(type => {
            dropzone.addEventListener(type, () => dropzone.classList.remove('dragover'));
        });

        dropzone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropzone.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                updateFileName(e.dataTransfer.files[0].name);
            }
        });

        fileInput.addEventListener('change', () => {
            if (fileInput.files.length) {
                updateFileName(fileInput.files[0].name);
            }
        });
    }

    function updateFileName(name) {
        if (fileSelectedText) {
            fileSelectedText.innerHTML = `
                <div class="d-flex align-items-center justify-content-center gap-2">
                    <i class="fas fa-file-invoice text-primary fs-5"></i>
                    <span>Selected Document: <strong>${name}</strong></span>
                </div>`;
            fileSelectedText.classList.remove('d-none');
        }
    }

    if (uploadForm) {
        uploadForm.addEventListener('submit', function (e) {
            if (!fileInput.files.length) {
                e.preventDefault();
                alert("Please select your resume file first.");
                return;
            }

            if (uploadProgressContainer && uploadProgressBar && uploadStepStatus && uploadSubmitBtn) {
                // Show progressive multi-step processing sequence
                uploadSubmitBtn.disabled = true;
                uploadSubmitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Processing Resume...`;
                uploadProgressContainer.classList.remove('d-none');

                const steps = [
                    { progress: 20, text: "Reading document file..." },
                    { progress: 45, text: "Parsing text structure and contact info..." },
                    { progress: 70, text: "Evaluating technical skills & formatting..." },
                    { progress: 90, text: "Generating Google Gemini AI critique..." },
                    { progress: 98, text: "Finalizing ATS report..." }
                ];

                let currentStep = 0;
                const interval = setInterval(() => {
                    if (currentStep < steps.length) {
                        uploadProgressBar.style.width = steps[currentStep].progress + '%';
                        uploadStepStatus.textContent = steps[currentStep].text;
                        currentStep++;
                    } else {
                        clearInterval(interval);
                    }
                }, 600);
            }
        });
    }

    // 3. Form Submit Button Spinner Lock for all generic forms
    document.querySelectorAll('form:not(#resumeUploadForm)').forEach(form => {
        form.addEventListener('submit', function () {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Loading...`;
            }
        });
    });
});
