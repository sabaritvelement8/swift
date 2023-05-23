$(document).ready(function () {
    $("#CourseForm").validate({
        rules: {},
        messages: {},
        submitHandler: function (form, event) {
            event.preventDefault();
            var formData = $("#CourseForm").serializeArray();
            var url = $("#form_url").val()
            $.ajax({
                url: url,
                headers: {
                    "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
                },
                method: "POST",
                data: formData,
                beforeSend: function () {
                    $("#course-submit").attr("disabled", "disabled");
                    $("#course-submit").val("Saving...");
                },
                success: function (response) {
                    if (response.status) {
                        $(".carousel__button").click()
                        FilterCourse('')
                        $(".msg_desc").text(response.message)
                        $("#flash_message_success").attr("style", "display:block;")
                        setTimeout(function () {
                            $("#flash_message_success").attr("style", "display:none;")
                        }, 3500)
                    } else {
                        if ('message' in response) {
                            $(".carousel__button").click()
                            $(".msg_desc").text(response.message)
                            $("#flash_message_error").attr("style", "display:block;")
                            setTimeout(function () {
                                $("#flash_message_error").attr("style", "display:none;")
                            }, 3500)
                        } else {
                            $('#course-form-div').html(response.template)
                        }
                    }
                },
                complete: function () {
                    $("#course-submit").attr("disabled", false);
                    $("#course-submit").val("Save");
                },
            });
        },
    });
});

function FilterCourse(page) {
    if (page == '') {
        page = $('#current_page').val()
    }
    var url = $('#load_course').val()
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: { 'page': page },
        beforeSend: function () { },
        success: function (response) {
            $('#course-tbody').html(response.template)
            $('#course-pagination').html(response.pagination)
        },
    });
}

$(document).on('click', '#create_course', function (event) {
    event.preventDefault();
    var url = $(this).attr('data-url')
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function () {
            $('#course-form-div').html('Loading...')
        },
        success: function (response) {
            $('#course-form-div').html(response.template)
            $('#popup_head').html(response.title)
        },
    });
})
$(document).on('click', '.course-edit', function (event) {
    event.preventDefault();
    var url = $(this).attr('data-url')
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function () {
            $('#course-form-div').html('Loading...')
        },
        success: function (response) {
            $('#course-form-div').html(response.template)
            $('#popup_head').html(response.title)
        },
    });
})

// Function to delete course
function DeleteCourse(id) {
    var url = '/course/' + String(id) + '/delete/'
    swal({
        icon: "warning",
        title: "Verify Details",
        text: "Are you sure you want to delete this record?",
        buttons: true,
        dangerMode: true,
    }).then(function (okey) {
        if (okey) {
            $.ajax({
                url: url,
                headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
                method: "POST",
                data: {},
                beforeSend: function () { },
                success: function (response) {
                    if (response.status) {
                        $(".msg_desc").text(response.message);
                        $("#flash_message_success").attr("style", "display:block;");
                        setTimeout(function () {
                            $("#flash_message_success").attr("style", "display:none;");
                        }, 3500);
                        FilterCourse('')
                    }
                },
            });
        }
    });
}