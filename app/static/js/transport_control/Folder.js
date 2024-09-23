const Row = require('./Row');
const plusIcon = require('../../svg/plus.svg');

class Folder extends Row {

}

const folder = new Folder('bang', 'folder')
folder.setIcon(plusIcon);
console.log(folder)