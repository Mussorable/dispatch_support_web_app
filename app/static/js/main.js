import Trucks from "./classes/Trucks.js";
import Trailers from "./classes/Trailers.js";

import TableControl from "./control/TableControl.js";

document.addEventListener("DOMContentLoaded", async () => {
    if (window.location.pathname === '/' || window.location.pathname === '/index') {
        const trucks = new Trucks();
        let truck_list = await trucks.fetchAll();
        trucks.buildTree(truck_list);


        const trailers = new Trailers('/trailers');
        let trailer_list = await trailers.fetchAll();
        trailers.buildTree(trailer_list);

        const tb = new TableControl();

        const expandCollapseButtons = document.querySelectorAll(".action-unfold");
        if (expandCollapseButtons.length > 0) {
            expandCollapseButtons.forEach(button => {
                button.addEventListener("click", () => {
                    tb.toggleExpandCollapse(button);
                    tb.toggleFolderIcon(button);
                });
            });
        }
    }
});