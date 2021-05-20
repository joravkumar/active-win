const { ipcRenderer } = require('electron');


window.addEventListener('DOMContentLoaded', () => {
    const replaceText = (selector, text) => {
      const element = document.getElementById(selector)
      if (element) element.innerText = text
    }

    ipcRenderer.invoke('start-loop');

    ipcRenderer.on('render', (_, text) => {
        replaceText('active-win', text);
    });
  })