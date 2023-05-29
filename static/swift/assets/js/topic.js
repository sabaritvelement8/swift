$(document).ready(function() {
    $("#SubjectsForm").validate({
        rules: {},
        messages: {},
        submitHandler: function(form, event) {
            event.preventDefault();
            var formData = $("#SubjectsForm").serializeArray();
            var url = $("#form_url").val()
            $.ajax({
                url: url,
                headers: {
                    "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
                },
                method: "POST",
                data: formData,
                beforeSend: function() {
                    $("#topic-submit").attr("disabled", "disabled");
                    $("#topic-submit").val("Saving...");
                },
                success: function(response) {
                    if (response.status) {                        
                        $(".carousel__button").click()
                        FilterSubjects('')
                        $(".msg_desc").text(response.message)
                        $("#flash_message_success").attr("style", "display:block;")
                        setTimeout(function() {
                            $("#flash_message_success").attr("style", "display:none;")
                        }, 3500)
                    } else {                       
                        if ('message' in response ){
                            $(".carousel__button").click()
                            $(".msg_desc").text(response.message)
                            $("#flash_message_error").attr("style", "display:block;")
                            setTimeout(function() {
                                $("#flash_message_error").attr("style", "display:none;")
                            }, 3500)                                                       
                        } else {                      
                            $('#topic-form-div').html(response.template)     
                        } 
                    }                
                },
                complete: function() {
                    $("#topic-submit").attr("disabled", false);
                    $("#topic-submit").val("Save");
                },
            });
        },
    });
});



function FilterSubjects(page) {
    if (page == '') {
        page = $('#current_page').val()
    }
    var url = $('#load_topic').val()
    var filter = $('#search-id').val()
    var course = $('#topic-select').val()

    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: { 'page': page ,
              'filter':filter,
                'topic':topic},
        beforeSend: function() {},
        success: function(response) {
            $('#subject-tbody').html(response.template)
            $('#subject-pagination').html(response.pagination)
        },
    });
}


// live search
// $('#form').on('keyup', function () {
//     var filter = $(this).val();
//     FilterSubjects(filter);
// });

// // dropdown

// $('#course-select').change(function () {
    
//     FilterSubjects('');
// });

// //res
// $('#reset-button').click(function() {
//     $('#search-id').val('');  // Clear the search input
//     $('#course-select').val(''); 
//     FilterSubjects();  
// });


$(document).on('click', '#create_topic', function(event) {
    event.preventDefault();
    var url = $(this).attr('data-url')
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function() {
            $('#topic-form-div').html('Loading...')
        },
        success: function(response) {            
            $('#topic-form-div').html(response.template)
            $('#popup_head').html(response.title)
        },
    });
})


// $(document).on('click', '.subject-edit', function(event) {
//     event.preventDefault();
//     var url = $(this).attr('data-url')
//     $.ajax({
//         url: url,
//         headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
//         method: "GET",
//         data: {},
//         beforeSend: function() {
//             $('#subject-form-div').html('Loading...')
//         },
//         success: function(response) {
//             $('#subject-form-div').html(response.template)
//             $('#popup_head').html(response.title)
//         },
//     });
// })

// // Function to delete subject
// function DeleteSubject(id) {
//     var url = '/subject/' + String(id) + '/delete/'
//     swal({
//         icon: "warning",
//         title: "Verify Details",
//         text: "Are you sure you want to delete this record?",
//         buttons: true,
//         dangerMode: true,
//     }).then(function(okey) {
//         if (okey) {
//             $.ajax({
//                 url: url,
//                 headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
//                 method: "POST",
//                 data: {},
//                 beforeSend: function() {},
//                 success: function(response) {
//                     if (response.status) {
//                         $(".msg_desc").text(response.message);
//                         $("#flash_message_success").attr("style", "display:block;");
//                         setTimeout(function() {
//                             $("#flash_message_success").attr("style", "display:none;");
//                         }, 3500);
//                         FilterSubjects('')
//                     }
//                 },
//             });
//         }
//     });
// }



