// const eel = require('electron')

async function createCurForRub() {
  const valueRub = parseFloat(document.getElementById('rub-input').value);
  const listCurs = document.getElementById('list-cur').children;

  // eslint-disable-next-line no-restricted-syntax
  for (const divCurr of listCurs) {
    const nameCurr = divCurr.getElementsByTagName('span')[0].textContent;
    // eslint-disable-next-line no-await-in-loop
    divCurr.getElementsByTagName('input')[0].value = await eel.convert_value_py(valueRub, 'RUB', nameCurr)();
  }
}

document.getElementById('btn-sum').onclick = createCurForRub;
