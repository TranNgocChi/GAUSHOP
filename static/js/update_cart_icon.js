function updateCartCount() {
    $.ajax({
        url: '/api/cart_count_api',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            $('#cart-count').text(data.cart_count);
        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
}

$(document).ready(function() {
    updateCartCount();
});