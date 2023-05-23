

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
                    $("#subject-submit").attr("disabled", "disabled");
                    $("#subject-submit").val("Saving...");
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
                            $('#subject-form-div').html(response.template)     
                        } 
                    }                
                },
                complete: function() {
                    $("#subject-submit").attr("disabled", false);
                    $("#subject-submit").val("Save");
                },
            });
        },
    });
});



function FilterSubjects(page) {
    if (page == '') {
        page = $('#current_page').val()
    }
    var url = $('#load_subject').val()
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: { 'page': page },
        beforeSend: function() {},
        success: function(response) {
            $('#subject-tbody').html(response.template)
            $('#subject-pagination').html(response.pagination)
        },
    });
}



$(document).on('click', '#create_subject', function(event) {
    event.preventDefault();
    var url = $(this).attr('data-url')
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function() {
            $('#subject-form-div').html('Loading...')
        },
        success: function(response) {            
            $('#subject-form-div').html(response.template)
            $('#popup_head').html(response.title)
        },
    });
})


$(document).on('click', '.subject-edit', function(event) {
    event.preventDefault();
    var url = $(this).attr('data-url')
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
        method: "GET",
        data: {},
        beforeSend: function() {
            $('#subject-form-div').html('Loading...')
        },
        success: function(response) {
            $('#subject-form-div').html(response.template)
            $('#popup_head').html(response.title)
        },
    });
})

// Function to delete subject
function DeleteSubject(id) {
    var url = '/subject/' + String(id) + '/delete/'
    swal({
        icon: "warning",
        title: "Verify Details",
        text: "Are you sure you want to delete this record?",
        buttons: true,
        dangerMode: true,
    }).then(function(okey) {
        if (okey) {
            $.ajax({
                url: url,
                headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
                method: "POST",
                data: {},
                beforeSend: function() {},
                success: function(response) {
                    if (response.status) {
                        $(".msg_desc").text(response.message);
                        $("#flash_message_success").attr("style", "display:block;");
                        setTimeout(function() {
                            $("#flash_message_success").attr("style", "display:none;");
                        }, 3500);
                        FilterSubjects('')
                    }
                },
            });
        }
    });
}



// $(document).ready(function() {
// $('#search-form').submit(function(event) {
//     event.preventDefault();  // Prevent form submission
//     var searchQuery = $('#search-input').val();
//     $.ajax({
//         url: '/search/',  // URL
//         type: 'GET',
//         data: { search_query: searchQuery },
//         success: function(response) {
//             console.log(response)
          

//             var results = response.results;
//             var resultsContainer = $('#results-container');
//             resultsContainer.empty();
//             if (results.length > 0) {
//                 var ul = $('<ul>');
//                 for (var i = 0; i < results.length; i++) {
//                     var li = $('<li>').text(results[i].name);
//                     ul.append(li);
//                 }
//                 resultsContainer.append(ul);
//             } else {
//                 resultsContainer.text('No results found.');
//             }
//         }
//     });
// });
// });

$(document).ready(function() {
    $('#search-form').submit(function(event) {
        event.preventDefault();  // Prevent form submission
        var searchQuery = $('#search-input').val();
        $.ajax({
            url: '/search/',  // URL
            type: 'GET',
            data: { search_query: searchQuery },
            success: function(response) {
                console.log(response);

                var results = response.results;
                var resultsContainer = $('#results-container');
                resultsContainer.empty();
                if (results.length > 0) {
                    var table = $('<table>');
                    var thead = $('<thead>');
                    var tbody = $('<tbody>');

                    // Create table header
                    var headerRow = $('<tr>');
                    headerRow.append($('<th>').text('id'));
                    headerRow.append($('<th>').text('Name'));
                    headerRow.append($('<th>').text('Course'));
                    thead.append(headerRow);

                    // Create table rows for each result
                    for (var i = 0; i < results.length; i++) {
                        var result = results[i];
                        var row = $('<tr>');
                        row.append($('<td>').text(result.id));
                        row.append($('<td>').text(result.name));
                       
                        row.append($('<td>').text(result.course));
                        tbody.append(row);
                    }

                    table.append(thead);
                    table.append(tbody);
                    resultsContainer.append(table);
                } else {
                    resultsContainer.text('No results found.');
                }
            }
        });
    });
});
