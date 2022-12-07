$(document).ready(() => {
    let tableContent = $('#products-table').html()
    $('#search-input').on('input', (e) => {
        $('#products-table').html('')
        if($(e.target).val() == '') {
            $('#products-table').html('')
            $('#products-table').html(tableContent)
        }

        let url = $(e.target).attr('data-url');
        let query = $(e.target).val();
        let csrf = $(e.target).find('input[name="csrfmiddlewaretoken"]').val()
        let type = $(e.target).attr('data-type');

        data = {}
        data.query = query
        data['csrfmiddlewaretoken'] = csrf

        $.ajax({
            url: url,
            type: 'GET',
            dataset: 'json',
            data: data,
            cashe: true,
            success: (data) => {
                if ($(e.target).val() != '') {
                    if(type == 'product') {
                        renderProds(data)
                    } else if(type == 'ctg') {
                        renderCategory(data)
                    } else if(type == 'order') {
                        renderOrders(data)
                    }
                }
            }, 
            error: () => {
                console.log('error')
            }
        })
    })

    
    $("#select-status").on('change', (e) => {
        $('#products-table').html('')
        if ($(e.target).val() == 'All') {
            $('#products-table').html('')
            $('#products-table').html(tableContent)
        }
        let status = $(e.target).val()
        let url = $(e.target).attr('data-url');
        let type = $(e.target).attr('data-type')

        data = {}
        data.status = status
        $.ajax({
            url: url,
            dataset: 'json',
            data: data,
            type: 'GET',
            success: (data) => {
                if(type == 'product') {
                    if ($(e.target).val() != '') {
                        renderProds(data)
                    }                    
                } else if(type == 'order') {
                    renderOrders(data)
                }

            },
            error: () => {
                console.log('error')
            }
        })
    })


    function renderProds(data) {
        for (let prod of data) {
            $('#products-table').html(
                `
                            <tr>
                                <td>
                                    <div class="form-check form-check-sm form-check-custom form-check-solid">
                                        <input class="form-check-input" type="checkbox" value="1" />
                                    </div>
                                </td>
                                <td>
                                    <div class="d-flex align-items-center">
                                        <a href="/admin/products_edit/${prod.id}"
                                            class="symbol symbol-50px">
                                            <img class="symbol-label"
                                                src="${prod.img_url}">
                                        </a>
                                        <div class="ms-5">
                                            <a href="/admin/products_edit/${prod.id}"
                                                class="text-gray-800 text-hover-primary fs-5 fw-bolder"
                                                data-kt-ecommerce-product-filter="product_name" data-prodsid="${prod.id}">${prod.name}</a>
                                        </div>
                                    </div>
                                </td>
                                <td class="text-end pe-0">
                                    <span class="fw-bolder">00${prod.id}</span>
                                </td>
                                <td class="text-end pe-0" data-order="25">
                                    <span class="fw-bolder ms-3">${prod.qty}</span>
                                </td>
                                <td class="text-end pe-0">
                                    <span class="fw-bolder text-dark">$${prod.price}.00</span>
                                </td>
                                <td class="text-end pe-0" data-order="${prod.status}">
                                    <div class="badge ${prod.status.toLowerCase()}">${prod.status}</div>
                                </td>
                                <td class="text-end">
                                    <a class="btn btn-sm btn-light btn-active-light-primary"
                                        data-kt-menu-trigger="click" data-kt-menu-placement="bottom-end">Actions
                                        <span class="svg-icon svg-icon-5 m-0">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                                viewBox="0 0 24 24" fill="none">
                                                <path
                                                    d="M11.4343 12.7344L7.25 8.55005C6.83579 8.13583 6.16421 8.13584 5.75 8.55005C5.33579 8.96426 5.33579 9.63583 5.75 10.05L11.2929 15.5929C11.6834 15.9835 12.3166 15.9835 12.7071 15.5929L18.25 10.05C18.6642 9.63584 18.6642 8.96426 18.25 8.55005C17.8358 8.13584 17.1642 8.13584 16.75 8.55005L12.5657 12.7344C12.2533 13.0468 11.7467 13.0468 11.4343 12.7344Z"
                                                    fill="currentColor" />
                                            </svg>
                                        </span>
                                    </a>
                                    <div class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-bold fs-7 w-125px py-4"
                                        data-kt-menu="true">
                                        <div class="menu-item px-3">
                                            <a href="/admin/products_edit/${prod.id}"
                                                class="menu-link px-3">Edit</a>
                                        </div>
                                        <div class="menu-item px-3">
                                            <a href="/admin/delete-products/${prod.id}" class="menu-link px-3"
                                                data-kt-ecommerce-product-filter="delete_row">Delete</a>
                                        </div>
                                    </div>
                                </td>
                            </tr>
                        `
                + $('#products-table').html()
            )
        } 


        $('.btn.btn-sm.btn-light.btn-active-light-primary').on('click', (e) => {
            for (let btn of $('.btn.btn-sm.btn-light.btn-active-light-primary')) {
                $(btn).removeClass('show menu-dropdown')
            }
            $(e.target).addClass('show menu-dropdown')
            $(e.target).parent().find('.menu.menu-sub.menu-sub-dropdown.menu-column.menu-rounded.menu-gray-600.menu-state-bg-light-primary.fw-bold.fs-7.w-125px.py-4').toggleClass('show')
            $(e.target).parent().find('.menu.menu-sub.menu-sub-dropdown.menu-column.menu-rounded.menu-gray-600.menu-state-bg-light-primary.fw-bold.fs-7.w-125px.py-4').css({ "z-index": "105", "position": "fixed", "inset": "0px 0px auto auto", "margin": "0px", "transform": "translate3d(-59px, 226px, 0px)" })

        })
    }


    function renderCategory(data) {
        for (let ctg of data) {
            $('#products-table').html(
                `
                <tr class="odd">
                    <td>
                        <div class="form-check form-check-sm form-check-custom form-check-solid">
                            <input class="form-check-input" type="checkbox" value="1">
                        </div>
                    </td>
                    <td>
                        <div class="d-flex">
                            <!--begin::Thumbnail-->
                            <a href="/admin/update-category/${ctg.id}"
                                class="symbol symbol-50px">
                                <span class="symbol-label"
                                    style="background-image: url('${ctg.img_url}')"></span>
                            </a>
                            <div class="ms-5">
                                <a href="/admin/update-category/${ctg.id}"
                                    class="text-gray-800 text-hover-primary fs-5 fw-bolder mb-1"
                                    data-kt-ecommerce-category-filter="category_name">${ctg.name}</a>
                                <div class="text-muted fs-7 fw-bolder">${ctg.desk}</div>
                            </div>
                        </div>
                    </td>
                    <td class="text-end">
                        <a href="#" class="btn btn-sm btn-light btn-active-light-primary"
                            data-kt-menu-trigger="click" data-kt-menu-placement="bottom-end">Actions
                            <!--begin::Svg Icon | path: icons/duotune/arrows/arr072.svg-->
                            <span class="svg-icon svg-icon-5 m-0">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                    viewBox="0 0 24 24" fill="none">
                                    <path
                                        d="M11.4343 12.7344L7.25 8.55005C6.83579 8.13583 6.16421 8.13584 5.75 8.55005C5.33579 8.96426 5.33579 9.63583 5.75 10.05L11.2929 15.5929C11.6834 15.9835 12.3166 15.9835 12.7071 15.5929L18.25 10.05C18.6642 9.63584 18.6642 8.96426 18.25 8.55005C17.8358 8.13584 17.1642 8.13584 16.75 8.55005L12.5657 12.7344C12.2533 13.0468 11.7467 13.0468 11.4343 12.7344Z"
                                        fill="currentColor"></path>
                                </svg>
                            </span>
                            <!--end::Svg Icon-->
                        </a>
                        <div class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-bold fs-7 w-125px py-4"
                            data-kt-menu="true">
                            <!--begin::Menu item-->
                            <div class="menu-item px-3">
                                <a href="/admin/update-category/${ctg.id}"
                                    class="menu-link px-3">Edit</a>
                            </div>
                            <!--end::Menu item-->
                            <!--begin::Menu item-->
                            <div class="menu-item px-3">
                                <a href="/admin/del_ctg/${ctg.id}" class="menu-link px-3"
                                    data-kt-ecommerce-category-filter="delete_row">Delete</a>
                            </div>
                        </div>
                    </td>
                </tr>
            `
            )
        }


        $('.btn.btn-sm.btn-light.btn-active-light-primary').on('click', (e) => {
            for (let btn of $('.btn.btn-sm.btn-light.btn-active-light-primary')) {
                $(btn).removeClass('show menu-dropdown')
            }
            $(e.target).addClass('show menu-dropdown')
            $(e.target).parent().find('.menu.menu-sub.menu-sub-dropdown.menu-column.menu-rounded.menu-gray-600.menu-state-bg-light-primary.fw-bold.fs-7.w-125px.py-4').toggleClass('show')
            $(e.target).parent().find('.menu.menu-sub.menu-sub-dropdown.menu-column.menu-rounded.menu-gray-600.menu-state-bg-light-primary.fw-bold.fs-7.w-125px.py-4').css({ "z-index": "105", "position": "fixed", "inset": "0px 0px auto auto", "margin": "0px", "transform": "translate3d(-59px, 226px, 0px)" })

        })
    }


    function renderOrders(data) {
        for (let order of data) {
            $('#products-table').html(
                `
                    <tr>
                        <td>
                            <div class="form-check form-check-sm form-check-custom form-check-solid">
                                <input class="form-check-input" type="checkbox" value="1" />
                            </div>
                        </td>
                        <td data-kt-ecommerce-order-filter="order_id">
                            <a href="/admin/order/${ order.id }"
                                class="text-gray-800 text-hover-primary fw-bolder">${ order.id }</a>
                        </td>
                        <td>
                            <div class="d-flex align-items-center">
                                <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
                                    <a href="/admin/order/${ order.id }">
                                        <img class="symbol-label fs-3 bg-light-danger text-danger"
                                            src="${ order.img }"
                                        >
                                    </a>
                                </div>
                                <div class="ms-5">
                                    <a href="/admin/order/${ order.id }"
                                        class="text-gray-800 text-hover-primary fs-5 fw-bolder">
                                            ${ order.username }
                                    </a>
                                </div>
                            </div>
                        </td>
                        <td class="text-end pe-0" data-order="${ order.status }">
                            <div class="badge ${ order.status.toLowerCase() }">${ order.status }</div>
                        </td>
                        <td class="text-end pe-0">
                            <span class="fw-bolder">${ order.price }</span>
                        </td>
                        <td class="text-end" data-order="${ order.date }">
                            <span class="fw-bolder">${ order.date }</span>
                        </td>
                        <!--end::Date Modified=-->
                        <!--begin::Action=-->
                        <td class="text-end">
                            <a class="btn btn-sm btn-light btn-active-light-primary" data-kt-menu-trigger="click"
                                data-kt-menu-placement="bottom-end">Actions
                                <!--begin::Svg Icon | path: icons/duotune/arrows/arr072.svg-->
                                <span class="svg-icon svg-icon-5 m-0">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                                        <path
                                            d="M11.4343 12.7344L7.25 8.55005C6.83579 8.13583 6.16421 8.13584 5.75 8.55005C5.33579 8.96426 5.33579 9.63583 5.75 10.05L11.2929 15.5929C11.6834 15.9835 12.3166 15.9835 12.7071 15.5929L18.25 10.05C18.6642 9.63584 18.6642 8.96426 18.25 8.55005C17.8358 8.13584 17.1642 8.13584 16.75 8.55005L12.5657 12.7344C12.2533 13.0468 11.7467 13.0468 11.4343 12.7344Z"
                                            fill="currentColor" />
                                    </svg>
                                </span>
                            </a>
                            <!--begin::Menu-->
                            <div class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-bold fs-7 w-125px py-4"
                                data-kt-menu="true">
                                <div class="menu-item px-3">
                                    <a href="/admin/order/${ order.id }" class="menu-link px-3">View</a>
                                </div>
                                <div class="menu-item px-3">
                                    <a href="/admin/delete_order/${ order.id }" class="menu-link px-3" data-kt-ecommerce-order-filter="delete_row">Delete</a>
                                </div>
                            </div>
                        </td>
                    </tr>
                `
                + $('#products-table').html()
            )
        }

        $('.btn.btn-sm.btn-light.btn-active-light-primary').on('click', (e) => {
            console.log(e.target)
            for (let btn of $('.btn.btn-sm.btn-light.btn-active-light-primary')) {
                $(btn).removeClass('show menu-dropdown')
            }
            $(e.target).addClass('show menu-dropdown')
            $(e.target).parent().find('.menu.menu-sub.menu-sub-dropdown.menu-column.menu-rounded.menu-gray-600.menu-state-bg-light-primary.fw-bold.fs-7.w-125px.py-4').toggleClass('show')
            $(e.target).parent().find('.menu.menu-sub.menu-sub-dropdown.menu-column.menu-rounded.menu-gray-600.menu-state-bg-light-primary.fw-bold.fs-7.w-125px.py-4').css({ "z-index": "105", "position": "fixed", "inset": "0px 0px auto auto", "margin": "0px", "transform": "translate3d(-59px, 226px, 0px)" })

        })
    }

    function renderOrders(data) {
        for (let user of data) {
            $('#products-table').html(
                `
                                    
                `
                + $('#products-table').html()
            )
        }

        $('.btn.btn-sm.btn-light.btn-active-light-primary').on('click', (e) => {
            console.log(e.target)
            for (let btn of $('.btn.btn-sm.btn-light.btn-active-light-primary')) {
                $(btn).removeClass('show menu-dropdown')
            }
            $(e.target).addClass('show menu-dropdown')
            $(e.target).parent().find('.menu.menu-sub.menu-sub-dropdown.menu-column.menu-rounded.menu-gray-600.menu-state-bg-light-primary.fw-bold.fs-7.w-125px.py-4').toggleClass('show')
            $(e.target).parent().find('.menu.menu-sub.menu-sub-dropdown.menu-column.menu-rounded.menu-gray-600.menu-state-bg-light-primary.fw-bold.fs-7.w-125px.py-4').css({ "z-index": "105", "position": "fixed", "inset": "0px 0px auto auto", "margin": "0px", "transform": "translate3d(-59px, 226px, 0px)" })

        })
    }
})


