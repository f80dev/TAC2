var element = document.getElementsByClassName("#1"), index;
for (index = element.length - 1; index >= 0; index--) {
    element[index].parentNode.removeChild(element[index]);
}