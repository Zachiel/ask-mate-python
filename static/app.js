// Show uploaded image
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $("#imageResult").attr("src", e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

$(function () {
    $("#upload").on("change", function () {
        const size = (this.files[0].size / 1024 / 1024).toFixed(2);

        if (size > 1) {
            alert("File must be up to 1 MB");
            $("#imageResult").attr("src", "");
            $("upload").value = "";
        } else {
            $("#image-preview").removeClass("hidden");
            $("#upload-label").text(this.files[0].name);
            readURL(input);
        }
    });
});

$(document).ready(function () {
    "use strict";
    var forms = $(".needs-validation");
    var validation = Array.prototype.filter.call(forms, function (form) {
        form.addEventListener(
            "submit",
            function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add("was-validated");
            },
            false
        );
    });
});

$(function () {
    $('a[href="#search"]').on("click", function (event) {
        event.preventDefault();
        $("#search").addClass("open");
        $('#search > form > input[type="search"]').focus();
    });
    $("#search-fullscreen").keyup(function () {
        search = $("#search-input");
        searchFullscreen = $("#search-fullscreen");
        search.val(searchFullscreen.val());
        $.ajax({
            type: "POST",
            url: "/search",
            data: { search: search.val() },
            datatype: "json",
            success: function (data) {
                $("#search-result").empty();
                data.forEach(function (question) {
                    questionDict = JSON.stringify(question);
                    var str = question["message"];
                    if (str.length > 200) str = str.substring(0, 200) + " ...";
                    $("#search-result").append(`
                    <a href="/question/${question["id"]}">
                        <div class="row justify-content-between align-items-start g-2 my-3">
                            <div class="col-1">
                                <img class="img-fluid result-image" onerror="this.style.display='none'" src="${
                                    !question["image"] ? "" : question["image"]
                                }"/>
                            </div>
                            <div class="col mx-5">${question["title"]}</div>
                            <div class="col mx-5">${str}</div>
                            <div class="col">Tags: ${
                                !question["tag_name"]
                                    ? ""
                                    : question["tag_name"]
                            }</div>
                        </div>
                    </a>
                    `);
                });
            },
        });
    });
    $("#search, #search button.close").on("click keyup", function (event) {
        if (
            event.target == this ||
            event.target.className == "close" ||
            event.keyCode == 27
        ) {
            $(this).removeClass("open");
        }
    });
});
