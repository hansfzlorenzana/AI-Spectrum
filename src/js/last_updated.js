var request = new XMLHttpRequest();
request.open('GET', 'last_updated.txt', false);
request.send();
var textFileContent = request.responseText
document.getElementById("displayLastUpdated").innerHTML = textFileContent;