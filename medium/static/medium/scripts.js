(function () {
    // your page initialization code here
    // the DOM will be available here

    function test() {
        console.log('js loaded')
    }

    test()


    var featured = document.getElementById("id_featured_image");
    featured.onchange = function () {
        var reader = new FileReader();

        reader.onload = function (e) {
            // get loaded data and render thumbnail.
            document.getElementById("featured").src = e.target.result;
        };

        // read the image file as a data URL.
        reader.readAsDataURL(this.files[0]);
    };



})();