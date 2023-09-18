function addToCart(product_id) {
    event.preventDefault();
    
    
    if (user_is_logged_in) { 
        $.ajax({
            type: 'GET',
            url: `/add_to_cart/${product_id}/`,
            success: function(response) {
                Swal.fire({
                    icon: 'success',
                    title: 'Done',
                    text: 'Product has been added to your cart!',
                    timer: 4000, // Thời gian tự động đóng (4 giây)
                    showConfirmButton: false, // Ẩn nút "OK"
                });
                updateCartCount();
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    } else {
        window.location.href = '/loginUser';
    }
}



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