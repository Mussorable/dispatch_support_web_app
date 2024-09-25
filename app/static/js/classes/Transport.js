export default class Transport {
    constructor(transport_type_api, transport_title) {
        this.transport_type_api = `http://127.0.0.1:5000/api${transport_type_api}`;
        this.transport_title = transport_title;
    }

    async fetchAll() {
        try {
            const response = await fetch(`${this.transport_type_api}`)
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            return response.json();
        } catch (error) {
            console.error(error);
            return null;
        }
    }

    buildTree(data, folderName = this.transport_title) {
        const treeContainer = document.getElementById('tree-container');
        if (treeContainer && data && folderName)  {
            // Parent block
            const tree = document.createElement('div');
            tree.classList.add('tree');

            // Parent block wrapper
            const treeDescription = document.createElement('div');
            treeDescription.classList.add('tree-description');

            // Wrap/unwrap button
            const wrapButton = document.createElement('img');
            wrapButton.classList.add('action-unfold');
            wrapButton.src = plusIconPath;

            // Item icon
            const folderIcon = document.createElement('img');
            folderIcon.classList.add('folder-icon');
            folderIcon.src = folderIconPath;

            // Item name
            const itemName = document.createElement('span');
            itemName.classList.add('item-name');
            itemName.textContent = folderName;

            // Generate order
            tree.appendChild(treeDescription);
            treeDescription.appendChild(wrapButton);
            treeDescription.appendChild(folderIcon);
            treeDescription.appendChild(itemName);

            treeContainer.appendChild(tree);
        }
    }
}