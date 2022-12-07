$("#colors-select").on('change', (e) => {
    let color = $('#colors-select option:selected').attr('data-color')
    $('.color-block').css({ 'background': color })
})

$("#post_ctg").html('')
let id = $("#post_ctg").attr("data-id")
let url = '/get_categories/' + id
let post_id = $("#post_ctg").attr("data-post-id") 
let prod_id = $('#post_ctg').attr('data-prod-id')

$.ajax({
    url: url,
    type: 'POST',
    datatype: 'json',
    success: function (data) {
        console.log(data)
    },
    error: function () {
        console.log('error')
    }
})


$(".chs-image > .del-image-btn").on('click', (e) => {
    let del_url = $(e.target).attr("data-url");
    let del_id = $(e.target).attr("data-image-id"); 
    console.log($(`.chs-image[data-image-id='${del_id}']`))
    $.ajax({
        url: del_url,
        success: () => {
            $(`.chs-image[data-image-id='${del_id}']`).remove()
        }
    })
})


$(".image_files").on("change", (e) => {
    let files = e.target.files
    let id = $(e.target).attr('data-id')
    let block = $(`[data-id='${id}']`)
    renderFiles(files, $(e.target), block)
    console.log($(".del-image-btn.del-no-ajax"))
    console.log($('.chs-image'))
})


$(".del-image-btn").on('click', (e) => {
    let del_id = $(e.target).attr("data-image-id");
    let id = $(e.target).parent().parent().attr('data-id')
    let inp = $(`input[data-id='${id}']`)[0]
    let files = inp.files
    delete files[Number(del_id)]
    inp.files = files
    console.log(inp, files)
    renderFiles(inp.files, inp, $(e.target).parent().parent()[0])
})





const renderFiles = (files, input, block) => {
    lst = []
    let mult_inp = $(input)[0];
    var dt = new DataTransfer();
    for (let i = 0; i < files.length; i++) {
        dt.items.add(new File([files[i]], `photo_${i}.jpg`, { type: 'png/jpg' }));
        let reader = new FileReader()
        reader.onload = (function (e) {
            $(block).html(
                $(block).html() +
                `
                    <div class="chs-image" data-delurl='${i}' id='ch-img-${i}'>
                        <span data-url="${e.target.result}" data-image-id="${i}" data-photo='${e}' class="del-image-btn del-no-ajax">x</span>
                        <img src="${e.target.result}" alt="">
                    </div>
                `
            )

            let del_btn = document.querySelectorAll('.del-no-ajax')
            for(let btn of del_btn) {
                
                btn.onclick = (e) => {
                    console.log('<Begin>')
                    console.log()
                    let i = $(e.target).attr("data-image-id");
                    console.log(i)
                    $(`.chs-image[data-delurl='${i}']`).remove()
                    lst.splice(i, 1)
                    var dt2 = new DataTransfer();

                    for(let l of lst) {
                        dt2.items.add(new File([l], `photo.jpg`, { type: 'png/jpg' }));
                    }
                    
                    mult_inp.value = ''
                    mult_inp.files = dt2.files
                    console.log(mult_inp)
                    console.log(mult_inp.files)
                    console.log($('input[name="files"]')[0].files)
                    console.log('<End>')
                }
            }


        })
        reader.readAsDataURL(files[i]);
    }
    var file_list = dt.files;
    for(let file of file_list){
        lst.push(file)
    }
    console.log('!!!!!', lst)
}


function categorySelect(e) {
    let id = $(e.target).val()
    let url = '/api/admin/get_category/' + id
    console.log(id, url)

    $('#atribut-container').html(`
        <a href="{% url 'add-ctg' %}" class="btn btn-light-primary btn-sm mb-10" style="margin-bottom: 0 !important;">
            <!--begin::Svg Icon | path: icons/duotune/arrows/arr087.svg-->
            <span class="svg-icon svg-icon-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <rect opacity="0.5" x="11" y="18" width="12" height="2" rx="1" transform="rotate(-90 11 18)"
                        fill="currentColor"></rect>
                    <rect x="6" y="11" width="12" height="2" rx="1" fill="currentColor"></rect>
                </svg>
            </span>
            <!--end::Svg Icon-->Create new atribut
        </a>    
    `)

    $.ajax({
        url: url,
        type: 'GET',
        datatype: 'json',
        success: function (data) {
            if(data.length == 0) {
                return;
            }
            $('#ctg-block').html(
                $('#ctg-block').html() +
                `
                    <label class="form-label">Category</label>
                    <select name="category" class="form-select mb-2 category-select" required="">
                        <option value="">-----</option>
                    </select>
                `
            )

            for (let it of data) {
                $(".category-select").last().html(
                    $(".category-select").last().html() + `
                        <option value="${it.id}">${it.name}</option>
                    `
                )
            }

            $(".category-select").last().change((e) => {
                categorySelect(e)
            })

        },
        error: function () {
            console.log('error')
        }
    })
}


$('.category-select').change((e) => {
    categorySelect(e)
})



