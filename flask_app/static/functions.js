const content_div_id_list = ["get_job_content_div", "post_image_content_div", "get_audio_button_div"];

var toggle_content = function (content_div_id) {
    for (let index = 0; index < content_div_id_list.length; index++) {
        if (content_div_id === content_div_id_list[index]) {

            $("#" + content_div_id_list[index]).removeClass("d-none");
        } else {
            $("#" + content_div_id_list[index]).addClass("d-none");
        }
    }
};

var get_base64_string_from_img = function (selector) {
    let data_url = $(selector).prop("src");
    return data_url.replace(/^data:image\/(png|jpg|jpeg);base64,/, "");
};

var loadFile = function (event) {
    var reader = new FileReader();
    reader.onload = function () {
        $("#output_img").prop("src", reader.result);
        $("#output_img").removeClass("d-none");
    };
    reader.readAsDataURL(event.target.files[0]);
};

window.onload = function () {
    $("#get_job_button").click(function () {
        $.ajax({
            url: "job", type: "GET", success: function (result) {
                toggle_content("get_job_content_div");
                document.getElementById("json").innerHTML = JSON.stringify(result, undefined, 2);
            }
        });
    });

    $("#post_image_button").click(function () {
        let data = {
            user_id: "test_user",
            img: get_base64_string_from_img("#output_img"),
            job_id: parseInt($("#job_select").val())
        };

        $.ajax("image", {
            data: JSON.stringify(data),
            contentType: 'application/json',
            type: 'POST',
            success: function (result) {
                toggle_content("post_image_content_div");
                $("#post_image_content_img").prop("src", "data:image/png;base64, " + result["output_img"]);
            }
        });
    });

    $("#get_audio_button").click(function () {
        let audio_text_input = $("#audio_text_input").val();
        audio_text_input = audio_text_input.trim()
        audio_text_input = audio_text_input.toLowerCase()
        audio_text_input = audio_text_input.replace(' ', '_')

        let url = new URL(`/audio/${audio_text_input}`, window.location.href);

        $('#audio_source').prop('src', url.href);
        $('#audio').get(0).load();
        toggle_content("get_audio_button_div");
    });
};
