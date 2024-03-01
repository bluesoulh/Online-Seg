    function showImg(input) {
        var file = input.files[0];
        var reader = new FileReader()
        // 图片读取成功回调函数
        reader.onload = function(e) {
            document.getElementById('upload').src=e.target.result
        }
        reader.readAsDataURL(file)
    }
    $(document).ready(function() {
        $("#submit-button").click(function() {
        var formData = new FormData();
        formData.append('file', $("#upload-input")[0].files[0]);
        $.ajax({
            url: "/segmentation/segm",
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
        });
      });
    });