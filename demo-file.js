// Demo file for testing Iris VS Code features
function calculateTotal(items) {
    return items.reduce((sum, item) => sum + item.price, 0);
}

class ShoppingCart {
    constructor() {
        this.items = [];
    }
    
    addItem(item) {
        this.items.push(item);
    }
    
    getTotal() {
        return calculateTotal(this.items);
    }
}

export { ShoppingCart, calculateTotal };