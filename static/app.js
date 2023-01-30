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
