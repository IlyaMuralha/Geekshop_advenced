
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
        orderItemNum = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (priceArr[orderItemNum]) {
            orderItemQuantity = parseInt(target.value);
            deltaQuantity = orderItemQuantity - quantityArr[orderItemNum];
            quantityArr[orderItemNum] = orderItemQuantity;
            orderSummaryUpdate(priceArr[orderItemNum], deltaQuantity)
        }
    });

    $('.order_form').on('click', 'input[type=checkbox]', function() {
        let target = event.target
        orderItemNum = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (target.checked) {
            deltaQuantity = -quantityArr[orderItemNum];
        } else {
            deltaQuantity = quantityArr[orderItemNum];
        }
        orderSummaryUpdate(priceArr[orderItemNum], deltaQuantity)
    });

    function orderSummaryRecalc () {
        orderTotalQuantity = 0;
        orderTotalPrice = 0;

        for (let i = 0; i < totalForms; i++) {
            orderTotalQuantity += quantityArr[i];
            orderTotalPrice += priceArr[i];
        }

        $('.order_total_quantity').html(orderTotalQuantity.toString());
        $('.order_total_cost').html(orderTotalPrice.toFixed(2).toString());
    }

    function orderSummaryUpdate (orderItemPrice, deltaQuantity) {
        deltaCost = orderItemPrice * deltaQuantity;
        orderTotalPrice = Number((orderTotalPrice + deltaCost).toFixed(2));
        orderTotalQuantity = orderTotalQuantity + deltaQuantity;

        $('.order_total_quantity').text(orderTotalQuantity.toString());
        $('.order_total_cost').text(orderTotalPrice.toString());
    }

    $('.order_form select').change(function () {
        let target = event.target;
        orderItemNum = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));

        let orderItemProductPk = target.options[target.selectedIndex].value;

        if (orderItemProductPk) {
            $.ajax({
                url: '/order/product/' + orderItemProductPk + '/price/',
                success: function (data) {
                  if (data.price) {
                      priceArr[orderItemNum] = parseFloat(data.price);
                      if (isNaN(quantityArr[orderItemNum])) {
                          quantityArr[orderItemNum] = 0;
                      }
                      let priceHtml = '<span class="orderitems-' + orderItemNum + '-price">' + data.price.toString().replace('.', ',') + '</span> руб';
                      let curTr = $('.order_form table').find('tr:eq(' + (orderItemNum + 1) + ')');
                      curTr.find('td:eq(2)').html(priceHtml);
                      orderSummaryRecalc();
                  }
                }
            });
        }
    })

    $('.formset_row').formset({
        addText: 'Добавить продукт',
        deleteText: 'Удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem,
    });



    function deleteOrderItem(row) {
        let target_name = row[0].querySelector('input[type=number]').name
        orderItemNum = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));

        deltaQuantity = -quantityArr[orderItemNum];
        orderSummaryUpdate(priceArr[orderItemNum], deltaQuantity)
    }
}