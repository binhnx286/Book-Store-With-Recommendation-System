(function($) {
    $(document).ready(function() {
        // Hàm điều chỉnh hiển thị/ẩn các trường tùy theo giá trị của 'promotion_type'
        function toggleFields() {
            var promotionType = $('#id_promotion_type').val();  // Lấy giá trị của 'promotion_type'
            console.log('Current promotion_type: ', promotionType); // Kiểm tra giá trị của promotion_type trong console

            // Ẩn tất cả các trường trước khi thay đổi
            $('#id_products').closest('.form-row').hide();  // Ẩn trường 'products'
            $('#id_products_from').closest('.form-row').hide(); // Ẩn trường 'products_from'
            $('#id_subcategories').closest('.form-row').hide(); // Ẩn trường 'subcategories'
            $('#id_subcategories_from').closest('.form-row').hide(); // Ẩn trường 'subcategories_from'

            // Kiểm tra giá trị 'promotion_type' và hiển thị trường tương ứng
            if (promotionType === 'product') {
                console.log("Showing 'products' field");
                $('#id_products').closest('.form-row').show();  // Hiển thị trường 'products'
                $('#id_products_from').closest('.form-row').show(); // Hiển thị trường 'products_from'
            } else if (promotionType === 'subcategory') {
                console.log("Showing 'subcategories' field");
                $('#id_subcategories').closest('.form-row').show();  // Hiển thị trường 'subcategories'
                $('#id_subcategories_from').closest('.form-row').show(); // Hiển thị trường 'subcategories_from'
            }
        }

        // Gọi hàm khi trang được tải và khi giá trị của 'promotion_type' thay đổi
        toggleFields();  // Cập nhật khi trang được tải lần đầu

        // Thêm sự kiện thay đổi giá trị của 'promotion_type' để cập nhật lại các trường
        $('#id_promotion_type').on('change', function() {
            console.log('Promotion Type Changed'); // Kiểm tra xem có thay đổi giá trị không
            toggleFields();  // Cập nhật lại các trường sau khi thay đổi giá trị
        });
    });
})(django.jQuery);
