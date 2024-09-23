class Row {
    constructor(title, type) {
        this.title = title;
        this.type = type;
        this.icon = null;
        this.branch = null;
    }

    setIcon(icon) {
        this.icon = icon;
    }

    getInformation() {
        return this.title;
    }
}

module.exports = Row;