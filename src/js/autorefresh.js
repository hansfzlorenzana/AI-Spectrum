var timer = setInterval("autoRefresh()", 1000 * 5 * 60);

function autoRefresh() {
  self.location.reload(true);
}