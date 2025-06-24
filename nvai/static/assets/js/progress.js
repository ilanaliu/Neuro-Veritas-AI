function showProgressBar() {
    document.getElementById('progressContainer').style.display = 'block';
    document.getElementById('progressBar').style.width = '30%';
    document.getElementById('progressLabel').innerText = 'Uploading and processing...';
    // Simulate progress (optional, for user feedback)
    let width = 30;
    let interval = setInterval(function() {
        if (width < 90) {
            width += 10;
            document.getElementById('progressBar').style.width = width + '%';
        } else {
            clearInterval(interval);
        }
    }, 500);
}

window.onload = function() {
    // Hide progress bar if results are shown (page reloaded after POST)
    if (document.querySelector('.post pre') || document.querySelector('.post div')) {
        document.getElementById('progressContainer').style.display = 'none';
        document.getElementById('progressBar').style.width = '100%';
    }
};