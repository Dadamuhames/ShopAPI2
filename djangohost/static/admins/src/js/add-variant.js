$(document).ready(function() {
    $('#id_product').on('change', (e) => {
        $(".atribut-content").html('')
        let id = $(e.target).val()
        let url = '/admin/get_atr' 
        let csrf = $('[name="csrfmiddlewaretoken"]').val()
        data = {}
        data['csrfmiddlewaretoken'] = csrf
        data.id = id

        if(id != '') {
            $.ajax({
                url: url,
                data: data,
                datatype: 'json',
                type: 'POST',
                success: (data) => {
                    for(let key in data) {
                        opts = data[String(key)]
                        let id = key.split(' ')[0]
                        $(".atribut-content").html(
                            `
                                <label class="form-label" id="ctg-label-for-data">${key}</label>
                                <select name="atribut_${id}" class="form-select mb-2" id="select_atr_${id}" required>  
                                    
                                </select>
                                <div class="text-muted fs-7 mb-7">Add atribut to product</div>

                            ` + $(".atribut-content").html()
                        )   
                        $(`#select_atr_${id}`).html('<option value="">-----</option>')
                        for (let option in opts) {
                            $(`#select_atr_${id}`).html(
                                $(`#select_atr_${id}`).html() + `
                                <option value="${option}">${opts[String(option)]}</option>
                            `
                            )
                        }                 
                    }

                }
            })            
        } else {
            $(".atribut-content").html('')
        }


    })
})