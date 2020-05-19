$(document).ready(function() {
    $(document).on("click", ".add-server", function () {
        $('.add-server').prop('disabled', true);
        var server_ip = $(".server-ip").val();
        $.ajax({
            url: '/add',
            type: 'POST',
            data: {ip: server_ip},
            success: function (data) {
                $(".server-ip").val("");
                toastr.success(data.message);
                $('#exampleModal').modal('hide');
                $('.add-server').prop('disabled', false);
            },
            error: function (data) {
                toastr.error(data.responseJSON.message);
                $('.add-server').prop('disabled', false);
            }
        });
    });
    $(function(){
      $(".add-vote").click(function(){
         window.server_id = $(this).attr('serverid');
         $("#voteModal").modal("show");
      });
    });
    $(document).on("click", ".add-vote-button", function () {
        $('.add-vote-button').prop('disabled', true);
        var csrftoken = $('#csrf_token').val();
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            }
        });
        var server_id = window.server_id;
        $('.add-server').prop('disabled', true);
        $.ajax({
            url: '/add_vote',
            type: 'POST',
            data: {id: server_id, recaptcha : grecaptcha.getResponse()},
            success: function (data) {
                grecaptcha.reset();
                $(".server-ip").val("");
                toastr.success(data.message);
                $('#voteModal').modal('hide');
                $('.server-votes' + server_id).text(data.votes);
                $('.add-vote-button').prop('disabled', false);
            },
            error: function (data) {
                grecaptcha.reset();
                toastr.error(data.responseJSON.message);
                $('.add-vote-button').prop('disabled', false);
            }
        });
    });
});