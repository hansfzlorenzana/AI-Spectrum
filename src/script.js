// The app-name shows at the navi once appTitle is out of sight
window.addEventListener('scroll', function() {
  var title = document.querySelector('.title');
  var appName = document.querySelector('.app-name');
  if (title && appName) {
     var titleRect = title.getBoundingClientRect();
     var isTitleVisible = titleRect.bottom > 0 && titleRect.top < window.innerHeight;
     appName.style.visibility = isTitleVisible ? 'hidden' : 'visible';
  }
});

// Last Updated
var request = new XMLHttpRequest();
request.open('GET', './app/database/last_updated.txt', false);
request.send();
var textFileContent = request.responseText
document.getElementById("displayLastUpdated").innerHTML = textFileContent;

// Auto Refresh

var timer = setInterval("autoRefresh()", 1000 * 5 * 60);

function autoRefresh() {
  self.location.reload(true);
}

// Last Updated for each AI
fetch('./app/database/ai_last_update.txt')
    .then(response => response.text())
    .then(data => {
        const updateContainer = document.getElementById('displayAIUpdates');
        const updates = data.trim().split('\n');

        updates.forEach(update => {
            const aiName = update.split(':')[0].trim();
            const updateText = update.replace(aiName, `<span class="ai-name">${aiName}</span>`);
            updateContainer.innerHTML += `<p>${updateText}</p>`;
        });
    })
    .catch(error => console.error(error));

// Show/Hide AI Last Updated
function toggleAIUpdatesContainer(containerId) {
    var container = document.getElementById(containerId);
    if (container.style.display === "none") {
        container.style.display = "block";
    } else {
        container.style.display = "none";
    }
}
  

