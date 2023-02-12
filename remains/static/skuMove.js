$(function (){
    const skuMove = (obj, sap_eq, sku_name_eq) => {

        let sap_value = obj.parent().children().eq(sap_eq).text()
        let sku_name_value = obj.parent().children().eq(sku_name_eq).text()

        $("#loading").removeClass('d-none')

        $.ajax({
            type: 'GET',
            url: 'sku/',
            data: {'sap': sap_value, 'sku_name': sku_name_value},
            success: function (answer){
                $(".modal-content").html(answer);

                $("#loading").addClass('d-none');

                $("#skuMoveModal").modal('show')
            }
        })
    }

    $("div.move-contlog").click(function (){
        skuMove($(this),1, 2)
    })

    $("div.move-place").click(function (){
        skuMove($(this), 2, 3)
    })

    //
    // $("div.move").click(function (){
    //     let sap = $(this).parent().children().eq(2).text()
    //     let sku_name = $(this).parent().children().eq(3).text()
    //
    //     $("#loading").removeClass('d-none')
    //
    //     $.ajax({
    //         type: 'GET',
    //         url: 'sku/',
    //         data: {'sap': sap, 'sku_name': sku_name},
    //         success: function (answer){
    //             $(".modal-content").html(answer);
    //
    //             $("#loading").addClass('d-none');
    //
    //             $("#skuMoveModal").modal('show')
    //         }
    //     })
    // })
})