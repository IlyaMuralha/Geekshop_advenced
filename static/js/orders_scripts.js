
window.onload = function () {
    let _quantity, _price, orderItemNum, deltaQuantity, orderItemQuantity, deltaCost;

    let quantityArr = [];
    let priceArr = [];

    let totalForms = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());

    let orderTotalQuantity = parseInt($('.order_total_quantity').text()) || 0;
    let orderTotalPrice = parseFloat($('.order_total_cost').text()) || 0;
    console.log("order DOM ready");

    for (let i = 0; i < totalForms; i++) {
        _quantity = parseInt($('input[name=orderitems-' + i + '-quantity]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));

        quantityArr[i] = _quantity;
        if (_price) {
            priceArr[i] = _price;
        } else {
            priceArr[i] = 0;
        }
    }

    $('.order_form').on('click', 'input[type=number]', function() {
        let target = event.target
        orderItemNum = parseInt(target.name.replace('orderitems-', '').replace('-quantity'));
        if (priceArr[orderItemNum]) {
            orderItemQuantity = parseInt(target.value);
            deltaQuantity = orderItemQuantity - quantityArr[orderItemNum];
            quantityArr[orderItemNum] = orderItemQuantity;
            orderSummaryUpdate(priceArr[orderItemNum], deltaQuantity)
        }
    });

    $('.order_form').on('click', 'input[type=checkbox]', function() {
        let target = event.target
        orderItemNum = parseInt(target.name.replace('orderitems-', '').replace('-DELETE'));
        if (target.checked) {
            deltaQuantity = -quantityArr[orderItemNum];
        } else {
            deltaQuantity = quantityArr[orderItemNum];
        }
        orderSummaryUpdate(priceArr[orderItemNum], deltaQuantity)
    });

    function orderSummaryUpdate (orderItemPrice, deltaQuantity) {
        deltaCost = orderItemPrice * deltaQuantity;
        orderTotalPrice = Number((orderTotalPrice + deltaCost).toFixed(2));
        orderTotalQuantity = orderTotalQuantity + deltaQuantity;

        $('.order_total_quantity').text(orderTotalQuantity.toString());
        $('.order_total_cost').text(orderTotalPrice.toString());
    }
}