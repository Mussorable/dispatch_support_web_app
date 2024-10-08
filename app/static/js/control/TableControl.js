export default class TableControl {
    toggleExpandCollapse(button) {
        if (button.src.includes(plusIconPath)) {
            button.src = minusIconPath;
        } else {
            button.src = plusIconPath;
        }
    }

    toggleFolderIcon(expandButton) {
        const folderIcon = expandButton.parentElement.querySelector('img.folder-icon');
        if (folderIcon.src.includes(folderIconPath)) {
            folderIcon.src = folderOpenedIconPath;
        } else {
            folderIcon.src = folderIconPath;
        }
    }
}